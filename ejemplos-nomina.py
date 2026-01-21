from datetime import datetime
from decimal import Decimal
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.models.fiscalapi_models import Invoice, InvoiceComplement, InvoiceIssuer, InvoiceIssuerEmployerData, InvoiceRecipient, InvoiceRecipientEmployeeData, PayrollComplement, PayrollDeduction, PayrollEarning, PayrollEarningsComplement, PayrollOtherPayment, TaxCredential
from fiscalapi.services.fiscalapi_client import FiscalApiClient

def main ():

    print("Hello World!")
    settings = FiscalApiSettings(
            #api_url="https://test.fiscalapi.com",
            #api_key="<API_KEY>",
            #tenant="<TENANT_KEY>",
            api_url="http://localhost:5001",
            api_key="sk_development_b470ea83_3c0f_4209_b933_85223b960d91",
            tenant="102e5f13-e114-41dd-bea7-507fce177281"
    )

    client = FiscalApiClient(settings=settings)

    base64_cer = "MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTE0MzUxWhcNMjcwNTE4MTE0MzUxWjCB1zEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmecO6n2GS0zL025gbHGQVxznPDICoXzR2uUngz4DqxVUC/w9cE6FxSiXm2ap8Gcjg7wmcZfm85EBaxCx/0J2u5CqnhzIoGCdhBPuhWQnIh5TLgj/X6uNquwZkKChbNe9aeFirU/JbyN7Egia9oKH9KZUsodiM/pWAH00PCtoKJ9OBcSHMq8Rqa3KKoBcfkg1ZrgueffwRLws9yOcRWLb02sDOPzGIm/jEFicVYt2Hw1qdRE5xmTZ7AGG0UHs+unkGjpCVeJ+BEBn0JPLWVvDKHZAQMj6s5Bku35+d/MyATkpOPsGT/VTnsouxekDfikJD1f7A1ZpJbqDpkJnss3vQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFaUgj5PqgvJigNMgtrdXZnbPfVBbukAbW4OGnUhNrA7SRAAfv2BSGk16PI0nBOr7qF2mItmBnjgEwk+DTv8Zr7w5qp7vleC6dIsZFNJoa6ZndrE/f7KO1CYruLXr5gwEkIyGfJ9NwyIagvHHMszzyHiSZIA850fWtbqtythpAliJ2jF35M5pNS+YTkRB+T6L/c6m00ymN3q9lT1rB03YywxrLreRSFZOSrbwWfg34EJbHfbFXpCSVYdJRfiVdvHnewN0r5fUlPtR9stQHyuqewzdkyb5jTTw02D2cUfL57vlPStBj7SEi3uOWvLrsiDnnCIxRMYJ2UA2ktDKHk+zWnsDmaeleSzonv2CHW42yXYPCvWi88oE1DJNYLNkIjua7MxAnkNZbScNw01A6zbLsZ3y8G6eEYnxSTRfwjd8EP4kdiHNJftm7Z4iRU7HOVh79/lRWB+gd171s3d/mI9kte3MRy6V8MMEMCAnMboGpaooYwgAmwclI2XZCczNWXfhaWe0ZS5PmytD/GDpXzkX0oEgY9K/uYo5V77NdZbGAjmyi8cE2B2ogvyaN2XfIInrZPgEffJ4AB7kFA2mwesdLOCh0BLD9itmCve3A1FGR4+stO2ANUoiI3w3Tv2yQSg4bjeDlJ08lXaaFCLW2peEXMXjQUk7fmpb5MNuOUTW6BE="
    base64_key = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS/AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucoZQObOaLUEm+I+QZ7Y8Giupo+F1XWkLvAsdk/uZlJcTfKLJyJbJwsQYbSpLOCLataZ4O5MVnnmMbfG//NKJn9kSMvJQZhSwAwoGLYDm1ESGezrvZabgFJnoQv8Si1nAhVGTk9FkFBesxRzq07dmZYwFCnFSX4xt2fDHs1PMpQbeq83aL/PzLCce3kxbYSB5kQlzGtUYayiYXcu0cVRu228VwBLCD+2wTDDoCmRXtPesgrLKUR4WWWb5N2AqAU1mNDC+UEYsENAerOFXWnmwrcTAu5qyZ7GsBMTpipW4Dbou2yqQ0lpA/aB06n1kz1aL6mNqGPaJ+OqoFuc8Ugdhadd+MmjHfFzoI20SZ3b2geCsUMNCsAd6oXMsZdWm8lzjqCGWHFeol0ik/xHMQvuQkkeCsQ28PBxdnUgf7ZGer+TN+2ZLd2kvTBOk6pIVgy5yC6cZ+o1Tloql9hYGa6rT3xcMbXlW+9e5jM2MWXZliVW3ZhaPjptJFDbIfWxJPjz4QvKyJk0zok4muv13Iiwj2bCyefUTRz6psqI4cGaYm9JpscKO2RCJN8UluYGbbWmYQU+Int6LtZj/lv8p6xnVjWxYI+rBPdtkpfFYRp+MJiXjgPw5B6UGuoruv7+vHjOLHOotRo+RdjZt7NqL9dAJnl1Qb2jfW6+d7NYQSI/bAwxO0sk4taQIT6Gsu/8kfZOPC2xk9rphGqCSS/4q3Os0MMjA1bcJLyoWLp13pqhK6bmiiHw0BBXH4fbEp4xjSbpPx4tHXzbdn8oDsHKZkWh3pPC2J/nVl0k/yF1KDVowVtMDXE47k6TGVcBoqe8PDXCG9+vjRpzIidqNo5qebaUZu6riWMWzldz8x3Z/jLWXuDiM7/Yscn0Z2GIlfoeyz+GwP2eTdOw9EUedHjEQuJY32bq8LICimJ4Ht+zMJKUyhwVQyAER8byzQBwTYmYP5U0wdsyIFitphw+/IH8+v08Ia1iBLPQAeAvRfTTIFLCs8foyUrj5Zv2B/wTYIZy6ioUM+qADeXyo45uBLLqkN90Rf6kiTqDld78NxwsfyR5MxtJLVDFkmf2IMMJHTqSfhbi+7QJaC11OOUJTD0v9wo0X/oO5GvZhe0ZaGHnm9zqTopALuFEAxcaQlc4R81wjC4wrIrqWnbcl2dxiBtD73KW+wcC9ymsLf4I8BEmiN25lx/OUc1IHNyXZJYSFkEfaxCEZWKcnbiyf5sqFSSlEqZLc4lUPJFAoP6s1FHVcyO0odWqdadhRZLZC9RCzQgPlMRtji/OXy5phh7diOBZv5UYp5nb+MZ2NAB/eFXm2JLguxjvEstuvTDmZDUb6Uqv++RdhO5gvKf/AcwU38ifaHQ9uvRuDocYwVxZS2nr9rOwZ8nAh+P2o4e0tEXjxFKQGhxXYkn75H3hhfnFYjik/2qunHBBZfcdG148MaNP6DjX33M238T9Zw/GyGx00JMogr2pdP4JAErv9a5yt4YR41KGf8guSOUbOXVARw6+ybh7+meb7w4BeTlj3aZkv8tVGdfIt3lrwVnlbzhLjeQY6PplKp3/a5Kr5yM0T4wJoKQQ6v3vSNmrhpbuAtKxpMILe8CQoo="

    payroll_invoice = Invoice(
            version_code="4.0",
            series="F",
            date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            payment_method_code="PUE",
            currency_code="MXN",
            type_code="N",  # N = Nomina
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
                        base64_file=base64_cer,
                        file_type=0,  # Certificado
                        password="12345678a"
                    ),
                    TaxCredential(
                        base64_file=base64_key,
                        file_type=1,  # Llave privada
                        password="12345678a"
                    )
                ]
            ),
            recipient=InvoiceRecipient(
                tin="FUNK671228PH6",
                legal_name="KARLA FUENTE NOLASCO",
                zip_code="01160",
                tax_regime_code="605",
                cfdi_use_code="CN01",  # Nomina
                employee_data=InvoiceRecipientEmployeeData(
                    curp="XEXX010101MNEXXXA8",
                    social_security_number="04078873454",
                    labor_relation_start_date="2024-08-18",
                    seniority="P54W",  # ISO 8601 duration (54 weeks)
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
                    payroll_type_code="O",  # O = Ordinaria
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
    print(api_response)

if __name__ == "__main__":
    main()
