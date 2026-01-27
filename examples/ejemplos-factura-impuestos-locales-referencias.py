"""
Ejemplos de Factura con Impuestos Locales usando el SDK de FiscalAPI para Python.

Este archivo contiene ejemplos de facturas con impuestos locales (por referencias):
1. Impuestos Locales CEDULAR + ISH (ambos)
2. Impuestos Locales solo CEDULAR
3. Impuestos Locales solo ISH

Modo de operacion: Por Referencias (usando IDs de emisor y receptor)
"""

from datetime import datetime
from decimal import Decimal
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.models.fiscalapi_models import (
    Invoice,
    InvoiceItem,
    InvoiceIssuer,
    InvoiceRecipient,
    InvoiceComplement,
    ItemTax,
    LocalTax,
    LocalTaxesComplement
)
from fiscalapi.services.fiscalapi_client import FiscalApiClient


# ============================================================================
# CONFIGURACION
# ============================================================================

# Configuracion del cliente
settings = FiscalApiSettings(
    # api_url="https://test.fiscalapi.com",
    # api_key="<API_KEY>",
    # tenant="<TENANT_KEY>"
)

client = FiscalApiClient(settings=settings)

# IDs de personas para los ejemplos (pre-creadas en el sistema)
escuela_kemper_urgate_id = "2e7b988f-3a2a-4f67-86e9-3f931dd48581"


def get_invoice_items():
    """
    Retorna los items de ejemplo para las facturas con impuestos locales.
    """
    return [
        InvoiceItem(
            item_code="01010101",
            quantity=Decimal("9.5"),
            unit_of_measurement_code="E48",
            unit_of_measurement="Unidad de servicio",
            description="Invoicing software as a service",
            unit_price=Decimal("3587.75"),
            tax_object_code="02",
            item_sku="7506022301697",
            discount=Decimal("255.85"),
            item_taxes=[
                ItemTax(
                    tax_code="002",
                    tax_type_code="Tasa",
                    tax_rate=Decimal("0.160000"),
                    tax_flag_code="T"
                )
            ]
        ),
        InvoiceItem(
            item_code="01010101",
            quantity=Decimal("8"),
            unit_of_measurement_code="E48",
            unit_of_measurement="Unidad de servicio2",
            description="Software Consultant",
            unit_price=Decimal("250.85"),
            tax_object_code="02",
            item_sku="7506022301698",
            discount=Decimal("255.85"),
            item_taxes=[
                ItemTax(
                    tax_code="002",
                    tax_type_code="Tasa",
                    tax_rate=Decimal("0.160000"),
                    tax_flag_code="T"
                )
            ]
        ),
        InvoiceItem(
            item_code="01010101",
            quantity=Decimal("6"),
            unit_of_measurement_code="E48",
            unit_of_measurement="Unidad de servicio3",
            description="Computer software",
            unit_price=Decimal("1250.75"),
            tax_object_code="02",
            item_sku="7506022301699",
            item_taxes=[
                ItemTax(
                    tax_code="002",
                    tax_type_code="Tasa",
                    tax_rate=Decimal("0.160000"),
                    tax_flag_code="T"
                ),
                ItemTax(
                    tax_code="002",
                    tax_type_code="Tasa",
                    tax_rate=Decimal("0.106666"),
                    tax_flag_code="R"
                )
            ]
        )
    ]


# ============================================================================
# 1. IMPUESTOS LOCALES CEDULAR + ISH (Por Referencias)
# ============================================================================
def create_impuestos_locales_cedular_ish_referencias():
    """
    Crea una factura con impuestos locales CEDULAR e ISH por referencias.
    Usa IDs de emisor y receptor previamente creados en el sistema.
    """
    print("\n" + "="*60)
    print("1. IMPUESTOS LOCALES CEDULAR + ISH (Por Referencias)")
    print("="*60)

    invoice = Invoice(
        version_code="4.0",
        series="F",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        payment_form_code="01",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        payment_method_code="PUE",
        exchange_rate=1,
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=escuela_kemper_urgate_id
        ),
        items=get_invoice_items(),
        complement=InvoiceComplement(
            local_taxes=LocalTaxesComplement(
                taxes=[
                    LocalTax(
                        tax_name="CEDULAR",
                        tax_rate=Decimal("3.00"),
                        tax_amount=Decimal("6.00"),
                        tax_flag_code="R"
                    ),
                    LocalTax(
                        tax_name="ISH",
                        tax_rate=Decimal("8.00"),
                        tax_amount=Decimal("16.00"),
                        tax_flag_code="R"
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 2. IMPUESTOS LOCALES SOLO CEDULAR (Por Referencias)
# ============================================================================
def create_impuestos_locales_cedular_referencias():
    """
    Crea una factura con impuesto local CEDULAR por referencias.
    Usa IDs de emisor y receptor previamente creados en el sistema.
    """
    print("\n" + "="*60)
    print("2. IMPUESTOS LOCALES SOLO CEDULAR (Por Referencias)")
    print("="*60)

    invoice = Invoice(
        version_code="4.0",
        series="F",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        payment_form_code="01",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        payment_method_code="PUE",
        exchange_rate=1,
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=escuela_kemper_urgate_id
        ),
        items=get_invoice_items(),
        complement=InvoiceComplement(
            local_taxes=LocalTaxesComplement(
                taxes=[
                    LocalTax(
                        tax_name="CEDULAR",
                        tax_rate=Decimal("3.00"),
                        tax_amount=Decimal("6.00"),
                        tax_flag_code="R"
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 3. IMPUESTOS LOCALES SOLO ISH (Por Referencias)
# ============================================================================
def create_impuestos_locales_ish_referencias():
    """
    Crea una factura con impuesto local ISH por referencias.
    Usa IDs de emisor y receptor previamente creados en el sistema.
    """
    print("\n" + "="*60)
    print("3. IMPUESTOS LOCALES SOLO ISH (Por Referencias)")
    print("="*60)

    invoice = Invoice(
        version_code="4.0",
        series="F",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        payment_form_code="01",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        payment_method_code="PUE",
        exchange_rate=1,
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=escuela_kemper_urgate_id
        ),
        items=get_invoice_items(),
        complement=InvoiceComplement(
            local_taxes=LocalTaxesComplement(
                taxes=[
                    LocalTax(
                        tax_name="ISH",
                        tax_rate=Decimal("8.00"),
                        tax_amount=Decimal("16.00"),
                        tax_flag_code="R"
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# FUNCION PRINCIPAL
# ============================================================================
def main():
    """
    Funcion principal que ejecuta los ejemplos de factura con impuestos locales por referencias.
    Descomenta las funciones que desees ejecutar.
    """

    # 1. Impuestos locales CEDULAR + ISH
    # create_impuestos_locales_cedular_ish_referencias()

    # 2. Impuestos locales solo CEDULAR
    # create_impuestos_locales_cedular_referencias()

    # 3. Impuestos locales solo ISH
    # create_impuestos_locales_ish_referencias()

    pass


if __name__ == "__main__":
    main()
