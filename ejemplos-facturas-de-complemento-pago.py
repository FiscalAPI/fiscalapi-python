"""
Ejemplos de Factura de Complemento de Pago usando el SDK de FiscalAPI para Python.

Este archivo contiene ejemplos de diferentes tipos de facturas de complemento de pago:
1. Complemento de Pago por Valores (todos los datos inline)
2. Complemento de Pago por Referencias (usando IDs de emisor y receptor)
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
    PaymentComplement,
    PaidInvoice,
    PaidInvoiceTax,
    TaxCredential
)
from fiscalapi.services.fiscalapi_client import FiscalApiClient


# ============================================================================
# CONFIGURACION
# ============================================================================

# Configuracion del cliente
settings = FiscalApiSettings(
    # api_url="https://test.fiscalapi.com",
    # api_key="<API_KEY>",
    # tenant="<TENANT_KEY>",
 
)

client = FiscalApiClient(settings=settings)

# Certificados en base64
karla_fuente_nolasco_base64_cer = "MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY="
karla_fuente_nolasco_base64_key = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ="
password = "12345678a"


# ============================================================================
# 1. COMPLEMENTO DE PAGO POR VALORES
# ============================================================================
def create_complemento_pago_valores():
    """
    Crea una factura de complemento de pago (factura de pago) por valores.
    Incluye todos los datos del emisor, receptor y certificados inline.
    """
    print("\n" + "="*60)
    print("1. COMPLEMENTO DE PAGO POR VALORES")
    print("="*60)

    payment_invoice = Invoice(
        version_code="4.0",
        series="CP",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        currency_code="XXX",
        type_code="P",
        expedition_zip_code="01160",
        exchange_rate=1,
        export_code="01",
        issuer=InvoiceIssuer(
            tin="FUNK671228PH6",
            legal_name="KARLA FUENTE NOLASCO",
            tax_regime_code="621",
            tax_credentials=[
                TaxCredential(
                    base64_file=karla_fuente_nolasco_base64_cer,
                    file_type=0,
                    password=password
                ),
                TaxCredential(
                    base64_file=karla_fuente_nolasco_base64_key,
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
            cfdi_use_code="CP01",
            email="mail@domain.com",
        ),
        items=[
            InvoiceItem(
                item_code="84111506",
                quantity=1,
                unit_of_measurement_code="ACT",
                description="Pago",
                unit_price=0,
                tax_object_code="01"
            )
        ],
        complement=InvoiceComplement(
            payment=PaymentComplement(
                payment_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                payment_form_code="28",
                currency_code="MXN",
                exchange_rate=Decimal("1"),
                amount=Decimal("11600.00"),
                source_bank_tin="BSM970519DU8",
                source_bank_account="1234567891012131",
                target_bank_tin="BBA830831LJ2",
                target_bank_account="1234567890",
                paid_invoices=[
                    PaidInvoice(
                        uuid="5C7B0622-01B4-4EB8-96D0-E0DEBD89FF0F",
                        series="F",
                        number="123",
                        currency_code="MXN",
                        partiality_number=1,
                        sub_total=Decimal("10000.00"),
                        previous_balance=Decimal("11600.00"),
                        payment_amount=Decimal("11600.00"),
                        remaining_balance=Decimal("0"),
                        tax_object_code="02",
                        paid_invoice_taxes=[
                            PaidInvoiceTax(
                                tax_code="002",
                                tax_type_code="Tasa",
                                tax_rate=Decimal("0.160000"),
                                tax_flag_code="T"
                            )
                        ]
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payment_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 2. COMPLEMENTO DE PAGO POR REFERENCIAS
# ============================================================================
def create_complemento_pago_referencias():
    """
    Crea una factura de complemento de pago (factura de pago) por referencias.
    Usa IDs de emisor y receptor previamente creados en el sistema.
    No incluye conceptos (items) ya que no son necesarios en este modo.
    """
    print("\n" + "="*60)
    print("2. COMPLEMENTO DE PAGO POR REFERENCIAS")
    print("="*60)

    payment_invoice = Invoice(
        version_code="4.0",
        series="CP",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        currency_code="XXX",
        type_code="P",
        expedition_zip_code="01160",
        exchange_rate=1,
        export_code="01",
        issuer=InvoiceIssuer(
            id="109f4d94-63ea-4a21-ab15-20c8b87d8ee9"
        ),
        recipient=InvoiceRecipient(
            id="2e7b988f-3a2a-4f67-86e9-3f931dd48581"
        ),
        complement=InvoiceComplement(
            payment=PaymentComplement(
                payment_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                payment_form_code="28",
                currency_code="MXN",
                exchange_rate=Decimal("1"),
                amount=Decimal("11600.00"),
                source_bank_tin="BSM970519DU8",
                source_bank_account="1234567891012131",
                target_bank_tin="BBA830831LJ2",
                target_bank_account="1234567890",
                paid_invoices=[
                    PaidInvoice(
                        uuid="5C7B0622-01B4-4EB8-96D0-E0DEBD89FF0F",
                        series="F",
                        number="123",
                        currency_code="MXN",
                        partiality_number=1,
                        sub_total=Decimal("10000.00"),
                        previous_balance=Decimal("11600.00"),
                        payment_amount=Decimal("11600.00"),
                        remaining_balance=Decimal("0"),
                        tax_object_code="02",
                        paid_invoice_taxes=[
                            PaidInvoiceTax(
                                tax_code="002",
                                tax_type_code="Tasa",
                                tax_rate=Decimal("0.160000"),
                                tax_flag_code="T"
                            )
                        ]
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payment_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# FUNCION PRINCIPAL
# ============================================================================
def main():
    """
    Funcion principal que ejecuta todos los ejemplos de factura de complemento de pago.
    Descomenta las funciones que desees ejecutar.
    """
    print("="*60)
    print("EJEMPLOS DE FACTURA DE COMPLEMENTO DE PAGO - FISCALAPI PYTHON SDK")
    print("="*60)

    # Ejecutar todos los ejemplos uno por uno
    examples = [
        create_complemento_pago_valores,
        create_complemento_pago_referencias,
    ]

    results = []
    for example in examples:
        try:
            response = example()
            success = response.succeeded if response else False
            results.append((example.__name__, success, None))
        except Exception as e:
            results.append((example.__name__, False, str(e)))

    # Resumen de resultados
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)
    for name, success, error in results:
        status = "OK" if success else "FAILED"
        print(f"{name}: {status}")
        if error:
            print(f"  Error: {error}")

    print("\n" + "="*60)
    print("FIN DE LOS EJEMPLOS")
    print("="*60)


if __name__ == "__main__":
    main()
