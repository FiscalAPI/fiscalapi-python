"""webhooks.verify: la firma Standard Webhooks (HMAC-SHA256 sobre webhook-id.webhook-timestamp.cuerpo) y la tolerancia
del timestamp.

Los mismos escenarios viven en los SDK de .NET, Node.js, PHP y Java. El momento de la verificación se fija con
``webhooks._verify_at`` (segundos Unix del receptor), así el vector oficial (de 2021) verifica sin depender del reloj.
"""
import base64
import re
import time
import traceback
from collections.abc import Mapping
from datetime import timedelta
from typing import Callable, Iterator, Optional, Union

import pytest

from fiscalapi import WebhookEvent, WebhookVerificationException, webhooks
from webhook_signing import generate_secret, sign

# El vector publicado por Standard Webhooks (https://github.com/standard-webhooks/standard-webhooks): no es un secreto.
OFFICIAL_SECRET = "whsec_MfKQ9r8GKYqrTwjUPD8ILPZIo2LaLaSw"
OFFICIAL_ID = "msg_p5jXN8AQM9LWM0D4loKWxJek"
OFFICIAL_TIMESTAMP = 1614265330
OFFICIAL_BODY = '{"test": 2432232314}'
OFFICIAL_SIGNATURE = "v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE="

DEFAULT_SECONDS = 5 * 60
NOT_UTF8 = "El cuerpo o un header no es texto UTF-8 válido."


def official_headers(
    event_id: str = OFFICIAL_ID, timestamp: Optional[str] = None, signature: str = OFFICIAL_SIGNATURE
) -> dict:
    return {
        "webhook-id": event_id,
        "webhook-timestamp": str(OFFICIAL_TIMESTAMP) if timestamp is None else timestamp,
        "webhook-signature": signature,
    }


def verify_at(
    now: int,
    headers: Mapping,
    body: Union[str, bytes],
    secret: Union[str, list] = OFFICIAL_SECRET,
    tolerance: timedelta = webhooks.DEFAULT_TOLERANCE,
) -> WebhookEvent:
    return webhooks._verify_at(headers, body, secret, tolerance, now)


# --- Vector oficial y alteraciones ---


def test_the_official_vector_verifies():
    event = verify_at(OFFICIAL_TIMESTAMP, official_headers(), OFFICIAL_BODY)

    assert isinstance(event, WebhookEvent)


def test_the_official_vector_verifies_as_raw_bytes():
    event = verify_at(OFFICIAL_TIMESTAMP, official_headers(), OFFICIAL_BODY.encode("utf-8"))

    assert isinstance(event, WebhookEvent)


def test_a_tampered_signature_is_rejected():
    headers = official_headers(signature="v1,g0hM9SsF+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=")

    with pytest.raises(WebhookVerificationException, match="Ninguna firma"):
        verify_at(OFFICIAL_TIMESTAMP, headers, OFFICIAL_BODY)


def test_a_tampered_body_is_rejected():
    with pytest.raises(WebhookVerificationException, match="Ninguna firma"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(), '{"test": 2432232315}')


def test_a_body_reformatted_after_signing_is_rejected():
    # Mismo JSON sin el espacio: verificar exige el cuerpo crudo, no uno reserializado.
    with pytest.raises(WebhookVerificationException, match="Ninguna firma"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(), '{"test":2432232314}')


def test_a_tampered_id_is_rejected():
    with pytest.raises(WebhookVerificationException, match="Ninguna firma"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(event_id="msg_otro"), OFFICIAL_BODY)


# --- Tolerancia del timestamp ---


def test_a_timestamp_older_than_the_tolerance_is_rejected_and_the_boundary_is_accepted():
    verify_at(OFFICIAL_TIMESTAMP + DEFAULT_SECONDS, official_headers(), OFFICIAL_BODY)

    with pytest.raises(WebhookVerificationException, match="webhook-timestamp difiere"):
        verify_at(OFFICIAL_TIMESTAMP + DEFAULT_SECONDS + 1, official_headers(), OFFICIAL_BODY)


def test_a_timestamp_further_in_the_future_than_the_tolerance_is_rejected_and_the_boundary_is_accepted():
    verify_at(OFFICIAL_TIMESTAMP - DEFAULT_SECONDS, official_headers(), OFFICIAL_BODY)

    with pytest.raises(WebhookVerificationException, match="webhook-timestamp difiere"):
        verify_at(OFFICIAL_TIMESTAMP - DEFAULT_SECONDS - 1, official_headers(), OFFICIAL_BODY)


def test_the_default_tolerance_is_five_minutes():
    assert webhooks.DEFAULT_TOLERANCE == timedelta(minutes=5)


def test_a_custom_tolerance_replaces_the_default():
    tolerance = timedelta(seconds=30)

    verify_at(OFFICIAL_TIMESTAMP + 30, official_headers(), OFFICIAL_BODY, tolerance=tolerance)
    with pytest.raises(WebhookVerificationException, match="difiere"):
        verify_at(OFFICIAL_TIMESTAMP + 31, official_headers(), OFFICIAL_BODY, tolerance=tolerance)


def test_a_negative_tolerance_is_refused():
    with pytest.raises(ValueError, match="tolerancia"):
        webhooks.verify(official_headers(), OFFICIAL_BODY, OFFICIAL_SECRET, timedelta(seconds=-1))


def test_a_tolerance_that_is_not_a_timedelta_is_refused():
    with pytest.raises(TypeError, match="timedelta"):
        webhooks.verify(official_headers(), OFFICIAL_BODY, OFFICIAL_SECRET, 300)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "timestamp",
    [
        "1614265330.5",
        "-1614265330",
        " 1614265330",
        "1614265330000000000000",
        pytest.param("9223372036854775808", id="int64-mas-uno"),
        "abc",
        pytest.param("١٦١٤٢٦٥٣٣٠", id="digitos-arabigos"),
        pytest.param("1" * 5000, id="5000-digitos"),
    ],
)
def test_a_timestamp_that_is_not_unix_seconds_is_rejected(timestamp):
    with pytest.raises(WebhookVerificationException, match="segundos Unix"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(timestamp=timestamp), OFFICIAL_BODY)


def test_the_largest_unix_timestamp_is_rejected_by_the_tolerance_without_overflowing():
    with pytest.raises(WebhookVerificationException, match="difiere"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(timestamp="9223372036854775807"), OFFICIAL_BODY)


def test_a_timestamp_altered_within_the_tolerance_is_rejected_because_it_is_signed():
    altered = OFFICIAL_TIMESTAMP + 1

    with pytest.raises(WebhookVerificationException, match="Ninguna firma"):
        verify_at(altered, official_headers(timestamp=str(altered)), OFFICIAL_BODY)


# --- Header de firma ---


@pytest.mark.parametrize(
    "signature",
    [
        "v1a,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=",
        "v2,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=",
        "g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=",
        "v1,",
        "v1,!!!",
        "v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OÉ=",
        pytest.param("v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE", id="v1-sin-relleno"),
    ],
)
def test_a_signature_header_without_a_valid_v1_signature_is_rejected(signature):
    with pytest.raises(WebhookVerificationException, match="Ninguna firma"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(signature=signature), OFFICIAL_BODY)


def test_any_valid_v1_signature_among_several_verifies():
    signature = "v1,AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA= v1a,ignorada malformada " + OFFICIAL_SIGNATURE

    verify_at(OFFICIAL_TIMESTAMP, official_headers(signature=signature), OFFICIAL_BODY)


# --- Cuerpo ---


def test_a_body_with_a_lone_surrogate_is_rejected_even_when_signed_over_its_replacement_character():
    # Un sustituto suelto no tiene UTF-8: un codificador tolerante lo cambiaría por otro carácter y verificaría otros bytes.
    body = '{"test": "\ud800"}'
    signature = sign(OFFICIAL_ID, OFFICIAL_TIMESTAMP, body.encode("utf-8", "replace"), OFFICIAL_SECRET)

    with pytest.raises(WebhookVerificationException, match=re.escape(NOT_UTF8)) as raised:
        verify_at(OFFICIAL_TIMESTAMP, official_headers(signature=signature), body)
    assert isinstance(raised.value.__cause__, UnicodeEncodeError)


def test_a_bytes_body_that_is_not_utf8_is_rejected_even_when_its_bytes_are_signed():
    # El equivalente en bytes del sustituto suelto: bytes que no son UTF-8 válido.
    body = b'{"test": "\xed\xa0\x80"}'
    signature = sign(OFFICIAL_ID, OFFICIAL_TIMESTAMP, body, OFFICIAL_SECRET)

    with pytest.raises(WebhookVerificationException, match=re.escape(NOT_UTF8)) as raised:
        verify_at(OFFICIAL_TIMESTAMP, official_headers(signature=signature), body)
    assert isinstance(raised.value.__cause__, UnicodeDecodeError)


def test_a_bytes_body_that_is_not_utf8_is_rejected_before_its_signature_is_checked():
    # Mismo orden que los demás SDK: el cuerpo se lee como UTF-8 estricto antes de firmar, sin importar la firma.
    body = b'{"test": "\xed\xa0\x80"}'

    with pytest.raises(WebhookVerificationException, match=re.escape(NOT_UTF8)) as raised:
        verify_at(OFFICIAL_TIMESTAMP, official_headers(), body)
    assert isinstance(raised.value.__cause__, UnicodeDecodeError)


@pytest.mark.parametrize("body", ['{"id":"evt_1"} {"id":"evt_2"}', "null", "[]", '"evt_1"', "2432232314"])
def test_a_signed_body_that_is_not_exactly_one_json_object_is_rejected(body):
    signature = sign(OFFICIAL_ID, OFFICIAL_TIMESTAMP, body, OFFICIAL_SECRET)

    with pytest.raises(WebhookVerificationException, match="no es un evento"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(signature=signature), body)


def test_a_correctly_signed_body_that_is_not_json_is_rejected_with_its_cause():
    body = "no es json"
    signature = sign(OFFICIAL_ID, OFFICIAL_TIMESTAMP, body, OFFICIAL_SECRET)

    with pytest.raises(WebhookVerificationException, match="no es un evento") as raised:
        verify_at(OFFICIAL_TIMESTAMP, official_headers(signature=signature), body)
    assert raised.value.__cause__ is not None


def test_a_signed_event_with_fields_of_the_wrong_shape_is_rejected_with_its_cause():
    body = '{"id":"evt_1","data":"no es un objeto"}'
    signature = sign(OFFICIAL_ID, OFFICIAL_TIMESTAMP, body, OFFICIAL_SECRET)

    with pytest.raises(WebhookVerificationException, match="no es un evento") as raised:
        verify_at(OFFICIAL_TIMESTAMP, official_headers(signature=signature), body)
    assert raised.value.__cause__ is not None


# --- Headers ---


@pytest.mark.parametrize("missing", ["webhook-id", "webhook-timestamp", "webhook-signature"])
def test_a_missing_header_is_rejected_naming_it(missing):
    headers = {name: value for name, value in official_headers().items() if name != missing}

    with pytest.raises(WebhookVerificationException, match=f"Falta el header {missing}."):
        verify_at(OFFICIAL_TIMESTAMP, headers, OFFICIAL_BODY)


@pytest.mark.parametrize("empty", ["webhook-id", "webhook-timestamp", "webhook-signature"])
def test_an_empty_header_is_rejected_as_missing(empty):
    headers = {**official_headers(), empty: ""}

    with pytest.raises(WebhookVerificationException, match=f"Falta el header {empty}."):
        verify_at(OFFICIAL_TIMESTAMP, headers, OFFICIAL_BODY)


def test_header_names_are_case_insensitive():
    headers = {
        "Webhook-Id": OFFICIAL_ID,
        "WEBHOOK-TIMESTAMP": str(OFFICIAL_TIMESTAMP),
        "Webhook-Signature": OFFICIAL_SIGNATURE,
    }

    verify_at(OFFICIAL_TIMESTAMP, headers, OFFICIAL_BODY)


class FrameworkHeaders(Mapping):
    """Headers como los de Django (``request.headers``) o Starlette: un Mapping que no es dict, con nombres en Title-Case."""

    def __init__(self, values: dict) -> None:
        self._values = {name.title(): value for name, value in values.items()}

    def __getitem__(self, name: str) -> str:
        return self._values[name.title()]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)


class WerkzeugLikeHeaders:
    """Headers como los de Flask (werkzeug): sin ser un Mapping, iteran pares (nombre, valor) y tienen ``items()``."""

    def __init__(self, values: dict) -> None:
        self._pairs = [(name.title(), value) for name, value in values.items()]

    def __iter__(self) -> Iterator[tuple]:
        return iter(self._pairs)

    def items(self) -> list:
        return list(self._pairs)


def test_a_framework_headers_mapping_that_is_not_a_dict_verifies():
    verify_at(OFFICIAL_TIMESTAMP, FrameworkHeaders(official_headers()), OFFICIAL_BODY)


def test_flask_like_headers_with_items_verify():
    verify_at(OFFICIAL_TIMESTAMP, WerkzeugLikeHeaders(official_headers()), OFFICIAL_BODY)  # type: ignore[arg-type]


# --- Secretos ---


def test_a_secret_without_the_whsec_prefix_verifies():
    verify_at(OFFICIAL_TIMESTAMP, official_headers(), OFFICIAL_BODY, OFFICIAL_SECRET[len("whsec_"):])


def test_any_of_several_secrets_verifies_during_a_rotation():
    other_secret = generate_secret()

    verify_at(OFFICIAL_TIMESTAMP, official_headers(), OFFICIAL_BODY, [other_secret, OFFICIAL_SECRET])
    with pytest.raises(WebhookVerificationException, match="Ninguna firma"):
        verify_at(OFFICIAL_TIMESTAMP, official_headers(), OFFICIAL_BODY, [other_secret])


@pytest.mark.parametrize(
    "secret",
    [
        "",
        "whsec_",
        "whsec_%%no-es-base64%%",
        pytest.param("whsec_MfKQ9r8GKYqrTwjUPD8ILPZIo2LaLaS", id="truncado"),
        pytest.param("whsec_MfKQ9r8GKYqrTwjUPD8ILPZIo2LaLaSw\n", id="salto-de-linea-final"),
        pytest.param("whsec_MfKQ9r8GKYqrTwjU PD8ILPZIo2LaLaSw", id="espacio-interno"),
    ],
)
def test_a_malformed_secret_is_refused_as_a_configuration_error(secret):
    with pytest.raises(ValueError, match="secreto de firma") as raised:
        verify_at(OFFICIAL_TIMESTAMP, official_headers(), OFFICIAL_BODY, secret)
    assert not isinstance(raised.value, WebhookVerificationException)


def test_a_malformed_secret_in_a_list_names_its_position_without_its_value():
    malformed = "whsec_%%no-es-base64%%"

    with pytest.raises(ValueError, match="posición 1") as in_list:
        webhooks.verify(official_headers(), OFFICIAL_BODY, [OFFICIAL_SECRET, malformed])
    assert "no-es-base64" not in str(in_list.value)
    # Sin causa ni contexto encadenado: el error interno de base64 llevaría el secreto en las variables de su rastro.
    assert in_list.value.__cause__ is None and in_list.value.__context__ is None

    with pytest.raises(TypeError, match="posición 1"):
        webhooks.verify(official_headers(), OFFICIAL_BODY, [OFFICIAL_SECRET, None])  # type: ignore[list-item]

    with pytest.raises(ValueError) as single:
        webhooks.verify(official_headers(), OFFICIAL_BODY, malformed)
    assert "no-es-base64" not in str(single.value)
    assert "posición" not in str(single.value)


def test_missing_arguments_and_an_empty_secret_list_are_refused():
    with pytest.raises(TypeError, match="headers"):
        webhooks.verify(None, OFFICIAL_BODY, OFFICIAL_SECRET)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="body"):
        webhooks.verify(official_headers(), None, OFFICIAL_SECRET)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="secret"):
        webhooks.verify(official_headers(), OFFICIAL_BODY, None)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="al menos un secreto"):
        webhooks.verify(official_headers(), OFFICIAL_BODY, [])


def test_the_public_function_verifies_against_the_current_time():
    timestamp = int(time.time())
    headers = official_headers(
        timestamp=str(timestamp), signature=sign(OFFICIAL_ID, timestamp, OFFICIAL_BODY, OFFICIAL_SECRET)
    )

    assert isinstance(webhooks.verify(headers, OFFICIAL_BODY, OFFICIAL_SECRET), WebhookEvent)
    assert isinstance(webhooks.verify(headers, OFFICIAL_BODY, [OFFICIAL_SECRET]), WebhookEvent)
    with pytest.raises(WebhookVerificationException, match="difiere"):
        webhooks.verify(official_headers(), OFFICIAL_BODY, OFFICIAL_SECRET)


# --- El secreto no queda expuesto ---

# Sentry y otros rastreadores capturan las variables locales de cada marco y solo tapan las que se llaman "secret".
_SECRET_LOCAL = re.compile(r"^\s+secret = ")


def formatted_failure(call: Callable[[], object]) -> str:
    """El rastro de la excepción de ``call`` con las variables locales de cada marco, sin las líneas ``secret = …``."""
    try:
        call()
    except Exception as error:
        formatted = "".join(traceback.TracebackException.from_exception(error, capture_locals=True).format())
        return "\n".join(line for line in formatted.splitlines() if not _SECRET_LOCAL.match(line))
    raise AssertionError("La verificación debía fallar.")


def exposures(formatted: str, secret: str) -> list:
    """Las formas del secreto (su base64 y los bytes de la llave) que aparecen en ``formatted``."""
    encoded = secret[len("whsec_"):]
    return [text for text in (encoded, repr(base64.b64decode(encoded))) if text in formatted]


def test_the_signing_key_object_does_not_reveal_the_key():
    secret = generate_secret()

    key = webhooks._decode_secret(secret, "El secreto de firma")

    assert repr(key) == "***" and str(key) == "***"
    assert not hasattr(key, "__dict__")


def test_a_failed_signature_check_does_not_expose_the_secret_in_captured_locals():
    secret = generate_secret()

    formatted = formatted_failure(lambda: verify_at(OFFICIAL_TIMESTAMP, official_headers(), OFFICIAL_BODY, [secret]))

    assert "Ninguna firma" in formatted
    assert exposures(formatted, secret) == []


# Global y no local, para que el rastro solo lo pueda mostrar si el SDK lo deja en una variable suya.
MALFORMED_SECRET = "whsec_%%no-es-base64%%"


def test_a_malformed_secret_does_not_expose_any_secret_in_captured_locals():
    secret = generate_secret()

    formatted = formatted_failure(lambda: webhooks.verify(official_headers(), OFFICIAL_BODY, [secret, MALFORMED_SECRET]))

    assert "posición 1" in formatted
    assert exposures(formatted, secret) == []
    assert "no-es-base64" not in formatted
