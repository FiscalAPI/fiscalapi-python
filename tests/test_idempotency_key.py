"""Llave de idempotencia opcional en crear factura y transferir timbres.

Con ``idempotency_key`` el SDK manda el header ``Idempotency-Key`` con ese valor, y sin ella no manda el header. La llave de idempotencia
no cambia el cuerpo de la petición. El SDK no genera ni reintenta la llave de idempotencia: solo la pasa.
"""
from fiscalapi import Invoice, InvoiceIssuer, StampTransactionParams

INVOICES_URL = "https://sdk-tests.fiscalapi.invalid/api/v4/invoices"
STAMPS_URL = "https://sdk-tests.fiscalapi.invalid/api/v4/stamps"
ISSUER_ID = "4b1c2d3e-0000-4000-8000-000000000002"
PERSON_ID = "96b46762-d246-4a67-a562-510a25dbafa9"
IDEMPOTENCY_KEY = "pos-01-F-1001"

CREATED_INVOICE = {"succeeded": True, "message": "OK", "data": {"id": "7c1d2e3f-0000-4000-8000-0000000000b2"}}
TRANSFERRED = {"succeeded": True, "message": "OK", "data": True}


def _invoice() -> Invoice:
    return Invoice(version_code="4.0", series="F", type_code="I", issuer=InvoiceIssuer(id=ISSUER_ID))


def _transfer() -> StampTransactionParams:
    return StampTransactionParams(from_person_id=ISSUER_ID, to_person_id=PERSON_ID, amount=10)


# Crear factura

def test_create_invoice_sends_the_idempotency_key_header(client, fake_api):
    fake_api.respond_with(CREATED_INVOICE)

    client.invoices.create(_invoice(), idempotency_key=IDEMPOTENCY_KEY)

    [request] = fake_api.requests
    assert request["method"] == "POST"
    assert request["url"] == INVOICES_URL
    assert request["headers"]["Idempotency-Key"] == IDEMPOTENCY_KEY


def test_create_invoice_without_a_key_does_not_send_the_header(client, fake_api):
    fake_api.respond_with(CREATED_INVOICE)

    client.invoices.create(_invoice())

    [request] = fake_api.requests
    assert "Idempotency-Key" not in request["headers"]


def test_create_invoice_key_does_not_change_the_body(client, fake_api):
    fake_api.respond_with(CREATED_INVOICE)

    client.invoices.create(_invoice())
    client.invoices.create(_invoice(), idempotency_key=IDEMPOTENCY_KEY)

    without_key, with_key = fake_api.requests
    assert with_key["json"] == without_key["json"]


# Transferir timbres

def test_transfer_stamps_sends_the_idempotency_key_header(client, fake_api):
    fake_api.respond_with(TRANSFERRED)

    client.stamps.transfer_stamps(_transfer(), idempotency_key=IDEMPOTENCY_KEY)

    [request] = fake_api.requests
    assert request["method"] == "POST"
    assert request["url"] == STAMPS_URL
    assert request["headers"]["Idempotency-Key"] == IDEMPOTENCY_KEY


def test_transfer_stamps_without_a_key_does_not_send_the_header(client, fake_api):
    fake_api.respond_with(TRANSFERRED)

    client.stamps.transfer_stamps(_transfer())

    [request] = fake_api.requests
    assert "Idempotency-Key" not in request["headers"]


def test_transfer_stamps_key_does_not_change_the_body(client, fake_api):
    fake_api.respond_with(TRANSFERRED)

    client.stamps.transfer_stamps(_transfer())
    client.stamps.transfer_stamps(_transfer(), idempotency_key=IDEMPOTENCY_KEY)

    without_key, with_key = fake_api.requests
    assert with_key["json"] == without_key["json"]
