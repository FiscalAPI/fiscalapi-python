"""Tolerancia del SDK a respuestas del API con valores y campos que el SDK todavía no modela.

Son pruebas de caracterización: fijan el comportamiento ACTUAL. Una prueba cuyo nombre incluye ``fixed_by``
o ``exposed_by`` documenta un defecto conocido; se invierte cuando el SDK agregue el crédito de ticket y
``availableTicketBalance``. Los casos son:

1. una transacción de timbres con ``creditType: 3`` (créditos de ticket);
2. una persona con el campo nuevo ``availableTicketBalance``;
3. propiedades desconocidas en la envoltura, en ``data`` y en objetos anidados;
4. ``globalInformation`` en la respuesta de una factura.
"""
from decimal import Decimal

import pytest
from pydantic import ValidationError

from fiscalapi import CreditType, GlobalInformation

TICKET_CREDIT_TYPE = 3


def _ticket_credit_type_errors(error: ValidationError) -> list:
    return [e for e in error.errors() if e["loc"][-1] == "creditType" and e["input"] == TICKET_CREDIT_TYPE]


# 1. creditType: 3


def test_stamp_list_with_credit_type_3_raises_validation_error__fixed_by_SDK_012(client, fake_api, api_json):
    fake_api.respond_with(api_json("stamps-page-credit-type-3.json"))

    with pytest.raises(ValidationError) as raised:
        client.stamps.get_list(1, 10)

    assert len(_ticket_credit_type_errors(raised.value)) == 1
    assert raised.value.error_count() == 1


def test_stamp_by_id_with_credit_type_3_raises_validation_error__fixed_by_SDK_012(client, fake_api, api_json):
    fake_api.respond_with(api_json("stamp-credit-type-3.json"))

    with pytest.raises(ValidationError) as raised:
        client.stamps.get_by_id("8d0f6a52-6f1e-4c3a-9a10-000000000103")

    assert len(_ticket_credit_type_errors(raised.value)) == 1
    assert raised.value.error_count() == 1


def test_stamp_list_without_the_credit_type_3_item_deserializes_known_credit_types(client, fake_api, api_json):
    page = api_json("stamps-page-credit-type-3.json")
    page["data"]["items"] = [i for i in page["data"]["items"] if i["creditType"] != TICKET_CREDIT_TYPE]
    fake_api.respond_with(page)

    response = client.stamps.get_list(1, 10)

    assert response.succeeded is True
    assert [t.credit_type for t in response.data.items] == [CreditType.STAMP, CreditType.VALIDATION]
    assert response.data.total_count == 3
    assert fake_api.requested_urls == ["https://sdk-tests.fiscalapi.invalid/api/v4/stamps?pageNumber=1&pageSize=10"]


# 2. availableTicketBalance


def test_person_with_available_ticket_balance_deserializes_and_drops_the_field__exposed_by_SDK_012(
    client, fake_api, api_json
):
    fake_api.respond_with(api_json("person-ticket-balance.json"))

    response = client.people.get_by_id("4b1c2d3e-0000-4000-8000-000000000001")

    person = response.data
    assert response.succeeded is True
    assert person.available_balance == Decimal("100")
    assert person.committed_balance == Decimal("0")
    assert person.available_validation_balance == 50
    assert not hasattr(person, "available_ticket_balance")
    assert "availableTicketBalance" not in person.model_dump(by_alias=True)


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
