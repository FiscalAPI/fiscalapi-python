"""
Ejemplos de Factura con Impuestos Locales usando el SDK de FiscalAPI para Python.

Este archivo contiene ejemplos de facturas con impuestos locales (por valores):
1. Impuestos Locales CEDULAR + ISH (ambos)
2. Impuestos Locales solo CEDULAR
3. Impuestos Locales solo ISH

Modo de operacion: Por Valores (todos los datos inline)
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
    TaxCredential,
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

# Certificados en base64 para ESCUELA KEMPER URGATE
escuela_kemper_urgate_base64_cer = "MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTE0MzUxWhcNMjcwNTE4MTE0MzUxWjCB1zEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmecO6n2GS0zL025gbHGQVxznPDICoXzR2uUngz4DqxVUC/w9cE6FxSiXm2ap8Gcjg7wmcZfm85EBaxCx/0J2u5CqnhzIoGCdhBPuhWQnIh5TLgj/X6uNquwZkKChbNe9aeFirU/JbyN7Egia9oKH9KZUsodiM/pWAH00PCtoKJ9OBcSHMq8Rqa3KKoBcfkg1ZrgueffwRLws9yOcRWLb02sDOPzGIm/jEFicVYt2Hw1qdRE5xmTZ7AGG0UHs+unkGjpCVeJ+BEBn0JPLWVvDKHZAQMj6s5Bku35+d/MyATkpOPsGT/VTnsouxekDfikJD1f7A1ZpJbqDpkJnss3vQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFaUgj5PqgvJigNMgtrdXZnbPfVBbukAbW4OGnUhNrA7SRAAfv2BSGk16PI0nBOr7qF2mItmBnjgEwk+DTv8Zr7w5qp7vleC6dIsZFNJoa6ZndrE/f7KO1CYruLXr5gwEkIyGfJ9NwyIagvHHMszzyHiSZIA850fWtbqtythpAliJ2jF35M5pNS+YTkRB+T6L/c6m00ymN3q9lT1rB03YywxrLreRSFZOSrbwWfg34EJbHfbFXpCSVYdJRfiVdvHnewN0r5fUlPtR9stQHyuqewzdkyb5jTTw02D2cUfL57vlPStBj7SEi3uOWvLrsiDnnCIxRMYJ2UA2ktDKHk+zWnsDmaeleSzonv2CHW42yXYPCvWi88oE1DJNYLNkIjua7MxAnkNZbScNw01A6zbLsZ3y8G6eEYnxSTRfwjd8EP4kdiHNJftm7Z4iRU7HOVh79/lRWB+gd171s3d/mI9kte3MRy6V8MMEMCAnMboGpaooYwgAmwclI2XZCczNWXfhaWe0ZS5PmytD/GDpXzkX0oEgY9K/uYo5V77NdZbGAjmyi8cE2B2ogvyaN2XfIInrZPgEffJ4AB7kFA2mwesdLOCh0BLD9itmCve3A1FGR4+stO2ANUoiI3w3Tv2yQSg4bjeDlJ08lXaaFCLW2peEXMXjQUk7fmpb5MNuOUTW6BE="
escuela_kemper_urgate_base64_key = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS/AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucoZQObOaLUEm+I+QZ7Y8Giupo+F1XWkLvAsdk/uZlJcTfKLJyJbJwsQYbSpLOCLataZ4O5MVnnmMbfG//NKJn9kSMvJQZhSwAwoGLYDm1ESGezrvZabgFJnoQv8Si1nAhVGTk9FkFBesxRzq07dmZYwFCnFSX4xt2fDHs1PMpQbeq83aL/PzLCce3kxbYSB5kQlzGtUYayiYXcu0cVRu228VwBLCD+2wTDDoCmRXtPesgrLKUR4WWWb5N2AqAU1mNDC+UEYsENAerOFXWnmwrcTAu5qyZ7GsBMTpipW4Dbou2yqQ0lpA/aB06n1kz1aL6mNqGPaJ+OqoFuc8Ugdhadd+MmjHfFzoI20SZ3b2geCsUMNCsAd6oXMsZdWm8lzjqCGWHFeol0ik/xHMQvuQkkeCsQ28PBxdnUgf7ZGer+TN+2ZLd2kvTBOk6pIVgy5yC6cZ+o1Tloql9hYGa6rT3xcMbXlW+9e5jM2MWXZliVW3ZhaPjptJFDbIfWxJPjz4QvKyJk0zok4muv13Iiwj2bCyefUTRz6psqI4cGaYm9JpscKO2RCJN8UluYGbbWmYQU+Int6LtZj/lv8p6xnVjWxYI+rBPdtkpfFYRp+MJiXjgPw5B6UGuoruv7+vHjOLHOotRo+RdjZt7NqL9dAJnl1Qb2jfW6+d7NYQSI/bAwxO0sk4taQIT6Gsu/8kfZOPC2xk9rphGqCSS/4q3Os0MMjA1bcJLyoWLp13pqhK6bmiiHw0BBXH4fbEp4xjSbpPx4tHXzbdn8oDsHKZkWh3pPC2J/nVl0k/yF1KDVowVtMDXE47k6TGVcBoqe8PDXCG9+vjRpzIidqNo5qebaUZu6riWMWzldz8x3Z/jLWXuDiM7/Yscn0Z2GIlfoeyz+GwP2eTdOw9EUedHjEQuJY32bq8LICimJ4Ht+zMJKUyhwVQyAER8byzQBwTYmYP5U0wdsyIFitphw+/IH8+v08Ia1iBLPQAeAvRfTTIFLCs8foyUrj5Zv2B/wTYIZy6ioUM+qADeXyo45uBLLqkN90Rf6kiTqDld78NxwsfyR5MxtJLVDFkmf2IMMJHTqSfhbi+7QJaC11OOUJTD0v9wo0X/oO5GvZhe0ZaGHnm9zqTopALuFEAxcaQlc4R81wjC4wrIrqWnbcl2dxiBtD73KW+wcC9ymsLf4I8BEmiN25lx/OUc1IHNyXZJYSFkEfaxCEZWKcnbiyf5sqFSSlEqZLc4lUPJFAoP6s1FHVcyO0odWqdadhRZLZC9RCzQgPlMRtji/OXy5phh7diOBZv5UYp5nb+MZ2NAB/eFXm2JLguxjvEstuvTDmZDUb6Uqv++RdhO5gvKf/AcwU38ifaHQ9uvRuDocYwVxZS2nr9rOwZ8nAh+P2o4e0tEXjxFKQGhxXYkn75H3hhfnFYjik/2qunHBBZfcdG148MaNP6DjX33M238T9Zw/GyGx00JMogr2pdP4JAErv9a5yt4YR41KGf8guSOUbOXVARw6+ybh7+meb7w4BeTlj3aZkv8tVGdfIt3lrwVnlbzhLjeQY6PplKp3/a5Kr5yM0T4wJoKQQ6v3vSNmrhpbuAtKxpMILe8CQoo="
password = "12345678a"


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
# 1. IMPUESTOS LOCALES CEDULAR + ISH (Por Valores)
# ============================================================================
def create_impuestos_locales_cedular_ish_valores():
    """
    Crea una factura con impuestos locales CEDULAR e ISH por valores.
    Incluye todos los datos del emisor, receptor y certificados inline.
    """
    print("\n" + "="*60)
    print("1. IMPUESTOS LOCALES CEDULAR + ISH (Por Valores)")
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
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=[
                TaxCredential(
                    base64_file=escuela_kemper_urgate_base64_cer,
                    file_type=0,
                    password=password
                ),
                TaxCredential(
                    base64_file=escuela_kemper_urgate_base64_key,
                    file_type=1,
                    password=password
                )
            ]
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="G01",
            email="someone@somewhere.com"
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
# 2. IMPUESTOS LOCALES SOLO CEDULAR (Por Valores)
# ============================================================================
def create_impuestos_locales_cedular_valores():
    """
    Crea una factura con impuesto local CEDULAR por valores.
    Incluye todos los datos del emisor, receptor y certificados inline.
    """
    print("\n" + "="*60)
    print("2. IMPUESTOS LOCALES SOLO CEDULAR (Por Valores)")
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
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=[
                TaxCredential(
                    base64_file=escuela_kemper_urgate_base64_cer,
                    file_type=0,
                    password=password
                ),
                TaxCredential(
                    base64_file=escuela_kemper_urgate_base64_key,
                    file_type=1,
                    password=password
                )
            ]
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="G01",
            email="someone@somewhere.com"
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
# 3. IMPUESTOS LOCALES SOLO ISH (Por Valores)
# ============================================================================
def create_impuestos_locales_ish_valores():
    """
    Crea una factura con impuesto local ISH por valores.
    Incluye todos los datos del emisor, receptor y certificados inline.
    """
    print("\n" + "="*60)
    print("3. IMPUESTOS LOCALES SOLO ISH (Por Valores)")
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
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=[
                TaxCredential(
                    base64_file=escuela_kemper_urgate_base64_cer,
                    file_type=0,
                    password=password
                ),
                TaxCredential(
                    base64_file=escuela_kemper_urgate_base64_key,
                    file_type=1,
                    password=password
                )
            ]
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="G01",
            email="someone@somewhere.com"
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
    Funcion principal que ejecuta los ejemplos de factura con impuestos locales por valores.
    Descomenta las funciones que desees ejecutar.
    """

    # 1. Impuestos locales CEDULAR + ISH
    # create_impuestos_locales_cedular_ish_valores()

    # 2. Impuestos locales solo CEDULAR
    # create_impuestos_locales_cedular_valores()

    # 3. Impuestos locales solo ISH
    # create_impuestos_locales_ish_valores()

    pass


if __name__ == "__main__":
    main()
