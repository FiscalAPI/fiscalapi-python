"""Cancelar factura (DELETE /api/v4/invoices) cuando el SAT rechaza la solicitud.

El API responde 422 con ``succeeded`` en false, el mensaje genérico, "SAT <código>: <descripción>" en ``details`` y el
acuse con el código por UUID en ``data``. El SDK no lanza: entrega esos campos y deja el data en ``error_data``. Los
mismos escenarios viven en los SDK de .NET, Node.js, PHP y Java.
"""
from fiscalapi import CancelInvoiceRequest, CancelInvoiceResponse

INVOICE_ID = "21c39425-9d0a-449b-a7ba-49335b85b062"
INVOICE_UUID = "de841944-bd4f-4bb8-adfe-2a2282787c62"

SAT_REJECTION = {
    "data": {
        "base64CancellationAcknowledgement": "PD94bWwgdmVyc2lvbj0iMS4wIj8+...",
        "invoiceUuids": {INVOICE_UUID: "203"},
    },
    "succeeded": False,
    "message": "Sorry, it's not me, it's you.",
    "details": "SAT 203: el folio fiscal no corresponde al emisor de la solicitud de cancelación.",
    "httpStatusCode": 422,
}


def test_a_sat_rejection_is_422_with_the_sat_details_and_the_acknowledgement_in_error_data(client, fake_api):
    fake_api.respond_with(SAT_REJECTION, status_code=422)

    response = client.invoices.cancel(CancelInvoiceRequest(id=INVOICE_ID, cancellation_reason_code="02"))

    assert response.succeeded is False
    assert response.http_status_code == 422
    assert response.message == "Sorry, it's not me, it's you."
    assert response.details == "SAT 203: el folio fiscal no corresponde al emisor de la solicitud de cancelación."
    assert response.data is None
    rejection = CancelInvoiceResponse.model_validate(response.error_data)
    assert rejection.base64_cancellation_acknowledgement == "PD94bWwgdmVyc2lvbj0iMS4wIj8+..."
    assert rejection.invoice_uuids == {INVOICE_UUID: "203"}
    assert fake_api.requests[0]["method"] == "DELETE"
