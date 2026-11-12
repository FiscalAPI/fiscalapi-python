"""Acceso al portal de una persona (``login_enabled``) y contraseña opcional.

Los mismos escenarios viven en los SDK de .NET, Node, PHP y Java: en None, ninguno de los dos viaja, así que crear una
persona sin contraseña no manda ``password`` y un update que no fija ``login_enabled`` no cambia el acceso;
``login_enabled=False`` sí viaja.
"""
from fiscalapi import Person

BASE_URL = "https://sdk-tests.fiscalapi.invalid/api/v4"
PERSON_ID = "4b1c2d3e-0000-4000-8000-000000000002"

PERSON_RESPONSE = {
    "data": {"id": PERSON_ID, "legalName": "Persona de Prueba", "email": "someone@somewhere.com", "loginEnabled": True, "isOwner": False},
    "succeeded": True,
    "message": "",
    "details": "",
    "httpStatusCode": 200,
}


def new_person(**fields) -> Person:
    return Person(legal_name="Persona de Prueba", email="someone@somewhere.com", **fields)


def sent_body(fake_api) -> dict:
    assert len(fake_api.requests) == 1
    return fake_api.requests[0]["json"]


def test_crear_sin_contrasena_no_envia_password_ni_login_enabled(client, fake_api):
    fake_api.respond_with(PERSON_RESPONSE)

    client.people.create(new_person())

    assert sent_body(fake_api) == {"legalName": "Persona de Prueba", "email": "someone@somewhere.com"}


def test_crear_con_acceso_al_portal_envia_password_y_login_enabled(client, fake_api):
    fake_api.respond_with(PERSON_RESPONSE)

    client.people.create(new_person(password="YourStrongPassword123!", login_enabled=True))

    assert sent_body(fake_api) == {
        "legalName": "Persona de Prueba",
        "email": "someone@somewhere.com",
        "password": "YourStrongPassword123!",
        "loginEnabled": True,
    }


def test_actualizar_sin_login_enabled_no_lo_envia(client, fake_api):
    fake_api.respond_with(PERSON_RESPONSE)

    client.people.update(new_person(id=PERSON_ID))

    assert fake_api.requests[0]["method"] == "PUT"
    assert fake_api.requests[0]["url"] == f"{BASE_URL}/people/{PERSON_ID}"
    assert "loginEnabled" not in sent_body(fake_api)


def test_actualizar_con_login_enabled_en_false_lo_envia_como_false(client, fake_api):
    fake_api.respond_with(PERSON_RESPONSE)

    client.people.update(new_person(id=PERSON_ID, login_enabled=False))

    assert sent_body(fake_api)["loginEnabled"] is False


def test_la_respuesta_trae_el_acceso_efectivo(client, fake_api):
    fake_api.respond_with(PERSON_RESPONSE)

    response = client.people.get_by_id(PERSON_ID)

    assert response.data.login_enabled is True
    assert fake_api.requested_urls[-1] == f"{BASE_URL}/people/{PERSON_ID}"
