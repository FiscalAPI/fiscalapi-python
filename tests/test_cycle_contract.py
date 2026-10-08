"""Cambios de código del SDK en el ciclo de deuda técnica 2 (Fase III, C22).

Los escenarios 1 a 3 viven también en los SDK de .NET, Node.js, PHP y Java (DEC-136), cuando el cambio aplica a cada uno:

1. persona: ``valid_to`` de solo lectura y ``committed_balance`` heredado; ``capital_regime``, ``stripeCustomerId`` y
   ``subscriptionStatus`` fuera del modelo (SDK-043, SDK-044);
2. certificados: ``tin`` opcional al subir (SDK-045) y ``file_type`` 2 y 3 de la FIEL (SDK-058);
3. certificados sin ``update()``: el API retiró PUT tax-files (SDK-051).

Los escenarios 4 y 5 son solo de Python: el SDK deja de restringir con ``Literal`` las claves que valida el API y las
envía tal cual, como los otros SDK (SDK-044, SDK-050, SDK-058; DEC-163 H2).
"""
from datetime import datetime
from decimal import Decimal

import pytest

from fiscalapi import (
    BaseDto,
    CancelInvoiceRequest,
    InvoicePayment,
    Person,
    ProductTax,
    TaxCredential,
    TaxFile,
)
from fiscalapi.models.fiscalapi_models import ItemTax, LocalTax, PaidInvoiceTax

BASE_URL = "https://sdk-tests.fiscalapi.invalid/api/v4"
PERSON_ID = "4b1c2d3e-0000-4000-8000-000000000002"
TAX_FILE_ID = "7a1b2c3d-0000-4000-8000-0000000000f1"
BASE64_CER = "MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAw"
BASE64_KEY = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQG"

RETIRED_PERSON_KEYS = ("validTo", "capitalRegime", "CapitalRegime", "stripeCustomerId", "subscriptionStatus")


def _envelope(data) -> dict:
    return {"data": data, "succeeded": True, "message": "", "details": "", "httpStatusCode": 200}


# 1. Persona (SDK-043, SDK-044)


def test_person_from_response_reads_valid_to_and_committed_balance_and_drops_the_retired_fields(client, fake_api, api_json):
    fake_api.respond_with(api_json("person-valid-to.json"))

    response = client.people.get_by_id(PERSON_ID)

    person = response.data
    assert response.succeeded is True
    assert person.valid_to == datetime(2025, 7, 15, 10, 30)
    assert person.committed_balance == 0
    assert person.available_balance == 100
    assert "capital_regime" not in Person.model_fields
    dumped = person.model_dump(by_alias=True)
    for key in ("capitalRegime", "CapitalRegime", "stripeCustomerId", "subscriptionStatus"):
        assert key not in dumped


def test_person_create_sends_neither_valid_to_nor_the_retired_fields(client, fake_api, api_json):
    fake_api.respond_with(api_json("person-valid-to.json"))
    person = Person(legal_name="ESCUELA KEMPER URGATE", email="someone@example.com", password="UserPass123!", tin="EKU9003173C9")

    client.people.create(person)

    [request] = fake_api.requests
    assert request["method"] == "POST"
    assert request["url"] == f"{BASE_URL}/people"
    assert request["json"]["legalName"] == "ESCUELA KEMPER URGATE"
    for key in RETIRED_PERSON_KEYS:
        assert key not in request["json"]


# 2. Certificados: tin opcional (SDK-045) y file_type de la FIEL (SDK-058)


@pytest.mark.parametrize("file_type", [2, 3])
def test_tax_file_create_without_tin_sends_the_file_type_as_a_number_and_no_tin(client, fake_api, file_type):
    fake_api.respond_with(_envelope({"id": TAX_FILE_ID, "personId": PERSON_ID, "tin": "EKU9003173C9", "fileType": file_type, "sequence": 1}))
    tax_file = TaxFile(person_id=PERSON_ID, base64_file=BASE64_CER, file_type=file_type, password="12345678a")

    response = client.tax_files.create(tax_file)

    assert response.succeeded is True
    assert response.data.tin == "EKU9003173C9"
    [request] = fake_api.requests
    assert request["method"] == "POST"
    assert request["url"] == f"{BASE_URL}/tax-files"
    assert request["json"] == {"personId": PERSON_ID, "base64File": BASE64_CER, "fileType": file_type, "password": "12345678a"}


# 3. Certificados sin update() (SDK-051)


def test_tax_file_service_has_no_update(client):
    assert not hasattr(client.tax_files, "update")


def test_tax_file_delete_sends_delete_to_the_tax_file(client, fake_api):
    fake_api.respond_with(_envelope(True))

    response = client.tax_files.delete(TAX_FILE_ID)

    assert response.succeeded is True
    assert response.data is True
    [request] = fake_api.requests
    assert request["method"] == "DELETE"
    assert request["url"] == f"{BASE_URL}/tax-files/{TAX_FILE_ID}"
    assert request["json"] is None


# 4. Cancelación por valores: TaxCredential sin BaseDto (SDK-044) y motivo como texto (SDK-058)


@pytest.mark.parametrize("reason_code", ["02", "05"])
def test_cancel_by_values_sends_the_reason_code_as_is_and_only_the_credential_fields(client, fake_api, reason_code):
    fake_api.respond_with(_envelope({"base64CancellationAcknowledgement": "PD94", "invoiceUuids": {"UUID-1": "201"}}))
    request_model = CancelInvoiceRequest(
        invoice_uuid="UUID-1",
        tin="EKU9003173C9",
        cancellation_reason_code=reason_code,
        tax_credentials=[
            TaxCredential(base64_file=BASE64_CER, file_type=0),
            TaxCredential(base64_file=BASE64_KEY, file_type=1, password="12345678a"),
        ],
    )

    response = client.invoices.cancel(request_model)

    assert response.succeeded is True
    assert response.data.invoice_uuids == {"UUID-1": "201"}
    [request] = fake_api.requests
    assert request["method"] == "DELETE"
    assert request["url"] == f"{BASE_URL}/invoices"
    assert request["json"]["cancellationReasonCode"] == reason_code
    assert request["json"]["taxCredentials"] == [
        {"base64File": BASE64_CER, "fileType": 0},
        {"base64File": BASE64_KEY, "fileType": 1, "password": "12345678a"},
    ]


def test_tax_credential_is_not_a_base_dto():
    credential = TaxCredential(base64_file=BASE64_CER, file_type=0)

    assert not isinstance(credential, BaseDto)
    assert set(TaxCredential.model_fields) == {"base64_file", "file_type", "password"}
    assert credential.password is None


# 5. Claves de catálogo como texto: el SDK no las restringe, las valida el API (SDK-050, DEC-163 H2)


def test_catalog_keys_are_sent_as_is():
    product_tax = ProductTax(rate=Decimal("0.16"), tax_id="004", tax_flag_id="X", tax_type_id="Otro")
    person = Person(sat_tax_regime_id="699", sat_cfdi_use_id="Z99", user_type_id="U")

    assert product_tax.model_dump(mode="json", by_alias=True, exclude_none=True) == {
        "rate": "0.16",
        "taxId": "004",
        "taxFlagId": "X",
        "taxTypeId": "Otro",
    }
    assert person.model_dump(mode="json", by_alias=True, exclude_none=True) == {
        "satTaxRegimeId": "699",
        "satCfdiUseId": "Z99",
        "userTypeId": "U",
    }
    for model in (
        ItemTax(tax_flag_code="X"),
        PaidInvoiceTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.16"), tax_flag_code="X"),
        LocalTax(tax_flag_code="X"),
    ):
        assert model.model_dump(by_alias=True)["taxFlagCode"] == "X"


def test_invoice_payment_accepts_any_currency_code_and_defaults_to_mxn():
    common = dict(
        payment_date="2026-10-08T10:00:00",
        payment_form_code="03",
        amount=Decimal("100"),
        source_bank_tin="BSM970519DU8",
        source_bank_account="1234567891",
        target_bank_tin="BBA830831LJ2",
        target_bank_account="0123456789",
        paid_invoices=[],
    )

    assert InvoicePayment(currency_code="CAD", **common).model_dump(by_alias=True)["currencyCode"] == "CAD"
    assert InvoicePayment(**common).currency_code == "MXN"
