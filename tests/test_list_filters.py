"""Filtros de las listas de facturas, personas y productos (GET /api/v4/invoices, /people y /products).

Los mismos escenarios viven en los SDK de .NET, Node, PHP y Java: cada filtro asignado viaja en camelCase y escapado,
uno en None no se envía, y sin filtros la ruta va sin query. ``get_list(page_number, page_size)`` sigue igual.
"""
from datetime import date

import pytest
from pydantic import ValidationError

from fiscalapi import (
    Invoice,
    InvoiceListFilters,
    InvoiceListOrder,
    PersonListFilters,
    ProductListFilters,
)

BASE_URL = "https://sdk-tests.fiscalapi.invalid/api/v4"

EMPTY_PAGE = {
    "data": {"items": [], "pageNumber": 1, "totalPages": 0, "totalCount": 0, "hasPreviousPage": False, "hasNextPage": False},
    "succeeded": True,
    "message": "",
    "details": "",
    "httpStatusCode": 200,
}


@pytest.fixture
def api(fake_api):
    fake_api.respond_with(EMPTY_PAGE)
    return fake_api


def test_invoices_envia_cada_filtro_en_el_orden_del_contrato(client, api):
    filters = InvoiceListFilters(
        from_=date(2026, 9, 1),
        to=date(2026, 9, 30),
        issuer_tin="EKU9003173C9",
        recipient_tin="FUNK671228PH6",
        type_code="I",
        status_id="V",
        series="SDK-F",
        number="1001",
        uuid="5f2c7a1e-0000-4000-8000-0000000000c3",
        order=InvoiceListOrder.DESC,
        page_number=2,
        page_size=50,
    )

    response = client.invoices.get_list(filters=filters)

    assert response.succeeded is True
    assert response.data.items == []
    assert api.requests[-1]["method"] == "GET"
    assert api.requests[-1]["json"] is None
    assert api.requested_urls == [
        f"{BASE_URL}/invoices?from=2026-09-01&to=2026-09-30&issuerTin=EKU9003173C9&recipientTin=FUNK671228PH6"
        "&typeCode=I&statusId=V&series=SDK-F&number=1001&uuid=5f2c7a1e-0000-4000-8000-0000000000c3&order=desc"
        "&pageNumber=2&pageSize=50"
    ]


def test_invoices_envia_solo_los_filtros_asignados(client, api):
    client.invoices.get_list(filters=InvoiceListFilters(status_id="X", order="asc", series=None))

    assert api.requested_urls == [f"{BASE_URL}/invoices?statusId=X&order=asc"]


def test_invoices_order_acepta_el_texto_y_el_enum(client, api):
    client.invoices.get_list(filters=InvoiceListFilters(order="desc"))
    client.invoices.get_list(filters=InvoiceListFilters(order=InvoiceListOrder.ASC))

    assert api.requested_urls == [f"{BASE_URL}/invoices?order=desc", f"{BASE_URL}/invoices?order=asc"]


def test_invoices_order_rechaza_un_valor_fuera_del_contrato():
    with pytest.raises(ValidationError):
        InvoiceListFilters(order="DESC")


def test_invoices_sin_filtros_la_ruta_va_sin_query(client, api):
    client.invoices.get_list()
    client.invoices.get_list(filters=InvoiceListFilters())

    assert api.requested_urls == [f"{BASE_URL}/invoices", f"{BASE_URL}/invoices"]


def test_invoices_get_list_con_la_pagina_sigue_igual(client, api):
    client.invoices.get_list(1, 10)
    client.invoices.get_list(page_number=2, page_size=5)

    assert api.requested_urls == [
        f"{BASE_URL}/invoices?pageNumber=1&pageSize=10",
        f"{BASE_URL}/invoices?pageNumber=2&pageSize=5",
    ]


def test_invoices_filtros_y_pagina_a_la_vez_lanza_sin_llamar_al_api(client, api):
    with pytest.raises(ValueError):
        client.invoices.get_list(1, 10, filters=InvoiceListFilters(status_id="V"))

    assert api.requested_urls == []


def test_people_envia_search_escapado_user_type_id_y_la_pagina(client, api):
    filters = PersonListFilters(search="Ana María & Co", user_type_id="C", page_number=1, page_size=20)

    client.people.get_list(filters=filters)

    assert api.requested_urls == [f"{BASE_URL}/people?search=Ana+Mar%C3%ADa+%26+Co&userTypeId=C&pageNumber=1&pageSize=20"]


def test_people_envia_solo_los_filtros_asignados(client, api):
    client.people.get_list(filters=PersonListFilters(user_type_id="U"))

    assert api.requested_urls == [f"{BASE_URL}/people?userTypeId=U"]


def test_people_sin_filtros_la_ruta_va_sin_query(client, api):
    client.people.get_list()

    assert api.requested_urls == [f"{BASE_URL}/people"]


def test_people_get_list_con_la_pagina_sigue_igual(client, api):
    client.people.get_list(3, 25)

    assert api.requested_urls == [f"{BASE_URL}/people?pageNumber=3&pageSize=25"]


def test_products_envia_search_y_la_pagina(client, api):
    client.products.get_list(filters=ProductListFilters(search="01010101", page_number=3, page_size=5))

    assert api.requested_urls == [f"{BASE_URL}/products?search=01010101&pageNumber=3&pageSize=5"]


def test_products_sin_filtros_la_ruta_va_sin_query(client, api):
    client.products.get_list(filters=ProductListFilters())

    assert api.requested_urls == [f"{BASE_URL}/products"]


def test_products_get_list_con_la_pagina_sigue_igual(client, api):
    client.products.get_list(1, 2)

    assert api.requested_urls == [f"{BASE_URL}/products?pageNumber=1&pageSize=2"]


def test_la_lista_filtrada_deserializa_la_pagina(client, fake_api):
    page = dict(EMPTY_PAGE, data=dict(EMPTY_PAGE["data"], items=[{"id": "f1", "series": "SDK-F"}], totalCount=1, totalPages=1))
    fake_api.respond_with(page)

    response = client.invoices.get_list(filters=InvoiceListFilters(series="SDK-F"))

    assert isinstance(response.data.items[0], Invoice)
    assert response.data.items[0].id == "f1"
    assert response.data.total_count == 1
