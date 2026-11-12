"""Los cuerpos publicados (fixtures del kit sdk-e2e) deben cargar en los modelos del SDK, sin red.

Cada archivo de ``tests/fixtures/sdk-e2e`` es una copia del cuerpo que la documentación publica; si el modelo
rechaza alguno, el SDK deja de poder usar el ejemplo que la API documenta.
"""
import json
from pathlib import Path

import pytest

from fiscalapi.models.fiscalapi_models import CancelInvoiceRequest, Invoice, Person, Product, TaxFile

PUBLISHED_DIR = Path(__file__).parent / "fixtures" / "sdk-e2e"
MODEL_BY_FIXTURE = {
    "persona-crear.json": Person,
    "producto-crear.json": Product,
    "certificado.json": TaxFile,
    "llave.json": TaxFile,
    "cancelar-valores.json": CancelInvoiceRequest,
}


def _fixture_names():
    return sorted(path.name for path in PUBLISHED_DIR.glob("*.json"))


@pytest.mark.parametrize("name", _fixture_names())
def test_published_fixture_loads_into_sdk_model(name):
    body = json.loads((PUBLISHED_DIR / name).read_text(encoding="utf-8"))
    model = MODEL_BY_FIXTURE.get(name, Invoice)

    model.model_validate(body)
