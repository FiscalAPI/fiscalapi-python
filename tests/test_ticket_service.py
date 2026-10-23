"""Servicio de tickets de Auto CFDI (POST/GET/DELETE /api/v4/tickets).

Los mismos escenarios viven en los SDK de .NET, Node.js, PHP y Java: el cuerpo exacto de la ingesta y el header
Idempotency-Key solo si se pasa; la respuesta 201 de la ingesta; el 409 y el 422 con la forma de error del SDK
(``details`` con el texto del API y ``data`` en None); la query de la lista con ``status`` repetido; el detalle con y sin
``details``; el código; la cancelación con DELETE, y un estado que el SDK no conoce, conservado como texto.
"""
import copy
from datetime import date, datetime
from decimal import Decimal

import pytest

from fiscalapi import (
    Ticket,
    TicketActorType,
    TicketEventType,
    TicketIssuer,
    TicketItem,
    TicketItemTax,
    TicketListFilters,
    TicketStatus,
)

BASE_URL = "https://sdk-tests.fiscalapi.invalid/api/v4/tickets"
ISSUER_ID = "4b1c2d3e-0000-4000-8000-000000000002"
TICKET_ID = "9f8e7d6c-0000-4000-8000-0000000000a1"
GLOBAL_INVOICE_ID = "7c1d2e3f-0000-4000-8000-0000000000b2"
IDEMPOTENCY_KEY = "550e8400-e29b-41d4-a716-446655440000"

INGESTED = {
    "id": TICKET_ID,
    "ticketCode": "K7M2Q9X4TB3H",
    "qrUrl": "https://portal.fiscalapi.com/t/K7M2Q9X4TB3H",
    "status": "pending",
    "selfInvoiceEligible": True,
    "eligibleUntil": "2026-10-31T23:59:59.000",
    "subtotal": 100,
    "totalTransferredTaxes": 16,
    "totalWithheldTaxes": 0,
    "total": 116,
}

SUMMARY = {
    "id": TICKET_ID,
    "personId": ISSUER_ID,
    "folio": "F-1001",
    "series": "A",
    "paymentDate": "2026-09-01T00:00:00.000",
    "paymentFormCode": "01",
    "currencyCode": "MXN",
    "exchangeRate": None,
    "expeditionZipCode": "06000",
    "subtotal": 100,
    "totalTransferredTaxes": 16,
    "totalWithheldTaxes": 0,
    "total": 116,
    "status": "pending",
    "selfInvoiceEligible": True,
    "eligibleUntil": "2026-09-30T23:59:59.000",
    "invoiceId": None,
    "globalInvoiceId": None,
    "createdAt": "2026-09-01T00:05:00.000",
}

DETAIL = {
    **SUMMARY,
    "status": "cancelled",
    "currencyCode": "USD",
    "exchangeRate": 17.25,
    "selfInvoiceEligible": False,
    "eligibleUntil": None,
    "items": [{
        "itemCode": "50202306", "itemSku": "SKU-1", "quantity": 1, "unitOfMeasurementCode": "H87",
        "description": "Refresco", "unitPrice": 100, "discount": 0, "taxObjectCode": "02",
        "itemTaxes": [{"taxCode": "002", "taxTypeCode": "Tasa", "taxRate": 0.16, "taxFlagCode": "T"}],
    }],
    "events": [
        {"type": "ingested", "occurredAt": "2026-09-01T00:05:00.000", "actorType": "tenant", "invoiceId": None},
        {"type": "cancelled", "occurredAt": "2026-09-01T01:00:00.000", "actorType": "tenant", "invoiceId": None},
    ],
}

# El cuerpo exacto que recibe el API: nombres camelCase, decimales tal cual (pydantic los serializa como texto) y sin
# los miembros que quedaron en None.
EXPECTED_CREATE_BODY = {
    "issuer": {"id": ISSUER_ID},
    "folio": "F-1001",
    "series": "A",
    "paymentDate": "2026-10-15T12:30:00",
    "paymentFormCode": "01",
    "currencyCode": "MXN",
    "expeditionZipCode": "06000",
    "total": "116.00",
    "items": [{
        "itemCode": "50202306",
        "itemSku": "SKU-1",
        "quantity": "1.5",
        "unitOfMeasurementCode": "H87",
        "description": "Refresco",
        "unitPrice": "66.666667",
        "discount": "0.00",
        "taxObjectCode": "02",
        "itemTaxes": [{"taxCode": "002", "taxTypeCode": "Tasa", "taxRate": "0.160000", "taxFlagCode": "T"}],
    }],
}


def _ok(data, status: int = 200) -> dict:
    return {"data": data, "succeeded": True, "message": "", "details": "", "httpStatusCode": status}


def _new_ticket() -> Ticket:
    return Ticket(
        issuer=TicketIssuer(id=ISSUER_ID),
        folio="F-1001",
        series="A",
        payment_date=datetime(2026, 10, 15, 12, 30, 0),
        payment_form_code="01",
        currency_code="MXN",
        expedition_zip_code="06000",
        total=Decimal("116.00"),
        items=[TicketItem(
            item_code="50202306",
            item_sku="SKU-1",
            quantity=Decimal("1.5"),
            unit_of_measurement_code="H87",
            description="Refresco",
            unit_price=Decimal("66.666667"),
            discount=Decimal("0.00"),
            tax_object_code="02",
            item_taxes=[TicketItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T")],
        )],
    )


# a. Cuerpo e Idempotency-Key

def test_create_posts_the_exact_contract_with_the_idempotency_key_header(client, fake_api):
    fake_api.respond_with(_ok(INGESTED, 201), status_code=201)

    client.tickets.create(_new_ticket(), IDEMPOTENCY_KEY)

    [request] = fake_api.requests
    assert request["method"] == "POST"
    assert request["url"] == BASE_URL
    assert request["json"] == EXPECTED_CREATE_BODY
    assert request["headers"]["Idempotency-Key"] == IDEMPOTENCY_KEY


def test_create_without_a_key_does_not_send_the_idempotency_key_header(client, fake_api):
    fake_api.respond_with(_ok(INGESTED, 201), status_code=201)

    client.tickets.create(_new_ticket())

    [request] = fake_api.requests
    assert request["json"] == EXPECTED_CREATE_BODY
    assert "Idempotency-Key" not in request["headers"]


# b. Respuesta de la ingesta: la repetición con la misma llave de idempotencia devuelve esta misma 201

def test_create_reads_the_new_ticket_with_its_shape(client, fake_api):
    fake_api.respond_with(_ok(INGESTED, 201), status_code=201)

    response = client.tickets.create(_new_ticket(), IDEMPOTENCY_KEY)

    assert response.succeeded is True
    assert response.http_status_code == 201
    assert response.error_data is None
    ingested = response.data
    assert ingested.id == TICKET_ID
    assert ingested.ticket_code == "K7M2Q9X4TB3H"
    assert ingested.qr_url == "https://portal.fiscalapi.com/t/K7M2Q9X4TB3H"
    assert ingested.status is TicketStatus.PENDING
    assert ingested.self_invoice_eligible is True
    assert ingested.eligible_until == datetime(2026, 10, 31, 23, 59, 59)
    assert (ingested.subtotal, ingested.total_transferred_taxes, ingested.total_withheld_taxes, ingested.total) == (
        Decimal("100"), Decimal("16"), Decimal("0"), Decimal("116"))


def test_a_duplicate_folio_is_409_with_the_api_details_and_existing_ticket_id_in_error_data(client, fake_api):
    fake_api.respond_with({
        "data": {"existingTicketId": TICKET_ID},
        "succeeded": False,
        "message": "Sorry, it's not me, it's you.",
        "details": "Ya hay un ticket activo con esa serie y folio para el emisor: 'data.existingTicketId' es el ticket que lo tiene. Para volver a ingerirlo, cancela ese ticket primero.",
        "httpStatusCode": 409,
    }, status_code=409)

    response = client.tickets.create(_new_ticket())

    assert response.succeeded is False
    assert response.http_status_code == 409
    assert response.message == "Sorry, it's not me, it's you."
    assert response.details.startswith("Ya hay un ticket activo con esa serie y folio para el emisor")
    assert response.data is None
    assert response.error_data == {"existingTicketId": TICKET_ID}


def test_a_total_mismatch_is_422_with_the_api_details_and_the_totals_in_error_data(client, fake_api):
    fake_api.respond_with({
        "data": {"expectedTotal": 116.01, "computedTotal": 116},
        "succeeded": False,
        "message": "Sorry, it's not me, it's you.",
        "details": "'total' no cuadra al centavo con el total calculado de los conceptos e impuestos: 'data.expectedTotal' es el enviado y 'data.computedTotal' el calculado.",
        "httpStatusCode": 422,
    }, status_code=422)

    response = client.tickets.create(_new_ticket())

    assert response.succeeded is False
    assert response.http_status_code == 422
    assert response.details.startswith("'total' no cuadra al centavo")
    assert response.data is None
    assert response.error_data == {"expectedTotal": 116.01, "computedTotal": 116}


def test_an_error_without_data_leaves_error_data_none(client, fake_api):
    fake_api.respond_with({"data": None, "succeeded": False, "message": "Sorry, it's not me, it's you.",
                           "details": "No existe el ticket.", "httpStatusCode": 404}, status_code=404)

    response = client.tickets.get_by_id(TICKET_ID)

    assert response.succeeded is False
    assert response.http_status_code == 404
    assert response.error_data is None


# c. Lista con filtros

def test_get_list_sends_every_filter_repeating_status(client, fake_api):
    fake_api.respond_with(_ok({"items": [SUMMARY], "pageNumber": 2, "totalPages": 3, "totalCount": 21,
                               "hasPreviousPage": True, "hasNextPage": True}))

    response = client.tickets.get_list(TicketListFilters(
        status=[TicketStatus.PENDING, TicketStatus.INVOICED],
        person_id=ISSUER_ID,
        from_=date(2026, 9, 1),
        to=date(2026, 9, 30),
        page_number=2,
        page_size=50,
    ))

    [request] = fake_api.requests
    assert request["method"] == "GET"
    assert request["url"] == (
        f"{BASE_URL}?status=pending&status=invoiced&personId={ISSUER_ID}&from=2026-09-01&to=2026-09-30"
        "&pageNumber=2&pageSize=50"
    )
    page = response.data
    assert (page.page_number, page.total_pages, page.total_count) == (2, 3, 21)
    [ticket] = page.items
    assert ticket.person_id == ISSUER_ID
    assert ticket.payment_date == datetime(2026, 9, 1)
    assert ticket.status is TicketStatus.PENDING
    assert ticket.items is None and ticket.events is None


def test_get_list_sends_details_and_global_invoice_id_when_assigned(client, fake_api):
    fake_api.respond_with(_ok({"items": [], "pageNumber": 1, "totalPages": 0, "totalCount": 0,
                               "hasPreviousPage": False, "hasNextPage": False}))

    client.tickets.get_list(TicketListFilters(details=True, global_invoice_id=GLOBAL_INVOICE_ID))

    assert fake_api.requests[0]["url"] == f"{BASE_URL}?details=true&globalInvoiceId={GLOBAL_INVOICE_ID}"


def test_get_list_does_not_send_details_when_false(client, fake_api):
    fake_api.respond_with(_ok({"items": [], "pageNumber": 1, "totalPages": 0, "totalCount": 0,
                               "hasPreviousPage": False, "hasNextPage": False}))

    client.tickets.get_list(TicketListFilters(details=False))

    assert fake_api.requests[0]["url"] == BASE_URL


def test_get_list_without_filters_sends_no_query(client, fake_api):
    fake_api.respond_with(_ok({"items": [], "pageNumber": 1, "totalPages": 0, "totalCount": 0,
                               "hasPreviousPage": False, "hasNextPage": False}))

    client.tickets.get_list()

    assert fake_api.requests[0]["url"] == BASE_URL


# d. Detalle

def test_get_by_id_without_details_does_not_ask_for_them(client, fake_api):
    fake_api.respond_with(_ok(SUMMARY))

    response = client.tickets.get_by_id(TICKET_ID)

    assert fake_api.requests[0]["url"] == f"{BASE_URL}/{TICKET_ID}"
    assert response.data.id == TICKET_ID
    assert response.data.items is None


def test_get_by_id_with_details_reads_items_and_events(client, fake_api):
    fake_api.respond_with(_ok(DETAIL))

    response = client.tickets.get_by_id(TICKET_ID, details=True)

    assert fake_api.requests[0]["url"] == f"{BASE_URL}/{TICKET_ID}?details=true"
    ticket = response.data
    assert ticket.status is TicketStatus.CANCELLED
    assert ticket.exchange_rate == Decimal("17.25")
    [item] = ticket.items
    assert (item.item_code, item.item_sku, item.quantity, item.unit_price, item.discount) == (
        "50202306", "SKU-1", Decimal("1"), Decimal("100"), Decimal("0"))
    [tax] = item.item_taxes
    assert (tax.tax_code, tax.tax_type_code, tax.tax_rate, tax.tax_flag_code) == ("002", "Tasa", Decimal("0.16"), "T")
    assert [event.type for event in ticket.events] == [TicketEventType.INGESTED, TicketEventType.CANCELLED]
    assert all(event.actor_type is TicketActorType.TENANT for event in ticket.events)
    assert ticket.events[1].occurred_at == datetime(2026, 9, 1, 1, 0, 0)


# e. Código

def test_get_code_reads_the_code_and_the_qr_url(client, fake_api):
    fake_api.respond_with(_ok({"ticketCode": "K7M2Q9X4TB3H", "qrUrl": "https://portal.fiscalapi.com/t/K7M2Q9X4TB3H"}))

    response = client.tickets.get_code(TICKET_ID)

    assert fake_api.requests[0]["method"] == "GET"
    assert fake_api.requests[0]["url"] == f"{BASE_URL}/{TICKET_ID}/code"
    assert (response.data.ticket_code, response.data.qr_url) == (
        "K7M2Q9X4TB3H", "https://portal.fiscalapi.com/t/K7M2Q9X4TB3H")


# f. Cancelación

def test_cancel_uses_delete(client, fake_api):
    fake_api.respond_with(_ok(True))

    response = client.tickets.cancel(TICKET_ID)

    [request] = fake_api.requests
    assert request["method"] == "DELETE"
    assert request["url"] == f"{BASE_URL}/{TICKET_ID}"
    assert request["json"] is None
    assert response.data is True


# g. Valores que el SDK no conoce

def test_get_by_id_keeps_a_status_event_type_and_actor_type_that_the_sdk_does_not_know(client, fake_api):
    body = copy.deepcopy(DETAIL)
    body["status"] = "unknownState"
    body["events"] = [{"type": "unknownEvent", "occurredAt": "2026-09-01T00:05:00.000", "actorType": "unknownActor",
                       "invoiceId": None}]
    fake_api.respond_with(_ok(body))

    response = client.tickets.get_by_id(TICKET_ID, details=True)

    assert response.succeeded is True
    assert response.data.status == "unknownState"
    [event] = response.data.events
    assert (event.type, event.actor_type) == ("unknownEvent", "unknownActor")


@pytest.mark.parametrize("ticket_id", ["", " "])
def test_every_call_by_id_rejects_a_missing_id_without_calling_the_api(client, fake_api, ticket_id):
    for call in (client.tickets.get_by_id, client.tickets.get_code, client.tickets.cancel):
        with pytest.raises(ValueError, match="Se requiere el id del ticket."):
            call(ticket_id)
    assert fake_api.requests == []
