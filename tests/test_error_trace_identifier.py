"""Las respuestas de error exponen ``trace_identifier``, igual que en los SDK de .NET, Node.js y Java.

Los textos de los 5xx del API piden enviar el traceIdentifier a soporte. El cambio es aditivo: ``message``,
``details`` y ``http_status_code`` no cambian.
"""
from fiscalapi import SignManifestRequest

TRACE_IDENTIFIER = "5C1E0B7A92D44F3E8A6B1D07F3C29E41"


def _sign_request() -> SignManifestRequest:
    return SignManifestRequest(
        base64_cer="base64CerHere...",
        base64_key="base64KeyHere...",
        password="passwordPhraseHere...",
    )


def test_server_error_exposes_the_trace_identifier_and_keeps_message_and_details(client, fake_api):
    fake_api.respond_with({
        "data": None,
        "succeeded": False,
        "message": "Something went wrong on our end.",
        "details": "Ocurrió un error inesperado en el servidor. Escríbenos a soporte@fiscalapi.com con el traceIdentifier de esta respuesta.",
        "httpStatusCode": 500,
        "traceIdentifier": TRACE_IDENTIFIER,
    }, status_code=500)

    response = client.manifests.sign(_sign_request())

    assert response.succeeded is False
    assert response.http_status_code == 500
    assert response.message == "Something went wrong on our end."
    assert response.details == (
        "Ocurrió un error inesperado en el servidor. Escríbenos a soporte@fiscalapi.com con el traceIdentifier de esta respuesta."
    )
    assert response.trace_identifier == TRACE_IDENTIFIER
    assert response.data is None


def test_client_error_exposes_the_trace_identifier(client, fake_api):
    fake_api.respond_with({
        "data": None,
        "succeeded": False,
        "message": "Sorry, it's not me, it's you.",
        "details": "No existe un usuario con RFC EKU9003173C9 en el tenant actual.",
        "httpStatusCode": 404,
        "traceIdentifier": TRACE_IDENTIFIER,
    }, status_code=404)

    response = client.manifests.sign(_sign_request())

    assert response.http_status_code == 404
    assert response.message == "Sorry, it's not me, it's you."
    assert response.details == "No existe un usuario con RFC EKU9003173C9 en el tenant actual."
    assert response.trace_identifier == TRACE_IDENTIFIER


def test_validation_error_exposes_the_trace_identifier_and_keeps_the_joined_details(client, fake_api):
    fake_api.respond_with({
        "data": [{
            "propertyName": "Password",
            "errorMessage": "La contraseña de la llave privada (.key) es incorrecta o el archivo no es una llave privada.",
            "attemptedValue": None,
        }],
        "succeeded": False,
        "message": "Sorry, it's not me, it's you.",
        "details": "One or more validation failures have occurred.",
        "httpStatusCode": 400,
        "traceIdentifier": TRACE_IDENTIFIER,
    }, status_code=400)

    response = client.manifests.sign(_sign_request())

    assert response.http_status_code == 400
    assert response.details == (
        "Password: La contraseña de la llave privada (.key) es incorrecta o el archivo no es una llave privada."
    )
    assert response.trace_identifier == TRACE_IDENTIFIER


def test_error_without_trace_identifier_leaves_it_none(client, fake_api):
    fake_api.respond_with({
        "data": None,
        "succeeded": False,
        "message": "Too Many Requests",
        "details": "x",
        "httpStatusCode": 429,
    }, status_code=429)

    response = client.manifests.sign(_sign_request())

    assert response.http_status_code == 429
    assert response.trace_identifier is None
