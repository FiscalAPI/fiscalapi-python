"""GET /api/v4/people/{personId}/tax-files: lista de certificados (CSD y FIEL) de una persona, solo metadatos.

El API responde un arreglo no paginado en ``data``, sin ``base64File``, ``password``, ``createdAt`` ni ``updatedAt``.
"""
from datetime import datetime

from fiscalapi import TaxFile

PERSON_ID = "p1"
BASE_URL = "https://sdk-tests.fiscalapi.invalid/api/v4"

TAX_FILES_RESPONSE = {
    "data": [
        {"id": "a1", "personId": "p1", "tin": "EKU9003173C9", "fileType": 0,
         "validFrom": "2023-05-18T11:43:51", "validTo": "2027-05-18T11:43:51", "sequence": 1},
        {"id": "a2", "personId": "p1", "tin": "EKU9003173C9", "fileType": 1,
         "validFrom": "2023-05-18T11:43:51", "validTo": "2027-05-18T11:43:51", "sequence": 1},
    ],
    "succeeded": True,
    "message": "",
    "details": "",
    "httpStatusCode": 200,
}


def test_get_tax_files_pide_la_ruta_del_subrecurso_con_get(client, fake_api):
    fake_api.respond_with(TAX_FILES_RESPONSE)

    client.people.get_tax_files(PERSON_ID)

    assert fake_api.requests[-1]["method"] == "GET"
    assert fake_api.requested_urls[-1] == f"{BASE_URL}/people/{PERSON_ID}/tax-files"
    assert fake_api.requests[-1]["json"] is None


def test_get_tax_files_deserializa_la_lista_solo_con_metadatos(client, fake_api):
    fake_api.respond_with(TAX_FILES_RESPONSE)

    response = client.people.get_tax_files(PERSON_ID)

    assert response.succeeded is True
    assert response.http_status_code == 200
    assert len(response.data) == 2
    assert all(isinstance(item, TaxFile) for item in response.data)

    csd_cer, csd_key = response.data
    assert csd_cer.id == "a1"
    assert csd_cer.person_id == "p1"
    assert csd_cer.tin == "EKU9003173C9"
    assert csd_cer.file_type == 0
    assert csd_cer.valid_from == datetime(2023, 5, 18, 11, 43, 51)
    assert csd_cer.valid_to == datetime(2027, 5, 18, 11, 43, 51)
    assert csd_cer.sequence == 1

    assert csd_key.id == "a2"
    assert csd_key.file_type == 1


def test_get_tax_files_no_trae_archivo_ni_contrasena(client, fake_api):
    fake_api.respond_with(TAX_FILES_RESPONSE)

    response = client.people.get_tax_files(PERSON_ID)

    for item in response.data:
        assert item.base64_file is None
        assert item.password is None
        assert item.created_at is None
        assert item.updated_at is None
