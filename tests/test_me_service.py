"""GET /api/v4/me: la persona de la credencial con sus features y saldos, con los nombres del back.

Los mismos escenarios viven en los SDK de .NET, Node, PHP y Java.
"""
from fiscalapi import CreditBalance, MeInfo, MeService

BASE_URL = "https://sdk-tests.fiscalapi.invalid/api/v4"

ME_RESPONSE = {
    "data": {
        "id": "78d380fd-1b69-4e3c-8bc0-4f57737f7d5f",
        "legalName": "KARLA FUENTE NOLASCO",
        "tin": "FUNK671228PH6",
        "email": "persona@example.com",
        "tenantId": "102e5f13-e114-41dd-bea7-507fce177281",
        "environment": "Test",
        "isOwner": True,
        "features": {
            "isOwner": True,
            "roles": ["Owner"],
            "permissions": ["Invoices.Read", "Invoices.Issue"],
            "denied": {"Tickets.Create": {"missingFeatures": ["auto_cfdi"]}},
            "features": {"emision_cfdi": {"values": {}}, "descarga_cfdi": {"values": {"seats": 2}}},
            "subscription": {"status": "active", "isAvailable": True},
            "seatAssignments": [{"featureCode": "descarga_cfdi", "units": 1, "status": "Active"}],
        },
        "balances": [
            {"creditType": 1, "available": 7},
            {"creditType": 2, "available": 3},
        ],
    },
    "succeeded": True,
    "message": "",
    "details": "",
    "httpStatusCode": 200,
}


def test_me_get_hace_get_a_me_sin_cuerpo(client, fake_api):
    fake_api.respond_with(ME_RESPONSE)

    client.me.get()

    assert len(fake_api.requests) == 1
    assert fake_api.requests[0]["method"] == "GET"
    assert fake_api.requests[0]["url"] == f"{BASE_URL}/me"
    assert fake_api.requests[0]["json"] is None


def test_me_get_deserializa_la_persona_sus_features_y_sus_saldos(client, fake_api):
    fake_api.respond_with(ME_RESPONSE)

    response = client.me.get()
    info = response.data

    assert response.succeeded is True
    assert isinstance(info, MeInfo)
    assert info.id == "78d380fd-1b69-4e3c-8bc0-4f57737f7d5f"
    assert info.legal_name == "KARLA FUENTE NOLASCO"
    assert info.tin == "FUNK671228PH6"
    assert info.email == "persona@example.com"
    assert info.tenant_id == "102e5f13-e114-41dd-bea7-507fce177281"
    assert info.environment == "Test"
    assert info.is_owner is True

    features = info.features
    assert features.is_owner is True
    assert features.roles == ["Owner"]
    assert features.permissions == ["Invoices.Read", "Invoices.Issue"]
    assert features.denied["Tickets.Create"].missing_features == ["auto_cfdi"]
    assert features.features["emision_cfdi"].values == {}
    assert features.features["descarga_cfdi"].values["seats"] == 2
    assert features.subscription.status == "active"
    assert features.subscription.is_available is True
    assert len(features.seat_assignments) == 1
    seat = features.seat_assignments[0]
    assert (seat.feature_code, seat.units, seat.status) == ("descarga_cfdi", 1, "Active")

    assert info.balances == [CreditBalance(credit_type=1, available=7), CreditBalance(credit_type=2, available=3)]


def test_el_cliente_expone_el_servicio_me(client):
    assert isinstance(client.me, MeService)
