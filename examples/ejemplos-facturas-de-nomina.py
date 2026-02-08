"""
Ejemplos de Factura de Nomina usando el SDK de FiscalAPI para Python.

Este archivo contiene ejemplos de diferentes tipos de facturas de nomina:
1. Nomina Ordinaria
2. Nomina Asimilados
3. Nomina Con Bonos, Fondo Ahorro y Deducciones
4. Nomina Con Horas Extra
5. Nomina Con Incapacidades
6. Nomina con SNCF
7. Nomina Extraordinaria
8. Nomina Separacion Indemnizacion
9. Nomina Jubilacion Pension Retiro
10. Nomina Sin Deducciones
11. Nomina Subsidio causado al empleo
12. Nomina Viaticos
13. Nomina basica
"""

from datetime import datetime
from decimal import Decimal
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.models.fiscalapi_models import (
    Invoice,
    InvoiceComplement,
    InvoiceIssuer,
    InvoiceIssuerEmployerData,
    InvoiceRecipient,
    InvoiceRecipientEmployeeData,
    PayrollComplement,
    PayrollDeduction,
    PayrollEarning,
    PayrollEarningsComplement,
    PayrollOtherPayment,
    PayrollOvertime,
    PayrollDisability,
    PayrollSeverance,
    PayrollRetirement,
    PayrollBalanceCompensation,
    TaxCredential,
    EmployeeData,
    EmployerData,
    Person
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

# Certificados en base64
escuela_kemper_urgate_base64_cer = "MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTE0MzUxWhcNMjcwNTE4MTE0MzUxWjCB1zEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmecO6n2GS0zL025gbHGQVxznPDICoXzR2uUngz4DqxVUC/w9cE6FxSiXm2ap8Gcjg7wmcZfm85EBaxCx/0J2u5CqnhzIoGCdhBPuhWQnIh5TLgj/X6uNquwZkKChbNe9aeFirU/JbyN7Egia9oKH9KZUsodiM/pWAH00PCtoKJ9OBcSHMq8Rqa3KKoBcfkg1ZrgueffwRLws9yOcRWLb02sDOPzGIm/jEFicVYt2Hw1qdRE5xmTZ7AGG0UHs+unkGjpCVeJ+BEBn0JPLWVvDKHZAQMj6s5Bku35+d/MyATkpOPsGT/VTnsouxekDfikJD1f7A1ZpJbqDpkJnss3vQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFaUgj5PqgvJigNMgtrdXZnbPfVBbukAbW4OGnUhNrA7SRAAfv2BSGk16PI0nBOr7qF2mItmBnjgEwk+DTv8Zr7w5qp7vleC6dIsZFNJoa6ZndrE/f7KO1CYruLXr5gwEkIyGfJ9NwyIagvHHMszzyHiSZIA850fWtbqtythpAliJ2jF35M5pNS+YTkRB+T6L/c6m00ymN3q9lT1rB03YywxrLreRSFZOSrbwWfg34EJbHfbFXpCSVYdJRfiVdvHnewN0r5fUlPtR9stQHyuqewzdkyb5jTTw02D2cUfL57vlPStBj7SEi3uOWvLrsiDnnCIxRMYJ2UA2ktDKHk+zWnsDmaeleSzonv2CHW42yXYPCvWi88oE1DJNYLNkIjua7MxAnkNZbScNw01A6zbLsZ3y8G6eEYnxSTRfwjd8EP4kdiHNJftm7Z4iRU7HOVh79/lRWB+gd171s3d/mI9kte3MRy6V8MMEMCAnMboGpaooYwgAmwclI2XZCczNWXfhaWe0ZS5PmytD/GDpXzkX0oEgY9K/uYo5V77NdZbGAjmyi8cE2B2ogvyaN2XfIInrZPgEffJ4AB7kFA2mwesdLOCh0BLD9itmCve3A1FGR4+stO2ANUoiI3w3Tv2yQSg4bjeDlJ08lXaaFCLW2peEXMXjQUk7fmpb5MNuOUTW6BE="
escuela_kemper_urgate_base64_key = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS/AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucoZQObOaLUEm+I+QZ7Y8Giupo+F1XWkLvAsdk/uZlJcTfKLJyJbJwsQYbSpLOCLataZ4O5MVnnmMbfG//NKJn9kSMvJQZhSwAwoGLYDm1ESGezrvZabgFJnoQv8Si1nAhVGTk9FkFBesxRzq07dmZYwFCnFSX4xt2fDHs1PMpQbeq83aL/PzLCce3kxbYSB5kQlzGtUYayiYXcu0cVRu228VwBLCD+2wTDDoCmRXtPesgrLKUR4WWWb5N2AqAU1mNDC+UEYsENAerOFXWnmwrcTAu5qyZ7GsBMTpipW4Dbou2yqQ0lpA/aB06n1kz1aL6mNqGPaJ+OqoFuc8Ugdhadd+MmjHfFzoI20SZ3b2geCsUMNCsAd6oXMsZdWm8lzjqCGWHFeol0ik/xHMQvuQkkeCsQ28PBxdnUgf7ZGer+TN+2ZLd2kvTBOk6pIVgy5yC6cZ+o1Tloql9hYGa6rT3xcMbXlW+9e5jM2MWXZliVW3ZhaPjptJFDbIfWxJPjz4QvKyJk0zok4muv13Iiwj2bCyefUTRz6psqI4cGaYm9JpscKO2RCJN8UluYGbbWmYQU+Int6LtZj/lv8p6xnVjWxYI+rBPdtkpfFYRp+MJiXjgPw5B6UGuoruv7+vHjOLHOotRo+RdjZt7NqL9dAJnl1Qb2jfW6+d7NYQSI/bAwxO0sk4taQIT6Gsu/8kfZOPC2xk9rphGqCSS/4q3Os0MMjA1bcJLyoWLp13pqhK6bmiiHw0BBXH4fbEp4xjSbpPx4tHXzbdn8oDsHKZkWh3pPC2J/nVl0k/yF1KDVowVtMDXE47k6TGVcBoqe8PDXCG9+vjRpzIidqNo5qebaUZu6riWMWzldz8x3Z/jLWXuDiM7/Yscn0Z2GIlfoeyz+GwP2eTdOw9EUedHjEQuJY32bq8LICimJ4Ht+zMJKUyhwVQyAER8byzQBwTYmYP5U0wdsyIFitphw+/IH8+v08Ia1iBLPQAeAvRfTTIFLCs8foyUrj5Zv2B/wTYIZy6ioUM+qADeXyo45uBLLqkN90Rf6kiTqDld78NxwsfyR5MxtJLVDFkmf2IMMJHTqSfhbi+7QJaC11OOUJTD0v9wo0X/oO5GvZhe0ZaGHnm9zqTopALuFEAxcaQlc4R81wjC4wrIrqWnbcl2dxiBtD73KW+wcC9ymsLf4I8BEmiN25lx/OUc1IHNyXZJYSFkEfaxCEZWKcnbiyf5sqFSSlEqZLc4lUPJFAoP6s1FHVcyO0odWqdadhRZLZC9RCzQgPlMRtji/OXy5phh7diOBZv5UYp5nb+MZ2NAB/eFXm2JLguxjvEstuvTDmZDUb6Uqv++RdhO5gvKf/AcwU38ifaHQ9uvRuDocYwVxZS2nr9rOwZ8nAh+P2o4e0tEXjxFKQGhxXYkn75H3hhfnFYjik/2qunHBBZfcdG148MaNP6DjX33M238T9Zw/GyGx00JMogr2pdP4JAErv9a5yt4YR41KGf8guSOUbOXVARw6+ybh7+meb7w4BeTlj3aZkv8tVGdfIt3lrwVnlbzhLjeQY6PplKp3/a5Kr5yM0T4wJoKQQ6v3vSNmrhpbuAtKxpMILe8CQoo="
organicos_navez_osorio_base64_cer = "MIIF1DCCA7ygAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MzkwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTI1NTE2WhcNMjcwNTE4MTI1NTE2WjCB+zEzMDEGA1UEAxQqT1JHQU5JQ09TINFBVkVaIE9TT1JJTyBTLkEgREUgQy5WIFNBIERFIENWMTMwMQYDVQQpFCpPUkdBTklDT1Mg0UFWRVogT1NPUklPIFMuQSBERSBDLlYgU0EgREUgQ1YxMzAxBgNVBAoUKk9SR0FOSUNPUyDRQVZFWiBPU09SSU8gUy5BIERFIEMuViBTQSBERSBDVjElMCMGA1UELRQcT9FPMTIwNzI2UlgzIC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlAF4PoRqITQAEjFBzzfiT/NSN2yvb7Iv1ZMe4qD7tBxBxazRCx+GnimfpR+eaM744RlRDUj+hZfWcsOMn+q65UEIP+Xq5V1NbO1LZDse9uG1fLLSmptfKjyfvTtmBNYBjC3G6YmRv5qVw81CIS4aQOSMXKD+lrxjmRUhV9EAtXVoqGxvyDKeeX4caKuRz8mlrnR8/SMbnpobe5BNoXPrpDbEypemiJXe40pjsltY0RV3b0W0JtJQABUwZ9xn0lPYHY2q7IxYfohibv+o9ldXOXY6tivBZFfbGQSUp7CevC55+Y6uqh35Pi1o0nt/vBVgUOVPNM8d4TvGbXsE0G2J7QIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFp52XykMXfFUtjQqA2zzLPrPIDSMEpkm1vWY0qfz2gC2TlVpbDCWH2vFHpP8D14OifXOmYkws2cvLyE0uBN6se4zXxVHBpTEq+93rvu/tjvMU6r7DISDwB0EX5kmKIFcOugET3/Eq1mxZ6mrI0K26RaEUz+HVyR0EQ2Ll5CLExDkPYV/am0gynhn6QPkxPNbcbm77PEIbH7zc+t7ZB5sgQ6LnubgnKNZDn8bNhkuM1jqFkh7h0owhlJrOvATgrDSLnrot8FoLFkrWQD4uA5udGRwXn5QWx0QM5ScNiSgSRilSFEyXn6rH/CJLO05Sx5OwJJTaxFbAyOXnoNdPMzbQAziaW78478nCNZVSrKWpjwWpScirtM2zcQ9fywd/a3CG66Ff29zasfhHJCp29TIjj1OURp6l1CKc16+UxjuVJ1z5Xh7v3s8S2gtmuYP1sUXPvAEYuVp9CFW87QVMtl3+nGlyJEzSAW/yaps9ua5RmyJK0Mjk1zyXjOJoIY75CIOMN8oqVAxmLJg5XftXJSekGpxybw9aq9qOJdmxVcZoAFaYg4MAdKViBoYxfWfEm4q/ihRz4asnzLp9NJWTXN1YH94rJrK7JSEq820flgr1kiL7z7n1rgWMvhJH9nHriG3yRkno/8OdLJxOSXd7MKZfZx0EWDX8toqWyE7zia8aPM="
organicos_navez_osorio_base64_key = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS8AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRFLOMmsAaFFEdAecnfgJf0IlyJpvyNOGiSwXgY6uZtS0QJmmupWTlQATxbN4xeN7csx7yCMYxMiWXLyTbjVIWzzsFVKHbsxCudz6UDqMZ3aXEEPDDbPECXJC4FxqzuUgifN4QQuIvxfPbk23m3Vtqu9lr/xMrDNqLZ4RiqY2062kgQzGzekq8CSC97qBAbb8SFMgakFjeHN0JiTGaTpYCpGbu4d+i3ZrQ0mlYkxesdvCLqlCwVM0RTMJsNQ8vpBpRDzH372iOTLCO/gXtV8pEsxpUzG9LSUBo7xSMd1/lcfdyqVgnScgUm8/+toxk6uwZkUMWWvp7tqrMYQFYdR5CjiZjgAWrNorgMmawBqkJU6KQO/CpXVn99U1fANPfQoeyQMgLt35k0JKynG8MuWsgb4EG9Z6sRmOsCQQDDMKwhBjqcbEwN2dL4f1HyN8wklFCyYy6j1NTKU2AjRMXVu4+OlAp5jpjgv08RQxEkW/tNMSSBcpvOzNr64u0M692VA2fThR3UMQ/MZ2yVM6yY3GgIu2tJmg08lhmkoLpWZIMy7bZjj/AEbi7B3wSF4vDYZJcr/Djeezm3MMSghoiOIRSqtBjwf7ZjhA2ymdCsrzy7XSMVekT0y1S+ew1WhnzUNKQSucb6V2yRwNbm0EyeEuvVyHgiGEzCrzNbNHCfoFr69YCUi8itiDfiV7/p7LJzD8J/w85nmOkI/9p+aZ2EyaOdThqBmN4CtoDi5ixz/1EElLn7KVI4d/DZsZ4ZMu76kLAy94o0m6ORSbHX5hw12+P5DgGaLu/Dxd9cctRCkvcUdagiECuKGLJpxTJvEBQoZqUB8AJFgwKcNLl3Z5KAWL5hV0t1h8i3N4HllygqpfUSQMLWCtlGwdI4XGlGI5CmnjrL2Uj8sj9C0zSNqZVnAXFMV9f2ND9W6YJqfU89BQ6Y4QQRMGjXcVF7c78bn5r6zI+Qv2QKm3YiGCfuIa64B+PB/BdithpOuBPn5X5Zxc8ju/kYjJk7sau7VtKJseGOJ1bqOq99VzaxoHjzoJgthLHtni9WtGAnnQy7GMWGW4Un2yObHCxvQxx/rIZEaQiCGfRXOcZIZuXBe5xeHJFGrekDxu3YyumEnLWvsirDF3qhpUtxqvbkTuZw2xT3vTR+oWZpSEnYTd3k/09Eb0ovOPLkbhvcvCEeoI91EJvU+KI4Lm7ZsuTUSpECrHiS3uPOjboCigOWGayKzUHUICNrGK0zxgZXhhl6V7y9pImRl34ID/tZhr3veW4pQKgscv6sQjGJzaph2oCP7uZC6arGWcFpc2pgfBcobmOXYPWKskU3eWKClHBJnJ8MoOru+ObOb+izPhINHOmzP26TnKzFxdZiL+onxjadPYslcLtqlmOYpb/5hHgGOvitLhCLHCp0gYNB2uzj0sVxNs3k7k43KrlO5L6gp1KVaIw2a1yZzOCqDWWcePfKM3Mii9JdVyfHZLRRjFCQiOYo41AltHU+9IcaoT4J/j7pKw5tnlu2VaMlnN0dISpoq/ak0m4YjTd3XdRQeH9ktWmclkc65LdLKf9hIqjVqvOhQUJYkuT7OPgr+o7Z9BnClXMz1/CYWftwQE="
password = "12345678a"

escuela_kemper_urgate_id = "2e7b988f-3a2a-4f67-86e9-3f931dd48581"
karla_fuente_nolasco_id = "109f4d94-63ea-4a21-ab15-20c8b87d8ee9"
organicos_navez_osorio_id = "f645e146-f80e-40fa-953f-fd1bd06d4e9f"
xochilt_casas_chavez_id = "e3b4edaa-e4d9-4794-9c5b-3dd5b7e372aa"
ingrid_xodar_jimenez_id = "9367249f-f0ee-43f4-b771-da2fff3f185f"

# ============================================================================
# 1. NOMINA ORDINARIA (Facturación por valores)
# ============================================================================
def create_nomina_ordinaria_values():
    """
    Crea una factura de nomina ordinaria con percepciones, deducciones y otros pagos.
    """
    print("\n" + "="*60)
    print("1. NOMINA ORDINARIA")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108"
            ),
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
            tin="FUNK671228PH6",
            legal_name="KARLA FUENTE NOLASCO",
            zip_code="01160",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101MNEXXXA8",
                social_security_number="04078873454",
                labor_relation_start_date="2024-08-18",
                seniority="P54W",
                sat_contract_type_id="01",
                sat_tax_regime_type_id="02",
                employee_number="123456789",
                department="GenAI",
                position="Sr Software Engineer",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="05",
                sat_bank_id="012",
                base_salary_for_contributions=Decimal("2828.50"),
                integrated_daily_salary=Decimal("0.00"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2025-08-30",
                initial_payment_date="2025-07-31",
                final_payment_date="2025-08-30",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="1003",
                            concept="Sueldo Nominal",
                            taxed_amount=Decimal("95030.00"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="005",
                            code="5913",
                            concept="Fondo de Ahorro Aportacion Patron",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("4412.46")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="1885",
                            concept="Bono Ingles",
                            taxed_amount=Decimal("14254.50"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="029",
                            code="1941",
                            concept="Vales Despensa",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("3439.00")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="1824",
                            concept="Herramientas Teletrabajo (telecom y prop. electri)",
                            taxed_amount=Decimal("273.00"),
                            exempt_amount=Decimal("0.00")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="002",
                            code="5050",
                            concept="Exceso de subsidio al empleo",
                            amount=Decimal("0.00"),
                            subsidy_caused=Decimal("0.00")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="5003",
                        concept="ISR Causado",
                        amount=Decimal("27645.52")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="5910",
                        concept="Fondo de ahorro Empleado Inversion",
                        amount=Decimal("4412.46")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="5914",
                        concept="Fondo de Ahorro Patron Inversion",
                        amount=Decimal("4412.46")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="1966",
                        concept="Contribucion poliza exceso GMM",
                        amount=Decimal("519.91")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="1934",
                        concept="Descuento Vales Despensa",
                        amount=Decimal("1.00")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="1942",
                        concept="Vales Despensa Electronico",
                        amount=Decimal("3439.00")
                    ),
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="1895",
                        concept="IMSS",
                        amount=Decimal("2391.13")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 2. NOMINA ASIMILADOS (Facturación por valores)
# ============================================================================
def create_nomina_asimilados_values():
    """
    Crea una factura de nomina para asimilados a salarios.
    """
    print("\n" + "="*60)
    print("2. NOMINA ASIMILADOS")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="06880",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                origin_employer_tin="EKU9003173C9"
            ),
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
            tin="CACX7605101P8",
            legal_name="XOCHILT CASAS CHAVEZ",
            zip_code="36257",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                sat_contract_type_id="09",
                sat_unionized_status_id="No",
                sat_tax_regime_type_id="09",
                employee_number="00002",
                department="ADMINISTRACION",
                position="DIRECTOR DE ADMINISTRACION",
                sat_payment_periodicity_id="99",
                sat_bank_id="012",
                bank_account="1111111111",
                sat_payroll_state_id="CMX"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-06-02T00:00:00",
                initial_payment_date="2023-06-01T00:00:00",
                final_payment_date="2023-06-02T00:00:00",
                days_paid=Decimal("1"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="046",
                            code="010046",
                            concept="INGRESOS ASIMILADOS A SALARIOS",
                            taxed_amount=Decimal("111197.73"),
                            exempt_amount=Decimal("0.00")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="020002",
                        concept="ISR",
                        amount=Decimal("36197.73")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 3. NOMINA CON BONOS, FONDO AHORRO Y DEDUCCIONES (Facturación por valores)
# ============================================================================
def create_nomina_bonos_fondo_ahorro_values():
    """
    Crea una factura de nomina con bonos, fondo de ahorro y multiples deducciones.
    """
    print("\n" + "="*60)
    print("3. NOMINA CON BONOS, FONDO AHORRO Y DEDUCCIONES")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="Z0000001234"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101MNEXXXA8",
                social_security_number="0000000000",
                labor_relation_start_date="2022-03-02T00:00:00",
                seniority="P66W",
                sat_contract_type_id="01",
                sat_unionized_status_id="No",
                sat_tax_regime_type_id="02",
                employee_number="111111",
                sat_job_risk_id="4",
                sat_payment_periodicity_id="02",
                integrated_daily_salary=Decimal("180.96"),
                sat_payroll_state_id="GUA"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-06-11T00:00:00",
                initial_payment_date="2023-06-05T00:00:00",
                final_payment_date="2023-06-11T00:00:00",
                days_paid=Decimal("7"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="SP01",
                            concept="SUELDO",
                            taxed_amount=Decimal("1210.30"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="010",
                            code="SP02",
                            concept="PREMIO PUNTUALIDAD",
                            taxed_amount=Decimal("121.03"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="029",
                            code="SP03",
                            concept="MONEDERO ELECTRONICO",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("269.43")
                        ),
                        PayrollEarning(
                            earning_type_code="010",
                            code="SP04",
                            concept="PREMIO DE ASISTENCIA",
                            taxed_amount=Decimal("121.03"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="005",
                            code="SP54",
                            concept="APORTACION FONDO AHORRO",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("121.03")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="002",
                            code="ISRSUB",
                            concept="Subsidio ISR para empleo",
                            amount=Decimal("0.0"),
                            subsidy_caused=Decimal("0.0"),
                            balance_compensation=PayrollBalanceCompensation(
                                favorable_balance=Decimal("0.0"),
                                year=2022,
                                remaining_favorable_balance=Decimal("0.0")
                            )
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="ZA09",
                        concept="APORTACION FONDO AHORRO",
                        amount=Decimal("121.03")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="ISR",
                        concept="ISR",
                        amount=Decimal("36.57")
                    ),
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="IMSS",
                        concept="Cuota de Seguridad Social EE",
                        amount=Decimal("30.08")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="ZA68",
                        concept="DEDUCCION FDO AHORRO PAT",
                        amount=Decimal("121.03")
                    ),
                    PayrollDeduction(
                        deduction_type_code="018",
                        code="ZA11",
                        concept="APORTACION CAJA AHORRO",
                        amount=Decimal("300.00")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 4. NOMINA CON HORAS EXTRA (Facturación por valores)
# ============================================================================
def create_nomina_horas_extra_values():
    """
    Crea una factura de nomina con horas extra.
    """
    print("\n" + "="*60)
    print("4. NOMINA CON HORAS EXTRA")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01",
                seniority="P437W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="04",
                sat_bank_id="002",
                bank_account="1111111111",
                base_salary_for_contributions=Decimal("490.22"),
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        ),
                        PayrollEarning(
                            earning_type_code="019",
                            code="00100",
                            concept="Horas Extra",
                            taxed_amount=Decimal("50.00"),
                            exempt_amount=Decimal("50.00"),
                            overtime=[
                                PayrollOvertime(
                                    days=1,
                                    hours_type_code="01",
                                    extra_hours=2,
                                    amount_paid=Decimal("100.00")
                                )
                            ]
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="00301",
                        concept="Seguridad Social",
                        amount=Decimal("200")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="00302",
                        concept="ISR",
                        amount=Decimal("100")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 5. NOMINA CON INCAPACIDADES (Facturación por valores)
# ============================================================================
def create_nomina_incapacidades_values():
    """
    Crea una factura de nomina con incapacidades.
    """
    print("\n" + "="*60)
    print("5. NOMINA CON INCAPACIDADES")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01T00:00:00",
                seniority="P437W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="04",
                sat_bank_id="002",
                bank_account="1111111111",
                base_salary_for_contributions=Decimal("490.22"),
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="00301",
                        concept="Seguridad Social",
                        amount=Decimal("200")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="00302",
                        concept="ISR",
                        amount=Decimal("100")
                    )
                ],
                disabilities=[
                    PayrollDisability(
                        disability_days=1,
                        disability_type_code="01"
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 6. NOMINA CON SNCF (Sistema Nacional de Coordinacion Fiscal) (Facturación por valores)
# ============================================================================
def create_nomina_sncf_values():
    """
    Crea una factura de nomina con SNCF (para organismos publicos).
    Usa los certificados de Organicos Navez Osorio.
    """
    print("\n" + "="*60)
    print("6. NOMINA CON SNCF")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="39074",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="OÑO120726RX3",
            legal_name="ORGANICOS ÑAVEZ OSORIO",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="27112029",
                sat_fund_source_id="IP"
            ),
            tax_credentials=[
                TaxCredential(
                    base64_file=organicos_navez_osorio_base64_cer,
                    file_type=0,
                    password=password
                ),
                TaxCredential(
                    base64_file=organicos_navez_osorio_base64_key,
                    file_type=1,
                    password=password
                )
            ]
        ),
        recipient=InvoiceRecipient(
            tin="CACX7605101P8",
            legal_name="XOCHILT CASAS CHAVEZ",
            zip_code="36257",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="80997742673",
                labor_relation_start_date="2021-09-01",
                seniority="P88W",
                sat_contract_type_id="01",
                sat_tax_regime_type_id="02",
                employee_number="273",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="04",
                integrated_daily_salary=Decimal("221.48"),
                sat_payroll_state_id="GRO"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-16T00:00:00",
                initial_payment_date="2023-05-01T00:00:00",
                final_payment_date="2023-05-16T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="P001",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("3322.20"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="P540",
                            concept="Compensacion",
                            taxed_amount=Decimal("100.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="P550",
                            concept="Compensacion Garantizada Extraordinaria",
                            taxed_amount=Decimal("2200.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="P530",
                            concept="Servicio Extraordinario",
                            taxed_amount=Decimal("200.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="001",
                            code="P506",
                            concept="Otras Prestaciones",
                            taxed_amount=Decimal("1500.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="001",
                            code="P505",
                            concept="Remuneracion al Desempeno Legislativo",
                            taxed_amount=Decimal("17500.0"),
                            exempt_amount=Decimal("0.0")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="002",
                            code="o002",
                            concept="Subsidio para el empleo efectivamente entregado al trabajador",
                            amount=Decimal("0.0"),
                            subsidy_caused=Decimal("0.0")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="D002",
                        concept="ISR",
                        amount=Decimal("4716.61")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="D525",
                        concept="Redondeo",
                        amount=Decimal("0.81")
                    ),
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="D510",
                        concept="Cuota Trabajador ISSSTE",
                        amount=Decimal("126.78")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 7. NOMINA EXTRAORDINARIA (Facturación por valores)
# ============================================================================
def create_nomina_extraordinaria_values():
    """
    Crea una factura de nomina extraordinaria (ej. aguinaldo).
    """
    print("\n" + "="*60)
    print("7. NOMINA EXTRAORDINARIA")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01",
                seniority="P439W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="99",
                sat_bank_id="002",
                bank_account="1111111111",
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-06-04T00:00:00",
                initial_payment_date="2023-06-04T00:00:00",
                final_payment_date="2023-06-04T00:00:00",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="002",
                            code="00500",
                            concept="Gratificacion Anual (Aguinaldo)",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("10000.00")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 8. NOMINA SEPARACION INDEMNIZACION (Facturación por valores)
# ============================================================================
def create_nomina_separacion_indemnizacion_values():
    """
    Crea una factura de nomina por separacion e indemnizacion.
    """
    print("\n" + "="*60)
    print("8. NOMINA SEPARACION INDEMNIZACION")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01",
                seniority="P439W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="99",
                sat_bank_id="002",
                bank_account="1111111111",
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-06-04T00:00:00",
                initial_payment_date="2023-05-05T00:00:00",
                final_payment_date="2023-06-04T00:00:00",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="023",
                            code="00500",
                            concept="Pagos por separacion",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("10000.00")
                        ),
                        PayrollEarning(
                            earning_type_code="025",
                            code="00900",
                            concept="Indemnizaciones",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("500.00")
                        )
                    ],
                    other_payments=[],
                    severance=PayrollSeverance(
                        total_paid=Decimal("10500.00"),
                        years_of_service=1,
                        last_monthly_salary=Decimal("10000.00"),
                        accumulable_income=Decimal("10000.00"),
                        non_accumulable_income=Decimal("0.00")
                    )
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 9. NOMINA JUBILACION PENSION RETIRO (Facturación por valores)
# ============================================================================
def create_nomina_jubilacion_pension_retiro_values():
    """
    Crea una factura de nomina por jubilacion, pension o retiro.
    """
    print("\n" + "="*60)
    print("9. NOMINA JUBILACION PENSION RETIRO")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01",
                seniority="P439W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="99",
                sat_bank_id="002",
                bank_account="1111111111",
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-05-05T00:00:00",
                initial_payment_date="2023-06-04T00:00:00",
                final_payment_date="2023-06-04T00:00:00",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="039",
                            code="00500",
                            concept="Jubilaciones, pensiones o haberes de retiro",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("10000.00")
                        )
                    ],
                    retirement=PayrollRetirement(
                        total_one_time=Decimal("10000.00"),
                        accumulable_income=Decimal("10000.00"),
                        non_accumulable_income=Decimal("0.00")
                    )
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 10. NOMINA SIN DEDUCCIONES (Facturación por valores)
# ============================================================================
def create_nomina_sin_deducciones_values():
    """
    Crea una factura de nomina sin deducciones.
    """
    print("\n" + "="*60)
    print("10. NOMINA SIN DEDUCCIONES")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01",
                seniority="P437W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="04",
                sat_bank_id="002",
                bank_account="1111111111",
                base_salary_for_contributions=Decimal("490.22"),
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 11. NOMINA SUBSIDIO CAUSADO AL EMPLEO (Facturación por valores)
# ============================================================================
def create_nomina_subsidio_causado_values():
    """
    Crea una factura de nomina con subsidio causado al empleo.
    """
    print("\n" + "="*60)
    print("11. NOMINA SUBSIDIO CAUSADO AL EMPLEO")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01T00:00:00",
                seniority="P437W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="02",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="04",
                sat_bank_id="002",
                bank_account="1111111111",
                base_salary_for_contributions=Decimal("490.22"),
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="007",
                            code="0002",
                            concept="ISR ajustado por subsidio",
                            amount=Decimal("145.80"),
                            subsidy_caused=Decimal("0.0")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="107",
                        code="D002",
                        concept="Ajuste al Subsidio Causado",
                        amount=Decimal("160.35")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="D002",
                        concept="ISR",
                        amount=Decimal("145.80")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 12. NOMINA VIATICOS (Facturación por valores)
# ============================================================================
def create_nomina_viaticos_values():
    """
    Crea una factura de nomina con viaticos.
    """
    print("\n" + "="*60)
    print("12. NOMINA VIATICOS")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01T00:00:00",
                seniority="P438W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="04",
                sat_bank_id="002",
                bank_account="1111111111",
                base_salary_for_contributions=Decimal("490.22"),
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-09-26T00:00:00",
                initial_payment_date="2023-09-11T00:00:00",
                final_payment_date="2023-09-26T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="050",
                            code="050",
                            concept="Viaticos",
                            taxed_amount=Decimal("0"),
                            exempt_amount=Decimal("3000")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="081",
                        code="081",
                        concept="Ajuste en viaticos entregados al trabajador",
                        amount=Decimal("3000")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 13. NOMINA BASICA (Facturación por valores)
# ============================================================================
def create_nomina_basica_values():
    """
    Crea una factura de nomina basica con sueldo y deducciones de seguridad social e ISR.
    """
    print("\n" + "="*60)
    print("13. NOMINA BASICA")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            employer_data=InvoiceIssuerEmployerData(
                employer_registration="B5510768108",
                origin_employer_tin="URE180429TM6"
            ),
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
            tin="XOJI740919U48",
            legal_name="INGRID XODAR JIMENEZ",
            zip_code="76028",
            tax_regime_code="605",
            cfdi_use_code="CN01",
            employee_data=InvoiceRecipientEmployeeData(
                curp="XEXX010101HNEXXXA4",
                social_security_number="000000",
                labor_relation_start_date="2015-01-01T00:00:00",
                seniority="P437W",
                sat_contract_type_id="01",
                sat_workday_type_id="01",
                sat_tax_regime_type_id="03",
                employee_number="120",
                department="Desarrollo",
                position="Ingeniero de Software",
                sat_job_risk_id="1",
                sat_payment_periodicity_id="04",
                sat_bank_id="002",
                bank_account="1111111111",
                base_salary_for_contributions=Decimal("490.22"),
                integrated_daily_salary=Decimal("146.47"),
                sat_payroll_state_id="JAL"
            )
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="00301",
                        concept="Seguridad Social",
                        amount=Decimal("200")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="00302",
                        concept="ISR",
                        amount=Decimal("100")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response



#********************(Facturación por referencias)****************************
#********************(Facturación por referencias)****************************
#********************(Facturación por referencias)****************************

# ============================================================================
# 1. NOMINA ORDINARIA (Facturación por referencias)
# ============================================================================
def create_nomina_ordinaria_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina ordinaria por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 1. NOMINA ORDINARIA (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(karla_fuente_nolasco_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(karla_fuente_nolasco_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "FUNO850618MJCNLR09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=karla_fuente_nolasco_id,
        social_security_number="04078873454",
        labor_relation_start_date=datetime(2024, 8, 18),
        seniority="P54W",
        sat_contract_type_id="01",
        sat_tax_regime_type_id="02",
        employee_number="123456789",
        department="GenAI",
        position="Sr Software Engineer",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="05",
        sat_bank_id="012",
        base_salary_for_contributions=Decimal("2828.50"),
        integrated_daily_salary=Decimal("0.00"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_ordinaria_references():
    """
    Crea una factura de nomina ordinaria con percepciones, deducciones y otros pagos.
    """
    print("\n" + "="*60)
    print("1. NOMINA ORDINARIA")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=karla_fuente_nolasco_id,
            tax_regime_code="605",
            cfdi_use_code="CN01"
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2025-08-30",
                initial_payment_date="2025-07-31",
                final_payment_date="2025-08-30",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="1003",
                            concept="Sueldo Nominal",
                            taxed_amount=Decimal("95030.00"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="005",
                            code="5913",
                            concept="Fondo de Ahorro Aportacion Patron",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("4412.46")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="1885",
                            concept="Bono Ingles",
                            taxed_amount=Decimal("14254.50"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="029",
                            code="1941",
                            concept="Vales Despensa",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("3439.00")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="1824",
                            concept="Herramientas Teletrabajo (telecom y prop. electri)",
                            taxed_amount=Decimal("273.00"),
                            exempt_amount=Decimal("0.00")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="002",
                            code="5050",
                            concept="Exceso de subsidio al empleo",
                            amount=Decimal("0.00"),
                            subsidy_caused=Decimal("0.00")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="5003",
                        concept="ISR Causado",
                        amount=Decimal("27645.52")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="5910",
                        concept="Fondo de ahorro Empleado Inversion",
                        amount=Decimal("4412.46")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="5914",
                        concept="Fondo de Ahorro Patron Inversion",
                        amount=Decimal("4412.46")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="1966",
                        concept="Contribucion poliza exceso GMM",
                        amount=Decimal("519.91")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="1934",
                        concept="Descuento Vales Despensa",
                        amount=Decimal("1.00")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="1942",
                        concept="Vales Despensa Electronico",
                        amount=Decimal("3439.00")
                    ),
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="1895",
                        concept="IMSS",
                        amount=Decimal("2391.13")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 2. NOMINA ASIMILADOS (Facturación por referencias)
# ============================================================================
def create_nomina_asimilados_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina asimilados por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 2. NOMINA ASIMILADOS (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(xochilt_casas_chavez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(xochilt_casas_chavez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "CACX850618MJCSHS09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=xochilt_casas_chavez_id,
        sat_contract_type_id="09",
        sat_unionized_status_id="No",
        sat_tax_regime_type_id="09",
        employee_number="00002",
        department="ADMINISTRACION",
        position="DIRECTOR DE ADMINISTRACION",
        sat_payment_periodicity_id="99",
        sat_bank_id="012",
        bank_account="1111111111",
        sat_payroll_state_id="CMX"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        origin_employer_tin="EKU9003173C9"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_asimilados_references():
    """
    Crea una factura de nomina para asimilados a salarios usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("2. NOMINA ASIMILADOS (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="06880",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=xochilt_casas_chavez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-06-02T00:00:00",
                initial_payment_date="2023-06-01T00:00:00",
                final_payment_date="2023-06-02T00:00:00",
                days_paid=Decimal("1"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="046",
                            code="010046",
                            concept="INGRESOS ASIMILADOS A SALARIOS",
                            taxed_amount=Decimal("111197.73"),
                            exempt_amount=Decimal("0.00")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="020002",
                        concept="ISR",
                        amount=Decimal("36197.73")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response

# ============================================================================
# 3. NOMINA CON BONOS, FONDO AHORRO Y DEDUCCIONES (Facturación por referencias)
# ============================================================================
def create_nomina_bonos_fondo_ahorro_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina bonos por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 3. NOMINA CON BONOS, FONDO AHORRO Y DEDUCCIONES (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="0000000000",
        labor_relation_start_date=datetime(2022, 3, 2),
        seniority="P66W",
        sat_contract_type_id="01",
        sat_unionized_status_id="No",
        sat_tax_regime_type_id="02",
        employee_number="111111",
        sat_job_risk_id="4",
        sat_payment_periodicity_id="02",
        integrated_daily_salary=Decimal("180.96"),
        sat_payroll_state_id="GUA"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="Z0000001234"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_bonos_fondo_ahorro_references():
    """
    Crea una factura de nomina con bonos, fondo de ahorro usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("3. NOMINA CON BONOS, FONDO AHORRO Y DEDUCCIONES (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-06-11T00:00:00",
                initial_payment_date="2023-06-05T00:00:00",
                final_payment_date="2023-06-11T00:00:00",
                days_paid=Decimal("7"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="SP01",
                            concept="SUELDO",
                            taxed_amount=Decimal("1210.30"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="010",
                            code="SP02",
                            concept="PREMIO PUNTUALIDAD",
                            taxed_amount=Decimal("121.03"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="029",
                            code="SP03",
                            concept="MONEDERO ELECTRONICO",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("269.43")
                        ),
                        PayrollEarning(
                            earning_type_code="010",
                            code="SP04",
                            concept="PREMIO DE ASISTENCIA",
                            taxed_amount=Decimal("121.03"),
                            exempt_amount=Decimal("0.00")
                        ),
                        PayrollEarning(
                            earning_type_code="005",
                            code="SP54",
                            concept="APORTACION FONDO AHORRO",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("121.03")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="002",
                            code="ISRSUB",
                            concept="Subsidio ISR para empleo",
                            amount=Decimal("0.0"),
                            subsidy_caused=Decimal("0.0"),
                            balance_compensation=PayrollBalanceCompensation(
                                favorable_balance=Decimal("0.0"),
                                year=2022,
                                remaining_favorable_balance=Decimal("0.0")
                            )
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="ZA09",
                        concept="APORTACION FONDO AHORRO",
                        amount=Decimal("121.03")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="ISR",
                        concept="ISR",
                        amount=Decimal("36.57")
                    ),
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="IMSS",
                        concept="Cuota de Seguridad Social EE",
                        amount=Decimal("30.08")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="ZA68",
                        concept="DEDUCCION FDO AHORRO PAT",
                        amount=Decimal("121.03")
                    ),
                    PayrollDeduction(
                        deduction_type_code="018",
                        code="ZA11",
                        concept="APORTACION CAJA AHORRO",
                        amount=Decimal("300.00")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 4. NOMINA CON HORAS EXTRA (Facturación por referencias)
# ============================================================================
def create_nomina_horas_extra_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina horas extra por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 4. NOMINA CON HORAS EXTRA (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P437W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="04",
        sat_bank_id="002",
        bank_account="1111111111",
        base_salary_for_contributions=Decimal("490.22"),
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_horas_extra_references():
    """
    Crea una factura de nomina con horas extra usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("4. NOMINA CON HORAS EXTRA (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        ),
                        PayrollEarning(
                            earning_type_code="019",
                            code="00100",
                            concept="Horas Extra",
                            taxed_amount=Decimal("50.00"),
                            exempt_amount=Decimal("50.00"),
                            overtime=[
                                PayrollOvertime(
                                    days=1,
                                    hours_type_code="01",
                                    extra_hours=2,
                                    amount_paid=Decimal("100.00")
                                )
                            ]
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="00301",
                        concept="Seguridad Social",
                        amount=Decimal("200")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="00302",
                        concept="ISR",
                        amount=Decimal("100")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 5. NOMINA CON INCAPACIDADES (Facturación por referencias)
# ============================================================================
def create_nomina_incapacidades_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina incapacidades por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 5. NOMINA CON INCAPACIDADES (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P437W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="04",
        sat_bank_id="002",
        bank_account="1111111111",
        base_salary_for_contributions=Decimal("490.22"),
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_incapacidades_references():
    """
    Crea una factura de nomina con incapacidades usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("5. NOMINA CON INCAPACIDADES (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="00301",
                        concept="Seguridad Social",
                        amount=Decimal("200")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="00302",
                        concept="ISR",
                        amount=Decimal("100")
                    )
                ],
                disabilities=[
                    PayrollDisability(
                        disability_days=1,
                        disability_type_code="01"
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 6. NOMINA CON SNCF (Facturación por referencias)
# ============================================================================
def create_nomina_sncf_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina SNCF por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 6. NOMINA CON SNCF (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(xochilt_casas_chavez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(organicos_navez_osorio_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(xochilt_casas_chavez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "CACX850618MJCSHS09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=organicos_navez_osorio_id,
        employee_person_id=xochilt_casas_chavez_id,
        social_security_number="80997742673",
        labor_relation_start_date=datetime(2021, 9, 1),
        seniority="P88W",
        sat_contract_type_id="01",
        sat_tax_regime_type_id="02",
        employee_number="273",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="04",
        integrated_daily_salary=Decimal("221.48"),
        sat_payroll_state_id="GRO"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=organicos_navez_osorio_id,
        employer_registration="27112029",
        sat_fund_source_id="IP"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_sncf_references():
    """
    Crea una factura de nomina con SNCF usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("6. NOMINA CON SNCF (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="39074",
        export_code="01",
        issuer=InvoiceIssuer(
            id=organicos_navez_osorio_id
        ),
        recipient=InvoiceRecipient(
            id=xochilt_casas_chavez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-16T00:00:00",
                initial_payment_date="2023-05-01T00:00:00",
                final_payment_date="2023-05-16T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="P001",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("3322.20"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="P540",
                            concept="Compensacion",
                            taxed_amount=Decimal("100.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="P550",
                            concept="Compensacion Garantizada Extraordinaria",
                            taxed_amount=Decimal("2200.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="038",
                            code="P530",
                            concept="Servicio Extraordinario",
                            taxed_amount=Decimal("200.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="001",
                            code="P506",
                            concept="Otras Prestaciones",
                            taxed_amount=Decimal("1500.0"),
                            exempt_amount=Decimal("0.0")
                        ),
                        PayrollEarning(
                            earning_type_code="001",
                            code="P505",
                            concept="Remuneracion al Desempeno Legislativo",
                            taxed_amount=Decimal("17500.0"),
                            exempt_amount=Decimal("0.0")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="002",
                            code="o002",
                            concept="Subsidio para el empleo efectivamente entregado al trabajador",
                            amount=Decimal("0.0"),
                            subsidy_caused=Decimal("0.0")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="D002",
                        concept="ISR",
                        amount=Decimal("4716.61")
                    ),
                    PayrollDeduction(
                        deduction_type_code="004",
                        code="D525",
                        concept="Redondeo",
                        amount=Decimal("0.81")
                    ),
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="D510",
                        concept="Cuota Trabajador ISSSTE",
                        amount=Decimal("126.78")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 7. NOMINA EXTRAORDINARIA (Facturación por referencias)
# ============================================================================
def create_nomina_extraordinaria_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina extraordinaria por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 7. NOMINA EXTRAORDINARIA (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P439W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="99",
        sat_bank_id="002",
        bank_account="1111111111",
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_extraordinaria_references():
    """
    Crea una factura de nomina extraordinaria usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("7. NOMINA EXTRAORDINARIA (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-06-04T00:00:00",
                initial_payment_date="2023-06-04T00:00:00",
                final_payment_date="2023-06-04T00:00:00",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="002",
                            code="00500",
                            concept="Gratificacion Anual (Aguinaldo)",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("10000.00")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 8. NOMINA SEPARACION INDEMNIZACION (Facturación por referencias)
# ============================================================================
def create_nomina_separacion_indemnizacion_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina separacion indemnizacion por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 8. NOMINA SEPARACION INDEMNIZACION (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P439W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="99",
        sat_bank_id="002",
        bank_account="1111111111",
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_separacion_indemnizacion_references():
    """
    Crea una factura de nomina por separacion e indemnizacion usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("8. NOMINA SEPARACION INDEMNIZACION (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-06-04T00:00:00",
                initial_payment_date="2023-05-05T00:00:00",
                final_payment_date="2023-06-04T00:00:00",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="023",
                            code="00500",
                            concept="Pagos por separacion",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("10000.00")
                        ),
                        PayrollEarning(
                            earning_type_code="025",
                            code="00900",
                            concept="Indemnizaciones",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("500.00")
                        )
                    ],
                    other_payments=[],
                    severance=PayrollSeverance(
                        total_paid=Decimal("10500.00"),
                        years_of_service=1,
                        last_monthly_salary=Decimal("10000.00"),
                        accumulable_income=Decimal("10000.00"),
                        non_accumulable_income=Decimal("0.00")
                    )
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 9. NOMINA JUBILACION PENSION RETIRO (Facturación por referencias)
# ============================================================================
def create_nomina_jubilacion_pension_retiro_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina jubilacion pension retiro por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 9. NOMINA JUBILACION PENSION RETIRO (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P439W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="99",
        sat_bank_id="002",
        bank_account="1111111111",
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_jubilacion_pension_retiro_references():
    """
    Crea una factura de nomina por jubilacion, pension o retiro usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("9. NOMINA JUBILACION PENSION RETIRO (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="E",
                payment_date="2023-05-05T00:00:00",
                initial_payment_date="2023-06-04T00:00:00",
                final_payment_date="2023-06-04T00:00:00",
                days_paid=Decimal("30"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="039",
                            code="00500",
                            concept="Jubilaciones, pensiones o haberes de retiro",
                            taxed_amount=Decimal("0.00"),
                            exempt_amount=Decimal("10000.00")
                        )
                    ],
                    retirement=PayrollRetirement(
                        total_one_time=Decimal("10000.00"),
                        accumulable_income=Decimal("10000.00"),
                        non_accumulable_income=Decimal("0.00")
                    )
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 10. NOMINA SIN DEDUCCIONES (Facturación por referencias)
# ============================================================================
def create_nomina_sin_deducciones_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina sin deducciones por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 10. NOMINA SIN DEDUCCIONES (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P437W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="04",
        sat_bank_id="002",
        bank_account="1111111111",
        base_salary_for_contributions=Decimal("490.22"),
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_sin_deducciones_references():
    """
    Crea una factura de nomina sin deducciones usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("10. NOMINA SIN DEDUCCIONES (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 11. NOMINA SUBSIDIO CAUSADO (Facturación por referencias)
# ============================================================================
def create_nomina_subsidio_causado_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina subsidio causado por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 11. NOMINA SUBSIDIO CAUSADO (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P437W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="02",  # Different from other types
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="04",
        sat_bank_id="002",
        bank_account="1111111111",
        base_salary_for_contributions=Decimal("490.22"),
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_subsidio_causado_references():
    """
    Crea una factura de nomina con subsidio causado usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("11. NOMINA SUBSIDIO CAUSADO (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ],
                    other_payments=[
                        PayrollOtherPayment(
                            other_payment_type_code="007",
                            code="0002",
                            concept="ISR ajustado por subsidio",
                            amount=Decimal("145.80"),
                            subsidy_caused=Decimal("0.0")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="107",
                        code="D002",
                        concept="Ajuste al Subsidio Causado",
                        amount=Decimal("160.35")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="D002",
                        concept="ISR",
                        amount=Decimal("145.80")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 12. NOMINA VIATICOS (Facturación por referencias)
# ============================================================================
def create_nomina_viaticos_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina viaticos por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 12. NOMINA VIATICOS (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P438W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="04",
        sat_bank_id="002",
        bank_account="1111111111",
        base_salary_for_contributions=Decimal("490.22"),
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_viaticos_references():
    """
    Crea una factura de nomina con viaticos usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("12. NOMINA VIATICOS (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-09-26T00:00:00",
                initial_payment_date="2023-09-11T00:00:00",
                final_payment_date="2023-09-26T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="050",
                            code="050",
                            concept="Viaticos",
                            taxed_amount=Decimal("0"),
                            exempt_amount=Decimal("3000")
                        )
                    ]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="081",
                        code="081",
                        concept="Ajuste en viaticos entregados al trabajador",
                        amount=Decimal("3000")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 13. NOMINA BASICA (Facturación por referencias)
# ============================================================================
def create_nomina_basica_references_setup_data():
    """
    Configura los datos de empleado/empleador para nomina basica por referencias.
    """
    print("\n" + "="*60)
    print("SETUP: 13. NOMINA BASICA (Referencias)")
    print("="*60)

    # 1. Delete existing employee data
    try:
        response = client.people.employee.delete(ingrid_xodar_jimenez_id)
        print(f"  - Delete employee: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employee data: {e}")

    # 2. Delete existing employer data
    try:
        response = client.people.employer.delete(escuela_kemper_urgate_id)
        print(f"  - Delete employer: {response.succeeded}")
    except Exception as e:
        print(f"  - No existing employer data: {e}")

    # 3. Update person with curp and tax regime for payroll
    person_response = client.people.get_by_id(ingrid_xodar_jimenez_id)
    if person_response.succeeded and person_response.data:
        person = person_response.data
        person.curp = "XOJI850618MJCDNG09"
        person.sat_tax_regime_id = "605"
        person.sat_cfdi_use_id = "CN01"
        response = client.people.update(person)
        print(f"  - Update person: {response.succeeded}")
        if not response.succeeded:
            print(f"    Error: {response.message} - {response.details}")

    # 4. Create employee data
    employee_data = EmployeeData(
        employer_person_id=escuela_kemper_urgate_id,
        employee_person_id=ingrid_xodar_jimenez_id,
        social_security_number="000000",
        labor_relation_start_date=datetime(2015, 1, 1),
        seniority="P437W",
        sat_contract_type_id="01",
        sat_workday_type_id="01",
        sat_tax_regime_type_id="03",
        employee_number="120",
        department="Desarrollo",
        position="Ingeniero de Software",
        sat_job_risk_id="1",
        sat_payment_periodicity_id="04",
        sat_bank_id="002",
        bank_account="1111111111",
        base_salary_for_contributions=Decimal("490.22"),
        integrated_daily_salary=Decimal("146.47"),
        sat_payroll_state_id="JAL"
    )
    response = client.people.employee.create(employee_data)
    print(f"  - Create employee: {response.succeeded}")
    if not response.succeeded:
        print(f"    Error: {response.message} - {response.details}")

    # 5. Create employer data
    employer_data = EmployerData(
        person_id=escuela_kemper_urgate_id,
        employer_registration="B5510768108",
        origin_employer_tin="URE180429TM6"
    )
    response = client.people.employer.create(employer_data)
    print(f"  - Create employer: {response.succeeded}")
def create_nomina_basica_references():
    """
    Crea una factura de nomina basica usando facturacion por referencias.
    """
    print("\n" + "="*60)
    print("13. NOMINA BASICA (Referencias)")
    print("="*60)

    payroll_invoice = Invoice(
        version_code="4.0",
        series="F",
        date="2026-01-25T10:00:00",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="N",
        expedition_zip_code="20000",
        export_code="01",
        issuer=InvoiceIssuer(
            id=escuela_kemper_urgate_id
        ),
        recipient=InvoiceRecipient(
            id=ingrid_xodar_jimenez_id
        ),
        complement=InvoiceComplement(
            payroll=PayrollComplement(
                version="1.2",
                payroll_type_code="O",
                payment_date="2023-05-24T00:00:00",
                initial_payment_date="2023-05-09T00:00:00",
                final_payment_date="2023-05-24T00:00:00",
                days_paid=Decimal("15"),
                earnings=PayrollEarningsComplement(
                    earnings=[
                        PayrollEarning(
                            earning_type_code="001",
                            code="00500",
                            concept="Sueldos, Salarios Rayas y Jornales",
                            taxed_amount=Decimal("2808.8"),
                            exempt_amount=Decimal("2191.2")
                        )
                    ],
                    other_payments=[]
                ),
                deductions=[
                    PayrollDeduction(
                        deduction_type_code="001",
                        code="00301",
                        concept="Seguridad Social",
                        amount=Decimal("200")
                    ),
                    PayrollDeduction(
                        deduction_type_code="002",
                        code="00302",
                        concept="ISR",
                        amount=Decimal("100")
                    )
                ]
            )
        )
    )

    api_response = client.invoices.create(payroll_invoice)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# FUNCIONES DE INVOCACION
# ============================================================================
def invoke_by_values_payrolls():
    """
    Invoca UN metodo de facturacion por valores.
    Descomenta solo UNO a la vez para ejecutar el ejemplo.
    """
    # create_nomina_ordinaria_values()
    # create_nomina_asimilados_values()
    # create_nomina_bonos_fondo_ahorro_values()
    # create_nomina_horas_extra_values()
    # create_nomina_incapacidades_values()
    # create_nomina_sncf_values()
    # create_nomina_extraordinaria_values()
    # create_nomina_separacion_indemnizacion_values()
    # create_nomina_jubilacion_pension_retiro_values()
    # create_nomina_sin_deducciones_values()
    # create_nomina_subsidio_causado_values()
    # create_nomina_viaticos_values()
    # create_nomina_basica_values()
    pass


def invoke_by_references_payrolls():
    """
    Invoca UN metodo de facturacion por referencias con su setup.
    Descomenta solo UN PAR a la vez para ejecutar el ejemplo.
    """
    # create_nomina_ordinaria_references_setup_data()
    # create_nomina_ordinaria_references()

    # create_nomina_asimilados_references_setup_data()
    # create_nomina_asimilados_references()

    # create_nomina_bonos_fondo_ahorro_references_setup_data()
    # create_nomina_bonos_fondo_ahorro_references()

    # create_nomina_horas_extra_references_setup_data()
    # create_nomina_horas_extra_references()

    # create_nomina_incapacidades_references_setup_data()
    # create_nomina_incapacidades_references()

    # create_nomina_sncf_references_setup_data()
    # create_nomina_sncf_references()

    # create_nomina_extraordinaria_references_setup_data()
    # create_nomina_extraordinaria_references()

    # create_nomina_separacion_indemnizacion_references_setup_data()
    # create_nomina_separacion_indemnizacion_references()

    # create_nomina_jubilacion_pension_retiro_references_setup_data()
    # create_nomina_jubilacion_pension_retiro_references()

    # create_nomina_sin_deducciones_references_setup_data()
    # create_nomina_sin_deducciones_references()

    # create_nomina_subsidio_causado_references_setup_data()
    # create_nomina_subsidio_causado_references()

    # create_nomina_viaticos_references_setup_data()
    # create_nomina_viaticos_references()

    create_nomina_basica_references_setup_data()
    create_nomina_basica_references()
    pass


# ============================================================================
# FUNCION PRINCIPAL
# ============================================================================
def main():
    """
    Funcion principal que ejecuta los ejemplos de factura de nomina.
    Descomenta las funciones que desees ejecutar.
    """
    print("="*60)
    print("EJEMPLOS DE FACTURA DE NOMINA - FISCALAPI PYTHON SDK")
    print("="*60)

    # invoke_by_values_payrolls()
    invoke_by_references_payrolls()

    print("\n" + "="*60)
    print("FIN DE LOS EJEMPLOS")
    print("="*60)


if __name__ == "__main__":
    main()
