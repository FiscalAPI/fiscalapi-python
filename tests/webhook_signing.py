"""La firma de WebhookSigner de fapi-back, copiada sin depender del back, para firmar entregas en las pruebas.

HMAC-SHA256 sobre ``{id}.{timestamp}.{body}`` en UTF-8 con los bytes base64 del secreto (sin ``whsec_``); una firma
``v1,<base64>`` por secreto, unidas por un espacio y en el orden recibido (el vigente primero).
"""
import base64
import hashlib
import hmac
import secrets as random_secrets
from typing import Union

SECRET_PREFIX = "whsec_"


def generate_secret() -> str:
    """Un secreto como WebhookSecret.Generate del back: ``whsec_`` + 32 bytes aleatorios en base64."""
    return SECRET_PREFIX + base64.b64encode(random_secrets.token_bytes(32)).decode("ascii")


def sign(event_id: str, timestamp: int, body: Union[str, bytes], *secrets: str) -> str:
    """El header ``webhook-signature`` de una entrega; un cuerpo ``str`` se firma con UTF-8 tolerante (surrogatepass)
    para poder firmar también un cuerpo que el SDK debe rechazar."""
    body_bytes = body if isinstance(body, bytes) else body.encode("utf-8", "surrogatepass")
    content = f"{event_id}.{timestamp}.".encode("utf-8") + body_bytes
    return " ".join(
        "v1," + base64.b64encode(hmac.new(_key(secret), content, hashlib.sha256).digest()).decode("ascii")
        for secret in secrets
    )


def headers(event_id: str, timestamp: int, body: Union[str, bytes], *secrets: str) -> dict:
    """Los tres headers de Standard Webhooks de una entrega firmada con ``secrets``."""
    return {
        "webhook-id": event_id,
        "webhook-timestamp": str(timestamp),
        "webhook-signature": sign(event_id, timestamp, body, *secrets),
    }


def _key(secret: str) -> bytes:
    encoded = secret[len(SECRET_PREFIX):] if secret.startswith(SECRET_PREFIX) else secret
    return base64.b64decode(encoded)
