"""Tolerancia del SDK a respuestas del API con valores y campos que el SDK modela o todavía no conoce.

Una prueba cuyo nombre incluye ``fixed_by`` o ``exposed_by`` documenta un defecto conocido que se invierte
cuando el SDK lo corrija. Los casos son:

1. transacciones con ``creditType: 3`` (``CreditType.TICKET``) y con un tipo de crédito que el SDK no conoce (99);
2. una persona con el saldo de créditos de ticket en ``balances``;
3. propiedades desconocidas en la envoltura, en ``data`` y en objetos anidados;
4. ``globalInformation`` en la respuesta de una factura.
"""
from decimal import Decimal

import pytest
from pydantic import ValidationError

from fiscalapi import CreditType, GlobalInformation, StampTransactionParams

TICKET_CREDIT_TYPE = 3
UNKNOWN_CREDIT_TYPE = 99
TICKET_TRANSACTION_ID = "8d0f6a52-6f1e-4c3a-9a10-000000000103"
PERSON_ID = "4b1c2d3e-0000-4000-8000-000000000001"


def _with_unknown_credit_type(page_or_stamp: dict) -> dict:
    """Cambia el creditType 3 de la transacción de tickets por un tipo que el SDK no conoce."""
    data = page_or_stamp["data"]
    transactions = data["items"] if "items" in data else [data]
    for transaction in transactions:
        if transaction["creditType"] == TICKET_CREDIT_TYPE:
            transaction["creditType"] = UNKNOWN_CREDIT_TYPE
    return page_or_stamp


# 1. creditType: 3 (TICKET) y un tipo desconocido


def test_stamp_list_reads_credit_type_3_as_ticket(client, fake_api, api_json):
    fake_api.respond_with(api_json("stamps-page-credit-type-3.json"))

    response = client.stamps.get_list(1, 10)

    credit_types = [t.credit_type for t in response.data.items]
    assert response.succeeded is True
    assert credit_types == [CreditType.STAMP, CreditType.VALIDATION, CreditType.TICKET]
    assert all(isinstance(c, CreditType) for c in credit_types)
    assert fake_api.requested_urls == ["https://sdk-tests.fiscalapi.invalid/api/v4/stamps?pageNumber=1&pageSize=10"]


def test_stamp_by_id_reads_credit_type_3_as_ticket(client, fake_api, api_json):
    fake_api.respond_with(api_json("stamp-credit-type-3.json"))

    response = client.stamps.get_by_id(TICKET_TRANSACTION_ID)

    assert response.succeeded is True
    assert response.data.credit_type is CreditType.TICKET
    assert response.data.amount == 25


def test_stamp_list_keeps_an_unknown_credit_type_as_its_number_without_failing(client, fake_api, api_json):
    fake_api.respond_with(_with_unknown_credit_type(api_json("stamps-page-credit-type-3.json")))

    response = client.stamps.get_list(1, 10)

    credit_types = [t.credit_type for t in response.data.items]
    assert response.succeeded is True
    assert credit_types == [CreditType.STAMP, CreditType.VALIDATION, UNKNOWN_CREDIT_TYPE]
    assert credit_types[0] is CreditType.STAMP
    assert type(credit_types[2]) is int
    assert response.data.items[2].model_dump(by_alias=True)["creditType"] == UNKNOWN_CREDIT_TYPE


def test_stamp_by_id_keeps_an_unknown_credit_type_as_its_number_without_failing(client, fake_api, api_json):
    fake_api.respond_with(_with_unknown_credit_type(api_json("stamp-credit-type-3.json")))

    response = client.stamps.get_by_id(TICKET_TRANSACTION_ID)

    assert response.succeeded is True
    assert response.data.credit_type == UNKNOWN_CREDIT_TYPE
    assert type(response.data.credit_type) is int
    assert response.data.amount == 25


def test_transfer_stamps_with_ticket_sends_credit_type_3(client, fake_api):
    fake_api.respond_with({"data": True, "succeeded": True, "message": "", "details": "", "httpStatusCode": 200})

    response = client.stamps.transfer_stamps(
        StampTransactionParams(from_person_id="1", to_person_id=PERSON_ID, amount=25, credit_type=CreditType.TICKET)
    )

    assert response.succeeded is True
    assert len(fake_api.requests) == 1
    assert fake_api.requests[0]["method"] == "POST"
    assert fake_api.requests[0]["url"] == "https://sdk-tests.fiscalapi.invalid/api/v4/stamps"
    assert fake_api.requests[0]["json"]["creditType"] == TICKET_CREDIT_TYPE


def test_stamp_list_without_the_credit_type_3_item_deserializes_known_credit_types(client, fake_api, api_json):
    page = api_json("stamps-page-credit-type-3.json")
    page["data"]["items"] = [i for i in page["data"]["items"] if i["creditType"] != TICKET_CREDIT_TYPE]
    fake_api.respond_with(page)

    response = client.stamps.get_list(1, 10)

    assert response.succeeded is True
    assert [t.credit_type for t in response.data.items] == [CreditType.STAMP, CreditType.VALIDATION]
    assert response.data.total_count == 3
    assert fake_api.requested_urls == ["https://sdk-tests.fiscalapi.invalid/api/v4/stamps?pageNumber=1&pageSize=10"]


# 2. Saldo de créditos de ticket en balances


def test_person_reads_the_ticket_balance_from_balances(client, fake_api, api_json):
    fake_api.respond_with(api_json("person-ticket-balance.json"))

    response = client.people.get_by_id(PERSON_ID)

    person = response.data
    assert response.succeeded is True
    assert person.available_balance == Decimal("100")
    assert person.committed_balance == Decimal("0")
    assert person.available_validation_balance == 50
    assert [(b.credit_type, b.available) for b in person.balances] == [
        (CreditType.STAMP, 100),
        (CreditType.VALIDATION, 50),
        (CreditType.TICKET, 25),
    ]


# 3. Propiedades desconocidas


def test_unknown_properties_on_a_stamp_transaction_are_ignored_and_known_fields_are_read(client, fake_api, api_json):
    stamp = api_json("stamp-credit-type-3.json")
    stamp["data"]["creditType"] = int(CreditType.VALIDATION)
    fake_api.respond_with(stamp)

    response = client.stamps.get_by_id("8d0f6a52-6f1e-4c3a-9a10-000000000103")

    transaction = response.data
    assert response.succeeded is True
    assert transaction.credit_type == CreditType.VALIDATION
    assert transaction.amount == 25
    assert transaction.from_person.legal_name == "FISCALAPI"
    assert "unknownScalarField" not in transaction.model_dump(by_alias=True)
    assert "unknownNestedField" not in transaction.from_person.model_dump(by_alias=True)


def test_unknown_properties_on_the_envelope_the_page_and_a_person_are_ignored(client, fake_api, api_json):
    fake_api.respond_with(api_json("person-ticket-balance.json"))

    response = client.people.get_by_id("4b1c2d3e-0000-4000-8000-000000000001")

    assert response.succeeded is True
    assert response.http_status_code == 200
    assert response.data.tin == "EKU9003173C9"
    assert "unknownEnvelopeField" not in response.model_dump(by_alias=True)
    assert "unknownObjectField" not in response.data.model_dump(by_alias=True)


# 4. globalInformation en la respuesta de una factura


def test_invoice_with_global_information_deserializes_it(client, fake_api, api_json):
    fake_api.respond_with(api_json("invoice-global-information.json"))

    response = client.invoices.get_by_id("3f2a9c1e-0b7d-4e55-9a61-2c8f0e4d7b10")

    assert response.succeeded is True
    assert response.data.global_information == GlobalInformation(periodicity_code="04", month_code="09", year=2026)
    assert response.data.issuer.tin == "EKU9003173C9"


def test_invoice_with_null_global_information_deserializes_it_as_none(client, fake_api, api_json):
    fake_api.respond_with(api_json("invoice-global-information-null.json"))

    response = client.invoices.get_by_id("3f2a9c1e-0b7d-4e55-9a61-2c8f0e4d7b10")

    assert response.succeeded is True
    assert response.data.global_information is None
    assert response.data.total == Decimal("1160")


def test_invoice_with_null_members_in_global_information_raises_validation_error__BE_008_must_not_emit_it(
    client, fake_api, api_json
):
    fake_api.respond_with(api_json("invoice-global-information-null-members.json"))

    with pytest.raises(ValidationError) as raised:
        client.invoices.get_by_id("3f2a9c1e-0b7d-4e55-9a61-2c8f0e4d7b10")

    failing_fields = sorted(e["loc"][-1] for e in raised.value.errors())
    assert failing_fields == ["monthCode", "periodicityCode", "year"]
