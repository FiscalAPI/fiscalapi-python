"""Infraestructura compartida de las pruebas del SDK.

Las respuestas del API se simulan reemplazando ``requests.request`` en ``base_service``: cada prueba
recorre el camino real del SDK (servicio -> ``send_request`` -> ``_process_response`` -> pydantic)
con un JSON fijo y sin red.
"""
import copy
import json
from pathlib import Path
from typing import Any, Callable

import pytest
import requests

from fiscalapi import FiscalApiClient, FiscalApiSettings

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    """Devuelve una copia del JSON de ``tests/fixtures/<name>`` para que la prueba pueda modificarla."""
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return copy.deepcopy(json.load(f))


class FakeApi:
    """Responde a cada petición del SDK con el cuerpo configurado y registra las peticiones.

    ``requests`` guarda, por petición, el método, la URL y el cuerpo JSON que armó el SDK (None si no lleva).
    """

    def __init__(self) -> None:
        self.body: Any = {}
        self.requested_urls: list[str] = []
        self.requests: list[dict] = []

    def respond_with(self, body: Any) -> None:
        self.body = body

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        self.requested_urls.append(url)
        self.requests.append({"method": method, "url": url, "json": kwargs.get("json")})
        response = requests.Response()
        response.status_code = 200
        response.encoding = "utf-8"
        response._content = json.dumps(self.body).encode("utf-8")
        return response


@pytest.fixture
def api_json() -> Callable[[str], dict]:
    return load_fixture


@pytest.fixture
def fake_api(monkeypatch: pytest.MonkeyPatch) -> FakeApi:
    api = FakeApi()
    monkeypatch.setattr("fiscalapi.services.base_service.requests.request", api.request)
    return api


@pytest.fixture
def client() -> FiscalApiClient:
    settings = FiscalApiSettings(api_url="https://sdk-tests.fiscalapi.invalid", api_key="sk_test_sdk", tenant="tenant-sdk")
    return FiscalApiClient(settings=settings)
