"""Verificación de las entregas de webhooks de FiscalAPI.

FiscalAPI firma cada entrega con Standard Webhooks (https://www.standardwebhooks.com): HMAC-SHA256 sobre
``webhook-id.webhook-timestamp.cuerpo`` con el secreto ``whsec_…`` del endpoint, en el header ``webhook-signature`` como
``v1,<base64>``. La firma es la única prueba de que una entrega viene de FiscalAPI.

Ejemplo::

    from fiscalapi import webhooks, WebhookVerificationException

    try:
        event = webhooks.verify(request.headers, request.get_data(), secret)
    except WebhookVerificationException:
        ...  # responda 400 y no procese la entrega
"""

import base64
import hashlib
import hmac
import json
import re
import time
from collections.abc import Iterable, Mapping
from datetime import timedelta
from typing import Final, Optional, Union

from pydantic import ValidationError

from .models.webhook_models import WebhookEvent

DEFAULT_TOLERANCE: Final = timedelta(minutes=5)
"""Diferencia máxima entre ``webhook-timestamp`` y el reloj del receptor, hacia atrás o hacia adelante: una entrega
capturada no se puede repetir después."""

_ID_HEADER: Final = "webhook-id"
_TIMESTAMP_HEADER: Final = "webhook-timestamp"
_SIGNATURE_HEADER: Final = "webhook-signature"
_SIGNATURE_VERSION: Final = "v1"
_SIGNATURE_SEPARATOR: Final = " "
_VERSION_SEPARATOR: Final = ","
_SECRET_PREFIX: Final = "whsec_"

# Solo dígitos ASCII: un signo, espacios, decimales o dígitos de otros alfabetos no son segundos Unix. El tope es el de un
# entero de 64 bits, el mismo que aceptan los demás SDK; el largo se limita antes de convertir a int.
_UNIX_SECONDS: Final = re.compile(r"[0-9]{1,19}")
_MAX_UNIX_SECONDS: Final = 2 ** 63 - 1

_NOT_AN_EVENT: Final = "El cuerpo firmado no es un evento de webhook en JSON."
_NOT_UTF8: Final = "El cuerpo o un header no es texto UTF-8 válido."


class WebhookVerificationException(Exception):
    """La entrega no se puede tratar como auténtica: falta un header de Standard Webhooks, ninguna firma coincide, el
    timestamp está fuera de la tolerancia, el cuerpo no es texto UTF-8 válido o el cuerpo firmado no es un evento. El
    receptor la rechaza (por ejemplo con un 400) y no la procesa. La causa original, si la hay, queda en ``__cause__``.
    """


def verify(
    headers: Mapping[str, str],
    body: Union[bytes, str],
    secret: Union[str, Iterable[str]],
    tolerance: timedelta = DEFAULT_TOLERANCE,
) -> WebhookEvent:
    """Verifica una entrega con el secreto del endpoint y devuelve su evento.

    Responda 2xx rápido y procese el evento después, fuera de la petición: FiscalAPI corta cada intento a los 15 s y lo
    reintenta. La entrega es al menos una vez: ``event.id`` (el header ``webhook-id``) se repite en cada reintento.

    Args:
        headers: Los headers de la petición recibida, con los nombres sin distinguir mayúsculas: el ``request.headers``
            de Flask, Django o FastAPI/Starlette, un ``dict`` o cualquier objeto con ``items()``.
        body: El cuerpo **crudo** tal como llegó, antes de deserializarlo; de preferencia los ``bytes``
            (``request.get_data()`` en Flask, ``request.body`` en Django, ``await request.body()`` en FastAPI). Un
            ``str`` se firma con su UTF-8. Un cuerpo deserializado y vuelto a serializar cambia sus bytes (espacios,
            orden, escapes) y su firma deja de coincidir.
        secret: El secreto del endpoint (``whsec_…``, o sin el prefijo) o una lista de secretos: durante una rotación,
            FiscalAPI firma con el nuevo y con el anterior por 24 h y basta que una firma ``v1`` coincida con uno.
        tolerance: Tolerancia del timestamp; por omisión ``DEFAULT_TOLERANCE`` (5 minutos).

    Returns:
        El evento del cuerpo verificado.

    Raises:
        WebhookVerificationException: Falta un header, el timestamp está fuera de la tolerancia, ninguna firma ``v1``
            coincide, el cuerpo no es texto UTF-8 válido o el cuerpo firmado no es un evento: rechace la entrega sin
            procesarla.
        ValueError: Un secreto no es base64 o está vacío, la lista de secretos está vacía o la tolerancia es negativa.
        TypeError: Un argumento es ``None`` o de otro tipo. ``ValueError`` y ``TypeError`` son errores de configuración
            del receptor, no de la entrega; en una lista indican la posición del secreto y nunca su valor.
    """
    return _verify_at(headers, body, secret, tolerance, int(time.time()))


def _verify_at(
    headers: Mapping[str, str],
    body: Union[bytes, str],
    secret: Union[str, Iterable[str]],
    tolerance: timedelta,
    now: int,
) -> WebhookEvent:
    """La verificación contra ``now``, los segundos Unix del reloj del receptor."""
    keys = _signing_keys(secret)
    _ensure_arguments(headers, body, tolerance)

    event_id = _required_header(headers, _ID_HEADER)
    timestamp = _required_header(headers, _TIMESTAMP_HEADER)
    signatures = _required_header(headers, _SIGNATURE_HEADER)

    _ensure_within_tolerance(timestamp, tolerance, now)
    text = _body_text(body)
    _ensure_signed(keys, _signed_content(event_id, timestamp, text), signatures)
    return _read_event(text)


def _ensure_arguments(headers: Mapping[str, str], body: Union[bytes, str], tolerance: timedelta) -> None:
    # Se exige items() y no Mapping: el request.headers de Flask (werkzeug) tiene items() sin ser un Mapping.
    if headers is None or not callable(getattr(headers, "items", None)):
        raise TypeError("headers debe ser un Mapping con los headers de la petición (por ejemplo request.headers).")
    if not isinstance(body, (bytes, bytearray, str)):
        raise TypeError("body debe ser el cuerpo crudo de la petición, en bytes o str.")
    if not isinstance(tolerance, timedelta):
        raise TypeError("tolerance debe ser un datetime.timedelta.")
    if tolerance < timedelta(0):
        raise ValueError("La tolerancia no puede ser negativa.")


class _SigningKey:
    """La llave HMAC de un secreto de firma. Nunca se muestra: los rastreadores de errores (Sentry y otros) capturan las
    variables locales de cada marco con ``repr()`` y solo tapan las que se llaman ``secret``."""

    __slots__ = ("_key",)

    def __init__(self, key: bytes) -> None:
        self._key = key

    @classmethod
    def decode(cls, secret: str) -> Optional["_SigningKey"]:
        """La llave del secreto (``whsec_…`` o sin el prefijo); None si no es base64. El texto del secreto solo vive en
        variables llamadas ``secret``, y el error de base64 no se encadena porque su rastro llevaría el secreto."""
        try:
            return cls(base64.b64decode(secret[len(_SECRET_PREFIX):] if secret.startswith(_SECRET_PREFIX) else secret,
                                        validate=True))
        except ValueError:  # binascii.Error (no es base64) o texto no ASCII
            return None

    def __bool__(self) -> bool:
        return bool(self._key)

    def __repr__(self) -> str:
        return "***"

    __str__ = __repr__

    def sign(self, content: bytes) -> str:
        """La firma v1 de ``content``: HMAC-SHA256 en base64."""
        return base64.b64encode(hmac.new(self._key, content, hashlib.sha256).digest()).decode("ascii")


def _signing_keys(secret: Union[str, Iterable[str]]) -> list[_SigningKey]:
    if isinstance(secret, str):
        return [_decode_secret(secret, "El secreto de firma")]
    if isinstance(secret, (bytes, bytearray)) or not isinstance(secret, Iterable):
        raise TypeError("secret debe ser el secreto del endpoint (whsec_…) o una lista de secretos, como str.")

    # Cada secreto de la lista también se llama secret: es el nombre que tapan los rastreadores de errores.
    keys = [_decode_secret(secret, f"El secreto de firma en la posición {index}") for index, secret in enumerate(secret)]
    if not keys:
        raise ValueError("Se necesita al menos un secreto de firma (whsec_…).")
    return keys


def _decode_secret(secret: object, description: str) -> _SigningKey:
    # Los mensajes nombran el secreto por su posición y nunca incluyen su valor: terminarían en los logs del receptor.
    if not isinstance(secret, str):
        raise TypeError(f"{description} no es un str.")

    key = _SigningKey.decode(secret)
    if key is None:
        raise ValueError(f"{description} no es whsec_ seguido de base64: cópielo completo del webhook.")
    if not key:
        raise ValueError(f"{description} está vacío.")
    return key


def _required_header(headers: Mapping[str, str], name: str) -> str:
    value = next(
        (value for key, value in headers.items() if isinstance(key, str) and key.isascii() and key.lower() == name),
        None,
    )
    if not value:
        raise WebhookVerificationException(f"Falta el header {name}.")
    if not isinstance(value, str):
        raise TypeError(f"El header {name} debe llegar como str.")
    return value


def _ensure_within_tolerance(timestamp: str, tolerance: timedelta, now: int) -> None:
    if not _UNIX_SECONDS.fullmatch(timestamp) or int(timestamp) > _MAX_UNIX_SECONDS:
        raise WebhookVerificationException(f"El header {_TIMESTAMP_HEADER} no es un número de segundos Unix.")

    seconds = tolerance.total_seconds()
    if abs(now - int(timestamp)) > seconds:
        raise WebhookVerificationException(
            f"El header {_TIMESTAMP_HEADER} difiere más de {seconds:g} s del reloj del receptor: puede ser una entrega "
            "repetida o un reloj desajustado."
        )


def _body_text(body: Union[bytes, str]) -> str:
    # Los bytes se leen como UTF-8 estricto antes de firmar, en el mismo orden que los demás SDK. Un texto UTF-8 válido
    # vuelve a codificarse en los mismos bytes, así que se firma exactamente lo que llegó.
    if isinstance(body, str):
        return body
    try:
        return bytes(body).decode("utf-8")
    except UnicodeDecodeError as error:
        raise WebhookVerificationException(_NOT_UTF8) from error


def _signed_content(event_id: str, timestamp: str, text: str) -> bytes:
    # UTF-8 estricto: un texto con un sustituto suelto se rechaza en vez de firmarse con un carácter de reemplazo.
    try:
        return f"{event_id}.{timestamp}.{text}".encode("utf-8")
    except UnicodeEncodeError as error:
        raise WebhookVerificationException(_NOT_UTF8) from error


def _ensure_signed(keys: list[_SigningKey], signed_content: bytes, signature_header: str) -> None:
    expected = [key.sign(signed_content) for key in keys]
    candidates = [
        signature
        for signature in map(_v1_signature, signature_header.split(_SIGNATURE_SEPARATOR))
        if signature is not None
    ]
    # compare_digest compara en tiempo constante; ambos lados son texto ASCII.
    if not any(hmac.compare_digest(each, candidate) for candidate in candidates for each in expected):
        raise WebhookVerificationException(
            f"Ninguna firma {_SIGNATURE_VERSION} del header {_SIGNATURE_HEADER} coincide con el cuerpo y el secreto."
        )


def _v1_signature(entry: str) -> Optional[str]:
    """La firma de una entrada ``v1,<base64>``; None si es de otra versión, no tiene versión o no es ASCII (una firma
    v1 siempre lo es)."""
    version, separator, signature = entry.partition(_VERSION_SEPARATOR)
    if not separator or version != _SIGNATURE_VERSION or not signature.isascii():
        return None
    return signature


def _read_event(text: str) -> WebhookEvent:
    # json.loads ya rechaza el contenido sobrante después del evento; el literal null, una lista o un valor suelto se
    # leen sin error, pero model_validate los rechaza porque no son un objeto.
    try:
        envelope = json.loads(text)
    except (ValueError, RecursionError) as error:
        raise WebhookVerificationException(_NOT_AN_EVENT) from error

    try:
        return WebhookEvent.model_validate(envelope)
    except ValidationError as error:
        raise WebhookVerificationException(_NOT_AN_EVENT) from error
