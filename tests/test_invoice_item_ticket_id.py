"""``InvoiceItem.ticket_id`` (Auto CFDI): liga cada concepto de la factura global a su ticket.

Los mismos escenarios viven en los SDK de .NET, Node.js, PHP y Java: sin ``ticket_id`` el cuerpo de ``invoices.create``
es exactamente el de la versión anterior; con él, cada concepto lleva ``"ticketId"`` (un ticket puede ir en varios
conceptos); un ``ticket_id`` en None nunca viaja, y el 409 de tickets no disponibles expone ``data.unavailableTickets``
en ``error_data``.
"""
import copy
import json
from datetime import datetime
from decimal import Decimal
from typing import Optional

import pytest

from fiscalapi import GlobalInformation, Invoice, InvoiceIssuer, InvoiceItem, InvoiceRecipient, ItemTax

INVOICES_URL = "https://sdk-tests.fiscalapi.invalid/api/v4/invoices"
ISSUER_ID = "4b1c2d3e-0000-4000-8000-000000000002"
TICKET_ID = "9f8e7d6c-0000-4000-8000-0000000000a1"
OTHER_TICKET_ID = "9f8e7d6c-0000-4000-8000-0000000000a2"

# Cuerpo que enviaba la versión anterior del SDK (sin ticket_id en InvoiceItem) para la misma global, en el orden de
# los campos del modelo.
PREVIOUS_PAYLOAD = (
    '{"versionCode": "4.0", "paymentFormCode": "01", "paymentMethodCode": "PUE", "currencyCode": "MXN", '
    '"typeCode": "I", "expeditionZipCode": "06000", "series": "G", "number": "1001", "date": "2026-10-01T10:00:00", '
    '"exportCode": "01", "issuer": {"id": "4b1c2d3e-0000-4000-8000-000000000002"}, "recipient": '
    '{"tin": "XAXX010101000", "legalName": "PUBLICO EN GENERAL", "zipCode": "06000", "taxRegimeCode": "616", '
    '"cfdiUseCode": "S01"}, "items": [{"itemCode": "01010101", "itemSku": "F-1001", "quantity": "1", '
    '"unitOfMeasurementCode": "ACT", "description": "Venta", "unitPrice": "100.00", "taxObjectCode": "02", '
    '"itemTaxes": [{"taxCode": "002", "taxTypeCode": "Tasa", "taxRate": "0.160000", "taxFlagCode": "T"}]}, '
    '{"itemCode": "01010101", "itemSku": "F-1001", "quantity": "1", "unitOfMeasurementCode": "ACT", '
    '"description": "Venta", "unitPrice": "50.00", "taxObjectCode": "02", "itemTaxes": [{"taxCode": "002", '
    '"taxTypeCode": "Tasa", "taxRate": "0.000000", "taxFlagCode": "T"}]}], "globalInformation": '
    '{"periodicityCode": "04", "monthCode": "09", "year": 2026}}'
)

UNAVAILABLE_TICKETS_DETAILS = (
    "Uno o más tickets ya no están disponibles para la factura global (solo entra un ticket en estado pending): "
    "'data.unavailableTickets' dice cuáles y su estado. No se cobró el timbre ni quedó tomado ningún ticket."
)


def concept(unit_price: str, tax_rate: str, ticket_id: Optional[str] = None) -> InvoiceItem:
    """Un concepto por grupo de impuestos del mismo ticket (IVA 16 % y 0 %)."""
    fields = dict(
        item_code="01010101",
        item_sku="F-1001",
        quantity=Decimal("1"),
        unit_of_measurement_code="ACT",
        description="Venta",
        unit_price=Decimal(unit_price),
        tax_object_code="02",
        item_taxes=[ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal(tax_rate), tax_flag_code="T")],
    )
    if ticket_id is not None:
        fields["ticket_id"] = ticket_id
    return InvoiceItem(**fields)


def global_invoice(items: list[InvoiceItem]) -> Invoice:
    return Invoice(
        version_code="4.0",
        series="G",
        number="1001",
        date=datetime(2026, 10, 1, 10, 0, 0),
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="06000",
        export_code="01",
        issuer=InvoiceIssuer(id=ISSUER_ID),
        recipient=InvoiceRecipient(
            tin="XAXX010101000",
            legal_name="PUBLICO EN GENERAL",
            zip_code="06000",
            tax_regime_code="616",
            cfdi_use_code="S01",
        ),
        global_information=GlobalInformation(periodicity_code="04", month_code="09", year=2026),
        items=items,
    )


CREATED = {
    "data": {"id": "9c1d2e3f-0000-4000-8000-0000000000a1", "uuid": "5F8C2D3E-1A2B-4C5D-8E9F-0A1B2C3D4E5F"},
    "succeeded": True,
    "message": "",
    "details": "",
    "httpStatusCode": 200,
}


@pytest.fixture(autouse=True)
def created(fake_api):
    fake_api.respond_with(copy.deepcopy(CREATED))


def sent_body(fake_api) -> dict:
    assert len(fake_api.requests) == 1
    request = fake_api.requests[0]
    assert (request["method"], request["url"]) == ("POST", INVOICES_URL)
    return request["json"]


def test_without_ticket_id_create_sends_exactly_the_previous_payload(client, fake_api):
    client.invoices.create(global_invoice([concept("100.00", "0.160000"), concept("50.00", "0.000000")]))

    assert json.dumps(sent_body(fake_api), ensure_ascii=False) == PREVIOUS_PAYLOAD


def test_a_ticket_id_set_to_none_is_omitted(client, fake_api):
    item = concept("100.00", "0.160000")
    item.ticket_id = None

    client.invoices.create(global_invoice([item]))

    assert "ticketId" not in sent_body(fake_api)["items"][0]


def test_with_ticket_id_each_item_carries_it_and_nothing_else_changes(client, fake_api):
    client.invoices.create(global_invoice([
        concept("100.00", "0.160000", TICKET_ID),
        concept("50.00", "0.000000", TICKET_ID),
    ]))

    expected = json.loads(PREVIOUS_PAYLOAD)
    for item in expected["items"]:
        item["ticketId"] = TICKET_ID
    assert sent_body(fake_api) == expected


def test_only_the_items_with_ticket_id_carry_it(client, fake_api):
    client.invoices.create(global_invoice([concept("100.00", "0.160000"), concept("50.00", "0.000000", OTHER_TICKET_ID)]))

    items = sent_body(fake_api)["items"]
    assert "ticketId" not in items[0]
    assert items[1]["ticketId"] == OTHER_TICKET_ID


def test_ticket_id_is_read_by_alias_and_by_name():
    assert InvoiceItem.model_validate({"ticketId": TICKET_ID}).ticket_id == TICKET_ID
    assert InvoiceItem(ticket_id=TICKET_ID).ticket_id == TICKET_ID


def test_unavailable_tickets_is_409_with_the_api_details_and_the_tickets_in_error_data(client, fake_api):
    unavailable = [{"ticketId": TICKET_ID, "status": "invoiced"}, {"ticketId": OTHER_TICKET_ID, "status": "globalizing"}]
    fake_api.respond_with({
        "data": {"unavailableTickets": copy.deepcopy(unavailable)},
        "succeeded": False,
        "message": "Sorry, it's not me, it's you.",
        "details": UNAVAILABLE_TICKETS_DETAILS,
        "httpStatusCode": 409,
    }, status_code=409)

    response = client.invoices.create(global_invoice([
        concept("100.00", "0.160000", TICKET_ID),
        concept("50.00", "0.000000", OTHER_TICKET_ID),
    ]))

    assert response.succeeded is False
    assert response.http_status_code == 409
    assert response.details == UNAVAILABLE_TICKETS_DETAILS
    assert response.data is None
    assert response.error_data == {"unavailableTickets": unavailable}
