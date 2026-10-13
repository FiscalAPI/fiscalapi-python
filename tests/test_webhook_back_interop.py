"""Interoperabilidad con el back: una entrega firmada como la firma WebhookSigner de fapi-back (dos secretos durante una
rotación, el vigente primero) y con el sobre tal como lo serializa el back (camelCase, sin espacios, createdAt al segundo
con Z y las nulas presentes) verifica con webhooks.verify y se lee completa en WebhookEvent.
"""
from datetime import datetime, timedelta, timezone

import pytest

from fiscalapi import WebhookEventTypes, WebhookVerificationException, webhooks
from webhook_signing import generate_secret, headers

EVENT_ID = "0f6b2c1e-7d3a-4e8b-9c51-2a4d6e8f0b13"
PERSON_ID = "4b1c2d3e-0000-4000-8000-000000000002"
INVOICE_ID = "9f8e7d6c-0000-4000-8000-0000000000a1"
DOWNLOAD_REQUEST_ID = "3c2b1a09-0000-4000-8000-0000000000b7"
ENDPOINT_ID = "6a5b4c3d-0000-4000-8000-0000000000c9"
TIMESTAMP = 1791830873  # 2026-10-12T18:47:53Z, el createdAt de los sobres

# Los sobres de WebhookEnvelopeTests de fapi-back, con ids fijos.
CANCELED_INVOICE_BODY = (
    '{"id":"0f6b2c1e-7d3a-4e8b-9c51-2a4d6e8f0b13","type":"invoice.canceled","createdAt":"2026-10-12T18:47:53Z",'
    '"personId":"4b1c2d3e-0000-4000-8000-000000000002","data":{"relatedObject":{"id":"9f8e7d6c-0000-4000-8000-0000000000a1",'
    '"type":"invoice","url":"/api/v4/invoices/9f8e7d6c-0000-4000-8000-0000000000a1"},"status":"X","previousStatus":"C"}}'
)

COMPLETED_DOWNLOAD_REQUEST_BODY = (
    '{"id":"0f6b2c1e-7d3a-4e8b-9c51-2a4d6e8f0b13","type":"download_request.completed","createdAt":"2026-10-12T18:47:53Z",'
    '"personId":null,"data":{"relatedObject":{"id":"3c2b1a09-0000-4000-8000-0000000000b7","type":"download_request",'
    '"url":"/api/v4/download-requests/3c2b1a09-0000-4000-8000-0000000000b7"},"status":null,"previousStatus":null}}'
)

# El sobre de WebhookEvent.EndpointTest del back (POST webhook-endpoints/{id}/test): el recurso es el endpoint.
ENDPOINT_TEST_BODY = (
    '{"id":"0f6b2c1e-7d3a-4e8b-9c51-2a4d6e8f0b13","type":"webhook_endpoint.test","createdAt":"2026-10-12T18:47:53Z",'
    '"personId":null,"data":{"relatedObject":{"id":"6a5b4c3d-0000-4000-8000-0000000000c9","type":"webhook_endpoint",'
    '"url":"/api/v4/webhook-endpoints/6a5b4c3d-0000-4000-8000-0000000000c9"},"status":null,"previousStatus":null}}'
)


def verify_delivered(delivery_headers: dict, body, secret):
    return webhooks._verify_at(delivery_headers, body, secret, webhooks.DEFAULT_TOLERANCE, TIMESTAMP)


@pytest.mark.parametrize("as_bytes", [False, True])
def test_a_back_delivery_signed_during_a_rotation_verifies_with_either_secret_and_reads_every_field(as_bytes):
    current, previous = generate_secret(), generate_secret()
    delivery_headers = headers(EVENT_ID, TIMESTAMP, CANCELED_INVOICE_BODY, current, previous)
    body = CANCELED_INVOICE_BODY.encode("utf-8") if as_bytes else CANCELED_INVOICE_BODY

    for receiver_secret in (current, previous):
        event = verify_delivered(delivery_headers, body, [receiver_secret])

        assert event.id == EVENT_ID
        assert event.type == WebhookEventTypes.INVOICE_CANCELED
        assert event.created_at == datetime(2026, 10, 12, 18, 47, 53, tzinfo=timezone.utc)
        assert event.created_at.tzinfo is timezone.utc
        assert event.person_id == PERSON_ID
        assert event.data.related_object.id == INVOICE_ID
        assert event.data.related_object.type == "invoice"
        assert event.data.related_object.url == "/api/v4/invoices/" + INVOICE_ID
        assert event.data.status == "X"
        assert event.data.previous_status == "C"


def test_a_back_delivery_without_person_or_statuses_reads_them_as_none():
    secret = generate_secret()
    delivery_headers = headers(EVENT_ID, TIMESTAMP, COMPLETED_DOWNLOAD_REQUEST_BODY, secret)

    event = verify_delivered(delivery_headers, COMPLETED_DOWNLOAD_REQUEST_BODY, secret)

    assert event.type == WebhookEventTypes.DOWNLOAD_REQUEST_COMPLETED
    assert event.person_id is None
    assert event.data.related_object.id == DOWNLOAD_REQUEST_ID
    assert event.data.related_object.type == "download_request"
    assert event.data.related_object.url == "/api/v4/download-requests/" + DOWNLOAD_REQUEST_ID
    assert event.data.status is None
    assert event.data.previous_status is None


def test_a_back_endpoint_test_delivery_points_to_the_endpoint_without_person_or_statuses():
    secret = generate_secret()
    delivery_headers = headers(EVENT_ID, TIMESTAMP, ENDPOINT_TEST_BODY, secret)

    event = verify_delivered(delivery_headers, ENDPOINT_TEST_BODY, secret)

    assert event.type == WebhookEventTypes.WEBHOOK_ENDPOINT_TEST
    assert event.person_id is None
    assert event.data.related_object.id == ENDPOINT_ID
    assert event.data.related_object.type == "webhook_endpoint"
    assert event.data.related_object.url == "/api/v4/webhook-endpoints/" + ENDPOINT_ID
    assert event.data.status is None
    assert event.data.previous_status is None


def test_an_unknown_type_and_unknown_fields_are_read_without_error():
    body = (
        '{"id":"evt_1","type":"invoice.future_state","createdAt":"2026-10-12T18:47:53Z","personId":null,"extra":1,'
        '"data":{"relatedObject":{"id":"r1","type":"future_resource","url":"/api/v4/future/r1","extra":true},'
        '"status":"Z","previousStatus":null,"extra":[1,2]}}'
    )
    secret = generate_secret()

    event = verify_delivered(headers("evt_1", TIMESTAMP, body, secret), body, secret)

    assert event.type == "invoice.future_state"
    assert event.data.related_object.type == "future_resource"
    assert event.data.status == "Z"


def test_a_created_at_with_an_offset_is_read_in_utc():
    body = '{"id":"evt_1","type":"invoice.canceled","createdAt":"2026-10-12T12:47:53-06:00","personId":null}'
    secret = generate_secret()

    event = verify_delivered(headers("evt_1", TIMESTAMP, body, secret), body, secret)

    assert event.created_at == datetime(2026, 10, 12, 18, 47, 53, tzinfo=timezone.utc)
    assert event.created_at.utcoffset() == timedelta(0)
    assert event.created_at.tzinfo is timezone.utc


@pytest.mark.parametrize(
    "created_at",
    [
        pytest.param('"1791830873"', id="epoch-como-texto"),
        pytest.param("1791830873", id="epoch-como-numero"),
        pytest.param('"2026-10-12"', id="fecha-sin-hora"),
        pytest.param('"2026-10-12T18:47:53"', id="sin-zona"),
        pytest.param('"2026-10-12T18:47Z"', id="sin-segundos"),
        pytest.param('"12/10/2026 18:47:53"', id="no-iso"),
    ],
)
def test_a_created_at_that_is_not_iso_8601_with_time_and_zone_is_rejected(created_at):
    body = '{"id":"evt_1","type":"invoice.canceled","createdAt":' + created_at + ',"personId":null}'
    secret = generate_secret()

    with pytest.raises(WebhookVerificationException, match="no es un evento") as raised:
        verify_delivered(headers("evt_1", TIMESTAMP, body, secret), body, secret)
    assert raised.value.__cause__ is not None


@pytest.mark.parametrize("created_at", ["2026-10-12T18:47:53Z", "2026-10-12T18:47:53.250Z", "2026-10-12T18:47:53+00:00"])
def test_a_created_at_in_iso_8601_with_time_and_zone_is_read(created_at):
    body = '{"id":"evt_1","type":"invoice.canceled","createdAt":"' + created_at + '","personId":null}'
    secret = generate_secret()

    event = verify_delivered(headers("evt_1", TIMESTAMP, body, secret), body, secret)

    assert event.created_at.replace(microsecond=0) == datetime(2026, 10, 12, 18, 47, 53, tzinfo=timezone.utc)
    assert event.created_at.tzinfo is timezone.utc


def test_the_event_type_constants_are_the_types_of_the_back():
    assert WebhookEventTypes.INVOICE_CANCELLATION_REQUESTED == "invoice.cancellation_requested"
    assert WebhookEventTypes.INVOICE_CANCELED == "invoice.canceled"
    assert WebhookEventTypes.INVOICE_CANCELLATION_REJECTED == "invoice.cancellation_rejected"
    assert WebhookEventTypes.DOWNLOAD_REQUEST_COMPLETED == "download_request.completed"
    assert WebhookEventTypes.DOWNLOAD_REQUEST_ABANDONED == "download_request.abandoned"
    assert WebhookEventTypes.DOWNLOAD_RULE_SUSPENDED == "download_rule.suspended"
    assert WebhookEventTypes.WEBHOOK_ENDPOINT_TEST == "webhook_endpoint.test"
