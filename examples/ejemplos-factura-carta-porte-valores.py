# ============================================================================
# CONFIGURACION
# ============================================================================

from datetime import datetime
from decimal import Decimal

# Configuracion del cliente
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.fiscalapi_client import FiscalApiClient
from fiscalapi.models.fiscalapi_models import (
    Invoice,
    InvoiceComplement,
    InvoiceIssuer,
    InvoiceRecipient,
    InvoiceItem,
    ItemTax,
    TaxCredential,
)
from fiscalapi.models.bill_of_lading_models import (
    LadingComplement,
    Ubicacion,
    UbicacionDomicilio,
    TipoFiguraDomicilio,
    Mercancia,
    CantidadTransporta,
    Autotransporte,
    Remolque,
    TipoFigura,
    RegimenAduanero,
    DocumentoAduanero,
    TransporteFerroviario,
    DerechoDePaso,
    Carro,
    TransporteAereo,
    ParteTransporte,
    TransporteMaritimo,
    ContenedorMaritimo,
    RemolqueCCP,
    DetalleMercancia,
)


settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="sk_test_b7dae706_e16f_4faf_90fb_a5d1990985a2",
    tenant="275510ee-f64d-435a-9e92-1553d8f10a7e"
)

client = FiscalApiClient(settings=settings)

# Certificados en base64
escuela_kemper_urgate_base64_cer = "MIIFsDCCA5igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0MTYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTE0MzUxWhcNMjcwNTE4MTE0MzUxWjCB1zEnMCUGA1UEAxMeRVNDVUVMQSBLRU1QRVIgVVJHQVRFIFNBIERFIENWMScwJQYDVQQpEx5FU0NVRUxBIEtFTVBFUiBVUkdBVEUgU0EgREUgQ1YxJzAlBgNVBAoTHkVTQ1VFTEEgS0VNUEVSIFVSR0FURSBTQSBERSBDVjElMCMGA1UELRMcRUtVOTAwMzE3M0M5IC8gVkFEQTgwMDkyN0RKMzEeMBwGA1UEBRMVIC8gVkFEQTgwMDkyN0hTUlNSTDA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtmecO6n2GS0zL025gbHGQVxznPDICoXzR2uUngz4DqxVUC/w9cE6FxSiXm2ap8Gcjg7wmcZfm85EBaxCx/0J2u5CqnhzIoGCdhBPuhWQnIh5TLgj/X6uNquwZkKChbNe9aeFirU/JbyN7Egia9oKH9KZUsodiM/pWAH00PCtoKJ9OBcSHMq8Rqa3KKoBcfkg1ZrgueffwRLws9yOcRWLb02sDOPzGIm/jEFicVYt2Hw1qdRE5xmTZ7AGG0UHs+unkGjpCVeJ+BEBn0JPLWVvDKHZAQMj6s5Bku35+d/MyATkpOPsGT/VTnsouxekDfikJD1f7A1ZpJbqDpkJnss3vQIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAFaUgj5PqgvJigNMgtrdXZnbPfVBbukAbW4OGnUhNrA7SRAAfv2BSGk16PI0nBOr7qF2mItmBnjgEwk+DTv8Zr7w5qp7vleC6dIsZFNJoa6ZndrE/f7KO1CYruLXr5gwEkIyGfJ9NwyIagvHHMszzyHiSZIA850fWtbqtythpAliJ2jF35M5pNS+YTkRB+T6L/c6m00ymN3q9lT1rB03YywxrLreRSFZOSrbwWfg34EJbHfbFXpCSVYdJRfiVdvHnewN0r5fUlPtR9stQHyuqewzdkyb5jTTw02D2cUfL57vlPStBj7SEi3uOWvLrsiDnnCIxRMYJ2UA2ktDKHk+zWnsDmaeleSzonv2CHW42yXYPCvWi88oE1DJNYLNkIjua7MxAnkNZbScNw01A6zbLsZ3y8G6eEYnxSTRfwjd8EP4kdiHNJftm7Z4iRU7HOVh79/lRWB+gd171s3d/mI9kte3MRy6V8MMEMCAnMboGpaooYwgAmwclI2XZCczNWXfhaWe0ZS5PmytD/GDpXzkX0oEgY9K/uYo5V77NdZbGAjmyi8cE2B2ogvyaN2XfIInrZPgEffJ4AB7kFA2mwesdLOCh0BLD9itmCve3A1FGR4+stO2ANUoiI3w3Tv2yQSg4bjeDlJ08lXaaFCLW2peEXMXjQUk7fmpb5MNuOUTW6BE="
escuela_kemper_urgate_base64_key = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS/AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucoZQObOaLUEm+I+QZ7Y8Giupo+F1XWkLvAsdk/uZlJcTfKLJyJbJwsQYbSpLOCLataZ4O5MVnnmMbfG//NKJn9kSMvJQZhSwAwoGLYDm1ESGezrvZabgFJnoQv8Si1nAhVGTk9FkFBesxRzq07dmZYwFCnFSX4xt2fDHs1PMpQbeq83aL/PzLCce3kxbYSB5kQlzGtUYayiYXcu0cVRu228VwBLCD+2wTDDoCmRXtPesgrLKUR4WWWb5N2AqAU1mNDC+UEYsENAerOFXWnmwrcTAu5qyZ7GsBMTpipW4Dbou2yqQ0lpA/aB06n1kz1aL6mNqGPaJ+OqoFuc8Ugdhadd+MmjHfFzoI20SZ3b2geCsUMNCsAd6oXMsZdWm8lzjqCGWHFeol0ik/xHMQvuQkkeCsQ28PBxdnUgf7ZGer+TN+2ZLd2kvTBOk6pIVgy5yC6cZ+o1Tloql9hYGa6rT3xcMbXlW+9e5jM2MWXZliVW3ZhaPjptJFDbIfWxJPjz4QvKyJk0zok4muv13Iiwj2bCyefUTRz6psqI4cGaYm9JpscKO2RCJN8UluYGbbWmYQU+Int6LtZj/lv8p6xnVjWxYI+rBPdtkpfFYRp+MJiXjgPw5B6UGuoruv7+vHjOLHOotRo+RdjZt7NqL9dAJnl1Qb2jfW6+d7NYQSI/bAwxO0sk4taQIT6Gsu/8kfZOPC2xk9rphGqCSS/4q3Os0MMjA1bcJLyoWLp13pqhK6bmiiHw0BBXH4fbEp4xjSbpPx4tHXzbdn8oDsHKZkWh3pPC2J/nVl0k/yF1KDVowVtMDXE47k6TGVcBoqe8PDXCG9+vjRpzIidqNo5qebaUZu6riWMWzldz8x3Z/jLWXuDiM7/Yscn0Z2GIlfoeyz+GwP2eTdOw9EUedHjEQuJY32bq8LICimJ4Ht+zMJKUyhwVQyAER8byzQBwTYmYP5U0wdsyIFitphw+/IH8+v08Ia1iBLPQAeAvRfTTIFLCs8foyUrj5Zv2B/wTYIZy6ioUM+qADeXyo45uBLLqkN90Rf6kiTqDld78NxwsfyR5MxtJLVDFkmf2IMMJHTqSfhbi+7QJaC11OOUJTD0v9wo0X/oO5GvZhe0ZaGHnm9zqTopALuFEAxcaQlc4R81wjC4wrIrqWnbcl2dxiBtD73KW+wcC9ymsLf4I8BEmiN25lx/OUc1IHNyXZJYSFkEfaxCEZWKcnbiyf5sqFSSlEqZLc4lUPJFAoP6s1FHVcyO0odWqdadhRZLZC9RCzQgPlMRtji/OXy5phh7diOBZv5UYp5nb+MZ2NAB/eFXm2JLguxjvEstuvTDmZDUb6Uqv++RdhO5gvKf/AcwU38ifaHQ9uvRuDocYwVxZS2nr9rOwZ8nAh+P2o4e0tEXjxFKQGhxXYkn75H3hhfnFYjik/2qunHBBZfcdG148MaNP6DjX33M238T9Zw/GyGx00JMogr2pdP4JAErv9a5yt4YR41KGf8guSOUbOXVARw6+ybh7+meb7w4BeTlj3aZkv8tVGdfIt3lrwVnlbzhLjeQY6PplKp3/a5Kr5yM0T4wJoKQQ6v3vSNmrhpbuAtKxpMILe8CQoo="
password = "12345678a"


# Helper: build the standard EKU tax credentials (cer + key)
def _kemper_credentials():
    return [
        TaxCredential(base64_file=escuela_kemper_urgate_base64_cer, file_type=0, password=password),
        TaxCredential(base64_file=escuela_kemper_urgate_base64_key, file_type=1, password=password),
    ]


# Helper: standard autotransporte with one remolque
def _autotransporte():
    return Autotransporte(
        perm_sct_id="TPAF01",
        num_permiso_sct="NumPermisoSCT1",
        config_vehicular_id="VL",
        peso_bruto_vehicular=Decimal("1"),
        placa_vm="plac892",
        anio_modelo_vm=2020,
        asegura_resp_civil="AseguraRespCivil",
        poliza_resp_civil="123456789",
        remolques=[Remolque(sub_tipo_rem_id="CTR004", placa="VL45K98")],
    )


# Helper: standard mercancia (sin documentacion aduanera)
def _mercancia_base(cantidad_transporta=None, documentacion_aduanera=None, tipo_materia_id=None, descripcion_materia=None):
    return Mercancia(
        bienes_transp_id="11121900",
        descripcion="Accesorios de equipo de telefonía",
        cantidad=Decimal("1.0"),
        clave_unidad_id="XBX",
        material_peligroso_id="No",
        denominacion_generica_prod="DenominacionGenericaProd1",
        denominacion_distintiva_prod="DenominacionDistintivaProd1",
        fabricante="Fabricante1",
        fecha_caducidad="2003-04-02T00:00:00",
        lote_medicamento="LoteMedic1",
        forma_farmaceutica_id="01",
        condiciones_esp_transp_id="01",
        registro_sanitario_folio_autorizacion="RegistroSanita1",
        peso_en_kg=Decimal("1"),
        fraccion_arancelaria_id="6309000100",
        tipo_materia_id=tipo_materia_id,
        descripcion_materia=descripcion_materia,
        documentacion_aduanera=documentacion_aduanera,
        cantidad_transporta=cantidad_transporta or [
            CantidadTransporta(cantidad=Decimal("1"), id_origen="OR101010", id_destino="DE202020")
        ],
    )


# ============================================================================
# 1. FACTURA INGRESO AUTOTRANSPORTE NACIONAL (sin impuestos)
# ============================================================================
def create_factura_autotransporte_nacional():
    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="SerieCCP31",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="URE180429TM6",
            legal_name="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            zip_code="86991",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="No",
                total_dist_rec=Decimal("1"),
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                logistica_inversa_recoleccion_devolucion_id="Sí",
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="URE180429TM6",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="URE180429TM6",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        distancia_recorrida=Decimal("1"),
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                ],
                mercancias=[_mercancia_base()],
                autotransporte=_autotransporte(),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="URE180429TM6",
                        num_licencia="NumLicencia1",
                        nombre_figura="NombreFigura1",
                        domicilio=TipoFiguraDomicilio(
                            calle="Calle1",
                            numero_exterior="NumeroExterior1",
                            numero_interior="NumeroInterior1",
                            colonia_id="Colonia1",
                            localidad_id="Localidad1",
                            referencia="Referencia1",
                            municipio_id="Municipio1",
                            estado_id="Estado1",
                            pais_id="AFG",
                            codigo_postal_id="CodigoPosta1",
                        ),
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# 2. FACTURA INGRESO AUTOTRANSPORTE NACIONAL CON IMPUESTOS
# ============================================================================
def create_factura_autotransporte_nacional_con_impuestos():
    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="SerieCCP31",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="URE180429TM6",
            legal_name="UNIVERSIDAD ROBOTICA ESPAÑOLA",
            zip_code="86991",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("26232.75"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.040000"), tax_flag_code="R"),
                ],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="No",
                total_dist_rec=Decimal("1"),
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                logistica_inversa_recoleccion_devolucion_id="Sí",
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="URE180429TM6",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="URE180429TM6",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        distancia_recorrida=Decimal("1"),
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                ],
                mercancias=[_mercancia_base()],
                autotransporte=_autotransporte(),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="URE180429TM6",
                        num_licencia="NumLicencia1",
                        nombre_figura="NombreFigura1",
                        domicilio=TipoFiguraDomicilio(
                            calle="Calle1",
                            numero_exterior="NumeroExterior1",
                            numero_interior="NumeroInterior1",
                            colonia_id="Colonia1",
                            localidad_id="Localidad1",
                            referencia="Referencia1",
                            municipio_id="Municipio1",
                            estado_id="Estado1",
                            pais_id="AFG",
                            codigo_postal_id="CodigoPosta1",
                        ),
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# 3. FACTURA INGRESO AUTOTRANSPORTE EXTRANJERO (salida)
# ============================================================================
def create_factura_autotransporte_extranjero():
    domicilio_usa = UbicacionDomicilio(
        calle="ST",
        numero_exterior="214",
        colonia_id="N/A",
        referencia="WHITE HOUSE",
        municipio_id="N/A",
        estado_id="TX",
        pais_id="USA",
        codigo_postal_id="N/A",
    )

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="SerieCCP31",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Salida",
                pais_origen_destino_id="USA",
                via_entrada_salida_id="01",
                total_dist_rec=Decimal("1"),
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                logistica_inversa_recoleccion_devolucion_id="Sí",
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        domicilio=domicilio_usa,
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        distancia_recorrida=Decimal("1"),
                        domicilio=domicilio_usa,
                    ),
                ],
                mercancias=[
                    _mercancia_base(tipo_materia_id="05", descripcion_materia="otramateria")
                ],
                autotransporte=_autotransporte(),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="NumLicencia1",
                        nombre_figura="NombreFigura1",
                        domicilio=domicilio_usa,
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# 4. FACTURA INGRESO AUTOTRANSPORTE INTERNACIONAL ADUANERO (entrada)
# ============================================================================
def create_factura_autotransporte_internacional_aduanero():
    domicilio_usa = UbicacionDomicilio(
        calle="ST",
        numero_exterior="214",
        colonia_id="N/A",
        referencia="WHITE HOUSE",
        municipio_id="N/A",
        estado_id="TX",
        pais_id="USA",
        codigo_postal_id="N/A",
    )

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="SerieCCP31",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Entrada",
                pais_origen_destino_id="USA",
                via_entrada_salida_id="01",
                total_dist_rec=Decimal("1"),
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                logistica_inversa_recoleccion_devolucion_id="Sí",
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="IMD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        domicilio=domicilio_usa,
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        distancia_recorrida=Decimal("1"),
                        domicilio=domicilio_usa,
                    ),
                ],
                mercancias=[
                    _mercancia_base(
                        tipo_materia_id="05",
                        descripcion_materia="otramateria",
                        documentacion_aduanera=[
                            DocumentoAduanero(
                                tipo_documento_id="01",
                                num_pedimento="23  43  0472  8000448",
                                rfc_impo="EKU9003173C9",
                            )
                        ],
                    )
                ],
                autotransporte=_autotransporte(),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="NumLicencia1",
                        nombre_figura="NombreFigura1",
                        domicilio=domicilio_usa,
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# HELPERS FERROVIARIO
# ============================================================================
def _transporte_ferroviario() -> TransporteFerroviario:
    return TransporteFerroviario(
        tipo_de_servicio_id="TS01",
        tipo_de_trafico_id="TT01",
        nombre_aseg="NombreAseg",
        num_poliza_seguro="NumPolizaSeguro",
        derechos_de_paso=[
            DerechoDePaso(
                tipo_derecho_de_paso_id="CDP114",
                kilometraje_pagado=Decimal("100"),
            )
        ],
        carros=[
            Carro(
                tipo_carro_id="TC08",
                matricula_carro="A00012",
                guia_carro="123ASD",
                toneladas_netas_carro=Decimal("10"),
            )
        ],
    )


def _figura_ferroviario() -> TipoFigura:
    return TipoFigura(
        tipo_figura_id="02",
        rfc_figura="EKU9003173C9",
        nombre_figura="NombreFigura",
        partes_transporte=[ParteTransporte(parte_transporte_id="PT02")],
        domicilio=TipoFiguraDomicilio(
            calle="calle",
            numero_exterior="211",
            colonia_id="0814",
            localidad_id="01",
            referencia="casa blanca",
            municipio_id="010",
            estado_id="ZAC",
            pais_id="MEX",
            codigo_postal_id="99080",
        ),
    )


# ============================================================================
# EJEMPLO 5: TRANSPORTE FERROVIARIO NACIONAL
# ============================================================================
def create_factura_ferroviario_nacional():
    credentials = _kemper_credentials()

    invoice = Invoice(
        series="Serie",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        payment_form_code="01",
        currency_code="MXN",
        payment_method_code="PPD",
        expedition_zip_code="99080",
        cfdi_type_id="T",
        tax_object_id="01",
        issuer=InvoiceIssuer(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
        ),
        recipient=InvoiceRecipient(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
            tax_zip_code="99080",
            cfdi_use_id="CP01",
        ),
        items=[
            InvoiceItem(
                quantity=Decimal("1"),
                unit_id="E48",
                unit_price=Decimal("0"),
                description="Flete",
                product_id="78101801",
                tax_object_id="01",
            )
        ],
        tax_credentials=credentials,
        complements=[
            InvoiceComplement(
                lading=LadingComplement(
                    transp_internac_id="No",
                    total_dist_rec=Decimal("500"),
                    peso_neto_total=Decimal("10"),
                    unidad_peso_id="XBX",
                    ubicaciones=[
                        Ubicacion(
                            tipo_ubicacion="Origen",
                            id_ubicacion="OR101010",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T10:00:00",
                            distancia_recorrida=Decimal("100"),
                            domicilio=UbicacionDomicilio(
                                calle="calle",
                                numero_exterior="211",
                                colonia_id="0814",
                                localidad_id="01",
                                referencia="casa blanca",
                                municipio_id="010",
                                estado_id="ZAC",
                                pais_id="MEX",
                                codigo_postal_id="99080",
                            ),
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202021",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T11:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97001",
                            nombre_estacion="MONTERREY",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202022",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T12:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97002",
                            nombre_estacion="GUADALAJARA",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202023",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T13:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97003",
                            nombre_estacion="QUERETARO",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202024",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T14:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97004",
                            nombre_estacion="TOLUCA",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202025",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T15:00:00",
                            distancia_recorrida=Decimal("100"),
                            domicilio=UbicacionDomicilio(
                                calle="calle",
                                numero_exterior="211",
                                colonia_id="0814",
                                localidad_id="01",
                                referencia="casa blanca",
                                municipio_id="010",
                                estado_id="ZAC",
                                pais_id="MEX",
                                codigo_postal_id="99080",
                            ),
                        ),
                    ],
                    mercancias=[
                        _mercancia_base(
                            cantidad_transporta=[
                                CantidadTransporta(
                                    cantidad=Decimal("100"),
                                    id_origen="OR101010",
                                    id_destino="DE202025",
                                )
                            ],
                            documentacion_aduanera=None,
                            tipo_materia_id=None,
                            descripcion_materia=None,
                        )
                    ],
                    transporte_ferroviario=_transporte_ferroviario(),
                    tipos_figura=[_figura_ferroviario()],
                )
            )
        ],
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura ferroviario nacional creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# EJEMPLO 6: TRANSPORTE FERROVIARIO EXTRANJERO (SALIDA)
# ============================================================================
def create_factura_ferroviario_extranjero():
    credentials = _kemper_credentials()

    invoice = Invoice(
        series="Serie",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        payment_form_id="01",
        currency_id="MXN",
        payment_method_id="PPD",
        expedition_zip_code="99080",
        cfdi_type_id="T",
        tax_object_id="01",
        issuer=InvoiceIssuer(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
        ),
        recipient=InvoiceRecipient(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
            tax_zip_code="99080",
            cfdi_use_id="CP01",
        ),
        items=[
            InvoiceItem(
                quantity=Decimal("1"),
                unit_id="E48",
                unit_price=Decimal("0"),
                description="Flete",
                product_id="78101801",
                tax_object_id="01",
            )
        ],
        tax_credentials=credentials,
        complements=[
            InvoiceComplement(
                lading=LadingComplement(
                    transp_internac_id="Sí",
                    entrada_salida_merc_id="Salida",
                    pais_origen_destino_id="USA",
                    via_entrada_salida_id="04",
                    total_dist_rec=Decimal("500"),
                    peso_neto_total=Decimal("10"),
                    unidad_peso_id="XBX",
                    regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
                    ubicaciones=[
                        Ubicacion(
                            tipo_ubicacion="Origen",
                            id_ubicacion="OR101010",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T10:00:00",
                            distancia_recorrida=Decimal("100"),
                            domicilio=UbicacionDomicilio(
                                calle="calle",
                                numero_exterior="211",
                                colonia_id="0814",
                                localidad_id="01",
                                referencia="casa blanca",
                                municipio_id="010",
                                estado_id="ZAC",
                                pais_id="MEX",
                                codigo_postal_id="99080",
                            ),
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202021",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T11:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97001",
                            nombre_estacion="MONTERREY",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202022",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T12:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97002",
                            nombre_estacion="GUADALAJARA",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202023",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T13:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97003",
                            nombre_estacion="QUERETARO",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202024",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T14:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97004",
                            nombre_estacion="TOLUCA",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202025",
                            rfc_remitente_destinatario="XEXX010101000",
                            nombre_remitente_destinatario="DESTINATARIO EXTRANJERO",
                            num_reg_id_trib="01010101",
                            residencia_fiscal_id="USA",
                            fecha_hora_salida_llegada="2024-11-12T15:00:00",
                            distancia_recorrida=Decimal("100"),
                            domicilio=UbicacionDomicilio(
                                calle="Main Street",
                                numero_exterior="100",
                                municipio_id="City",
                                estado_id="TX",
                                pais_id="USA",
                                codigo_postal_id="78500",
                            ),
                        ),
                    ],
                    mercancias=[
                        _mercancia_base(
                            cantidad_transporta=[
                                CantidadTransporta(
                                    cantidad=Decimal("100"),
                                    id_origen="OR101010",
                                    id_destino="DE202025",
                                )
                            ],
                            documentacion_aduanera=None,
                            tipo_materia_id="05",
                            descripcion_materia="otramateria",
                        )
                    ],
                    transporte_ferroviario=_transporte_ferroviario(),
                    tipos_figura=[_figura_ferroviario()],
                )
            )
        ],
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura ferroviario extranjero (salida) creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# EJEMPLO 7: TRANSPORTE FERROVIARIO INTERNACIONAL ADUANERO (ENTRADA)
# ============================================================================
def create_factura_ferroviario_internacional_aduanero():
    credentials = _kemper_credentials()

    invoice = Invoice(
        series="Serie",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        payment_form_id="01",
        currency_id="MXN",
        payment_method_id="PPD",
        expedition_zip_code="99080",
        cfdi_type_id="T",
        tax_object_id="01",
        issuer=InvoiceIssuer(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
        ),
        recipient=InvoiceRecipient(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
            tax_zip_code="99080",
            cfdi_use_id="CP01",
        ),
        items=[
            InvoiceItem(
                quantity=Decimal("1"),
                unit_id="E48",
                unit_price=Decimal("0"),
                description="Flete",
                product_id="78101801",
                tax_object_id="01",
            )
        ],
        tax_credentials=credentials,
        complements=[
            InvoiceComplement(
                lading=LadingComplement(
                    transp_internac_id="Sí",
                    entrada_salida_merc_id="Entrada",
                    pais_origen_destino_id="AFG",
                    via_entrada_salida_id="04",
                    total_dist_rec=Decimal("500"),
                    peso_neto_total=Decimal("10"),
                    unidad_peso_id="XBX",
                    regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="IMD")],
                    ubicaciones=[
                        Ubicacion(
                            tipo_ubicacion="Origen",
                            id_ubicacion="OR101010",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T10:00:00",
                            distancia_recorrida=Decimal("100"),
                            domicilio=UbicacionDomicilio(
                                calle="calle",
                                numero_exterior="211",
                                colonia_id="0814",
                                localidad_id="01",
                                referencia="casa blanca",
                                municipio_id="010",
                                estado_id="ZAC",
                                pais_id="MEX",
                                codigo_postal_id="99080",
                            ),
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202021",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T11:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97001",
                            nombre_estacion="MONTERREY",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202022",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T12:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97002",
                            nombre_estacion="GUADALAJARA",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202023",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T13:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97003",
                            nombre_estacion="QUERETARO",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202024",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T14:00:00",
                            distancia_recorrida=Decimal("100"),
                            num_estacion_id="97004",
                            nombre_estacion="TOLUCA",
                            tipo_estacion_id="01",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202025",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T15:00:00",
                            distancia_recorrida=Decimal("100"),
                            nombre_estacion="HUEHUETOCA",
                            domicilio=UbicacionDomicilio(
                                calle="calle",
                                numero_exterior="211",
                                colonia_id="0203",
                                localidad_id="01",
                                referencia="casa blanca",
                                municipio_id="006",
                                estado_id="COA",
                                pais_id="MEX",
                                codigo_postal_id="25900",
                            ),
                        ),
                    ],
                    mercancias=[
                        _mercancia_base(
                            cantidad_transporta=[
                                CantidadTransporta(
                                    cantidad=Decimal("100"),
                                    id_origen="OR101010",
                                    id_destino="DE202025",
                                )
                            ],
                            documentacion_aduanera=[
                                DocumentoAduanero(
                                    tipo_documento_id="01",
                                    num_pedimento="23  43  0472  8000448",
                                    rfc_impo="EKU9003173C9",
                                )
                            ],
                            tipo_materia_id="05",
                            descripcion_materia="otramateria",
                        )
                    ],
                    transporte_ferroviario=_transporte_ferroviario(),
                    tipos_figura=[_figura_ferroviario()],
                )
            )
        ],
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura ferroviario intl aduanero (entrada) creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# EJEMPLO 8: TRANSPORTE AÉREO NACIONAL
# ============================================================================
def create_factura_aereo_nacional():
    credentials = _kemper_credentials()

    invoice = Invoice(
        series="Serie",
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        payment_form_id="01",
        currency_id="MXN",
        payment_method_id="PPD",
        expedition_zip_code="99080",
        cfdi_type_id="T",
        tax_object_id="01",
        issuer=InvoiceIssuer(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
        ),
        recipient=InvoiceRecipient(
            tax_id="EKU9003173C9",
            tax_name="ESCUELA KEMPER URGATE",
            tax_regime_id="601",
            tax_zip_code="99080",
            cfdi_use_id="CP01",
        ),
        items=[
            InvoiceItem(
                quantity=Decimal("1"),
                unit_id="E48",
                unit_price=Decimal("0"),
                description="Flete",
                product_id="78101801",
                tax_object_id="01",
            )
        ],
        tax_credentials=credentials,
        complements=[
            InvoiceComplement(
                lading=LadingComplement(
                    transp_internac_id="No",
                    peso_neto_total=Decimal("10"),
                    unidad_peso_id="XBX",
                    ubicaciones=[
                        Ubicacion(
                            tipo_ubicacion="Origen",
                            id_ubicacion="OR101010",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T10:00:00",
                            num_estacion_id="EA0417",
                            nombre_estacion="Loreto",
                            tipo_estacion_id="02",
                        ),
                        Ubicacion(
                            tipo_ubicacion="Destino",
                            id_ubicacion="DE202025",
                            rfc_remitente_destinatario="EKU9003173C9",
                            nombre_remitente_destinatario="ESCUELA KEMPER URGATE",
                            fecha_hora_salida_llegada="2024-11-12T12:00:00",
                            num_estacion_id="EA0418",
                            nombre_estacion="Los Cabos",
                            tipo_estacion_id="02",
                        ),
                    ],
                    mercancias=[
                        Mercancia(
                            bienes_transp_id="11121900",
                            descripcion="Accesorios de equipo de telefonía",
                            cantidad=Decimal("100"),
                            clave_unidad_id="H87",
                            peso_en_kg=Decimal("10"),
                            valor_mercancia=Decimal("100"),
                            moneda_id="MXN",
                            cantidad_transporta=[
                                CantidadTransporta(
                                    cantidad=Decimal("100"),
                                    id_origen="OR101010",
                                    id_destino="DE202025",
                                )
                            ],
                        )
                    ],
                    transporte_aereo=TransporteAereo(
                        perm_sct_id="TPAF01",
                        num_permiso_sct="Demo",
                        matricula_aeronave="61E5-WZ",
                        nombre_aseg="NombreAseg",
                        num_poliza_seguro="NumPolizaSeguro",
                        numero_guia="acUbYlBVTmlzx",
                        lugar_contrato="LugarContrato",
                        codigo_transportista_id="CA001",
                        rfc_embarcador="EKU9003173C9",
                        nombre_embarcador="Embarcador",
                    ),
                    tipos_figura=[
                        TipoFigura(
                            tipo_figura_id="01",
                            rfc_figura="EKU9003173C9",
                            num_licencia="a234567890",
                            nombre_figura="NombreFigura",
                        )
                    ],
                )
            )
        ],
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura aéreo nacional creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# HELPERS MARITIMO
# ============================================================================
def _transporte_maritimo_base() -> TransporteMaritimo:
    return TransporteMaritimo(
        perm_sct_id="TPAF01",
        num_permiso_sct="NumPermisoSCT1",
        nombre_aseg="NombreAseg1",
        num_poliza_seguro="NumPolizaSeguro1",
        tipo_embarcacion_id="B01",
        matricula="Matricula1",
        numero_omi="IMO1234567",
        anio_embarcacion=2003,
        nombre_embarc="NombreEmbarc1",
        nacionalidad_embarc_id="AFG",
        unidades_de_arq_bruto=Decimal("0.001"),
        tipo_carga_id="CGS",
        eslora=Decimal("0.01"),
        manga=Decimal("0.01"),
        calado=Decimal("0.01"),
        puntal=Decimal("0.01"),
        linea_naviera="LineaNaviera1",
        nombre_agente_naviero="NombreAgenteNaviero1",
        num_autorizacion_naviero_id="ANC001/2022",
        num_viaje="NumViaje1",
        num_conoc_embarc="NumConocEmbarc1",
        permiso_temp_navegacion="PermisoTempNavegac1",
        contenedores=[
            ContenedorMaritimo(
                tipo_contenedor_id="CM011",
                id_ccp_relacionado="CCCBCD94-870A-4332-A52A-A52AA52AA52A",
                placa_vm_ccp="JNG7683",
                fecha_certificacion_ccp="2024-06-20T11:11:00",
                remolques_ccp=[
                    RemolqueCCP(
                        sub_tipo_rem_ccp_id="CTR001",
                        placa_ccp="JNG7636",
                    )
                ],
            )
        ],
    )


# ============================================================================
# EJEMPLO 9: TRANSPORTE AÉREO EXTRANJERO (SALIDA)
# ============================================================================
def create_factura_aereo_extranjero():
    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Salida",
                pais_origen_destino_id="USA",
                via_entrada_salida_id="03",
                unidad_peso_id="XBX",
                peso_neto_total=Decimal("10"),
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        num_estacion_id="EA0417",
                        nombre_estacion="Loreto",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        tipo_estacion_id="01",
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="XEXX010101000",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        num_estacion_id="EA0143",
                        nombre_estacion="Phoenix-Mesa Gateway",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        domicilio=UbicacionDomicilio(
                            calle="ST",
                            numero_exterior="12344",
                            colonia_id="N/A",
                            referencia="WHITE HOUSE",
                            municipio_id="N/A",
                            estado_id="TX",
                            pais_id="USA",
                            codigo_postal_id="12345",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2028-01-01T00:00:00",
                        lote_medicamento="LoteMedic1",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        valor_mercancia=Decimal("100"),
                        moneda_id="MXN",
                        tipo_materia_id="05",
                        descripcion_materia="otramateria",
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                    )
                ],
                transporte_aereo=TransporteAereo(
                    perm_sct_id="TPAF01",
                    num_permiso_sct="Demo",
                    matricula_aeronave="61E5-WZ",
                    nombre_aseg="NombreAseg",
                    num_poliza_seguro="NumPolizaSeguro",
                    numero_guia="acUbYlBVTmlzx",
                    lugar_contrato="LugarContrato",
                    codigo_transportista_id="CA001",
                    rfc_embarcador="EKU9003173C9",
                    nombre_embarcador="Embarcador",
                ),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="a234567890",
                        nombre_figura="NombreFigura",
                    )
                ],
            )
        ),
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura aéreo extranjero (salida) creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# EJEMPLO 10: TRANSPORTE AÉREO INTERNACIONAL ADUANERO (ENTRADA)
# ============================================================================
def create_factura_aereo_internacional_aduanero():
    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Entrada",
                pais_origen_destino_id="AFG",
                via_entrada_salida_id="03",
                unidad_peso_id="XBX",
                peso_neto_total=Decimal("10"),
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="IMD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        num_estacion_id="EA0417",
                        nombre_estacion="Loreto",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        tipo_estacion_id="01",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        num_estacion_id="EA0418",
                        nombre_estacion="Los Cabos",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        tipo_estacion_id="03",
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2028-01-01T00:00:00",
                        lote_medicamento="LoteMedic1",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        valor_mercancia=Decimal("100"),
                        moneda_id="MXN",
                        tipo_materia_id="05",
                        descripcion_materia="otramateria",
                        documentacion_aduanera=[
                            DocumentoAduanero(
                                tipo_documento_id="01",
                                num_pedimento="23  43  0472  8000448",
                                rfc_impo="EKU9003173C9",
                            )
                        ],
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                    )
                ],
                transporte_aereo=TransporteAereo(
                    perm_sct_id="TPAF01",
                    num_permiso_sct="Demo",
                    matricula_aeronave="61E5-WZ",
                    nombre_aseg="NombreAseg",
                    num_poliza_seguro="NumPolizaSeguro",
                    numero_guia="acUbYlBVTmlzx",
                    lugar_contrato="LugarContrato",
                    codigo_transportista_id="CA001",
                    rfc_embarcador="EKU9003173C9",
                    nombre_embarcador="Embarcador",
                ),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="a234567890",
                        nombre_figura="NombreFigura",
                    )
                ],
            )
        ),
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura aéreo intl aduanero (entrada) creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# EJEMPLO 11: TRANSPORTE MARÍTIMO NACIONAL
# ============================================================================
def create_factura_maritimo_nacional():
    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="No",
                unidad_peso_id="XBX",
                peso_neto_total=Decimal("1"),
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        num_estacion_id="PM001",
                        nombre_estacion="Rosarito",
                        navegacion_trafico_id="Altura",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        tipo_estacion_id="01",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        num_estacion_id="PM001",
                        nombre_estacion="Rosarito",
                        navegacion_trafico_id="Altura",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        tipo_estacion_id="03",
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2028-01-01T00:00:00",
                        lote_medicamento="LoteMedic1",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        valor_mercancia=Decimal("100"),
                        moneda_id="MXN",
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                        detalle_mercancia=DetalleMercancia(
                            unidad_peso_merc_id="Tu",
                            peso_bruto=Decimal("1"),
                            peso_neto=Decimal("1"),
                            peso_tara=Decimal("0.001"),
                            num_piezas=1,
                        ),
                    )
                ],
                transporte_maritimo=_transporte_maritimo_base(),
                tipos_figura=[_figura_ferroviario()],
            )
        ),
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura marítimo nacional creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# EJEMPLO 12: TRANSPORTE MARÍTIMO EXTRANJERO (SALIDA)
# ============================================================================
def create_factura_maritimo_extranjero():
    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Salida",
                pais_origen_destino_id="USA",
                via_entrada_salida_id="02",
                unidad_peso_id="XBX",
                peso_neto_total=Decimal("1"),
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        num_estacion_id="PM001",
                        nombre_estacion="Rosarito",
                        navegacion_trafico_id="Altura",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        tipo_estacion_id="01",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="XEXX010101000",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        num_estacion_id="PM120",
                        nombre_estacion="NombreEstacion",
                        navegacion_trafico_id="Altura",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        domicilio=UbicacionDomicilio(
                            calle="ST",
                            numero_exterior="12345",
                            colonia_id="N/A",
                            referencia="N/A",
                            municipio_id="N/A",
                            estado_id="TX",
                            pais_id="USA",
                            codigo_postal_id="12345",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2028-01-01T00:00:00",
                        lote_medicamento="LoteMedic1",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        valor_mercancia=Decimal("100"),
                        moneda_id="MXN",
                        tipo_materia_id="05",
                        descripcion_materia="otramateria",
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                        detalle_mercancia=DetalleMercancia(
                            unidad_peso_merc_id="Tu",
                            peso_bruto=Decimal("1"),
                            peso_neto=Decimal("1"),
                            peso_tara=Decimal("0.001"),
                            num_piezas=1,
                        ),
                    )
                ],
                transporte_maritimo=_transporte_maritimo_base(),
                tipos_figura=[_figura_ferroviario()],
            )
        ),
    )

    client = FiscalApiClient(settings=settings)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print("Factura marítimo extranjero (salida) creada:", response.data)
    else:
        print("Error:", response.message)


# ============================================================================
# EJEMPLO 13: TRANSPORTE MARÍTIMO INTERNACIONAL ADUANERO (ENTRADA) - INGRESO
# ============================================================================
def create_factura_maritimo_internacional_aduanero():
    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="CP3.1",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Entrada",
                pais_origen_destino_id="AFG",
                via_entrada_salida_id="01",
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                peso_neto_total=Decimal("1"),
                regimen_aduaneros=[
                    RegimenAduanero(regimen_aduanero_id="IMD"),
                    RegimenAduanero(regimen_aduanero_id="IMD"),
                ],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        num_estacion_id="EA0417",
                        nombre_estacion="Loreto",
                        navegacion_trafico_id="Altura",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        tipo_estacion_id="01",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        num_estacion_id="PM001",
                        nombre_estacion="Rosarito",
                        navegacion_trafico_id="Altura",
                        fecha_hora_salida_llegada="2023-08-01T04:00:01",
                        tipo_estacion_id="02",
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2003-04-02T00:00:00",
                        lote_medicamento="LoteMedic1",
                        forma_farmaceutica_id="01",
                        condiciones_esp_transp_id="01",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1.50"),
                        valor_mercancia=Decimal("100"),
                        moneda_id="MXN",
                        fraccion_arancelaria_id="6309000100",
                        tipo_materia_id="05",
                        descripcion_materia="otramateria",
                        documentacion_aduanera=[
                            DocumentoAduanero(
                                tipo_documento_id="01",
                                num_pedimento="23  43  0472  8000448",
                                rfc_impo="EKU9003173C9",
                            )
                        ],
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                                cves_transporte_id="02",
                            )
                        ],
                        detalle_mercancia=DetalleMercancia(
                            unidad_peso_merc_id="X1A",
                            peso_bruto=Decimal("1.50"),
                            peso_neto=Decimal("1.00"),
                            peso_tara=Decimal("0.50"),
                        ),
                    )
                ],
                transporte_maritimo=TransporteMaritimo(
                    perm_sct_id="TPAF01",
                    num_permiso_sct="NumPermisoSCT1",
                    nombre_aseg="NombreAseg1",
                    num_poliza_seguro="NumPolizaSeguro1",
                    tipo_embarcacion_id="B01",
                    matricula="Matricula1",
                    numero_omi="IMO1234567",
                    anio_embarcacion=2003,
                    nombre_embarc="NombreEmbarc1",
                    nacionalidad_embarc_id="AFG",
                    unidades_de_arq_bruto=Decimal("0.001"),
                    tipo_carga_id="CGS",
                    eslora=Decimal("0.01"),
                    manga=Decimal("0.01"),
                    calado=Decimal("0.01"),
                    puntal=Decimal("0.01"),
                    linea_naviera="LineaNaviera1",
                    nombre_agente_naviero="NombreAgenteNaviero1",
                    num_autorizacion_naviero_id="ANC001/2022",
                    num_viaje="NumViaje1",
                    num_conoc_embarc="NumConocEmbarc1",
                    permiso_temp_navegacion="PermisoTempNavegac1",
                    contenedores=[
                        ContenedorMaritimo(
                            tipo_contenedor_id="CM011",
                            id_ccp_relacionado="CCCBCD94-870A-4332-A52A-A52AA52AA52A",
                            placa_vm_ccp="JNG7683",
                            fecha_certificacion_ccp="2024-06-20T11:11:00",
                            remolques_ccp=[
                                RemolqueCCP(
                                    sub_tipo_rem_ccp_id="CTR001",
                                    placa_ccp="JNG7636",
                                )
                            ],
                        )
                    ],
                ),
                transporte_aereo=TransporteAereo(
                    perm_sct_id="TPAF01",
                    num_permiso_sct="Demo",
                    matricula_aeronave="61E5-WZ",
                    nombre_aseg="NombreAseg",
                    num_poliza_seguro="NumPolizaSeguro",
                    numero_guia="acUbYlBVTmlzx",
                    lugar_contrato="LugarContrato",
                    codigo_transportista_id="CA001",
                    rfc_embarcador="EKU9003173C9",
                    nombre_embarcador="Embarcador",
                ),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="NumLicencia1",
                        nombre_figura="NombreFigura1",
                        domicilio=TipoFiguraDomicilio(
                            calle="Calle1",
                            numero_exterior="NumeroExterior1",
                            numero_interior="NumeroInterior1",
                            colonia_id="Colonia1",
                            localidad_id="Localidad1",
                            referencia="Referencia1",
                            municipio_id="Municipio1",
                            estado_id="Estado1",
                            pais_id="AFG",
                            codigo_postal_id="CodigoPosta1",
                        ),
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 14: TRASLADO AUTOTRANSPORTE NACIONAL
# ============================================================================
def create_factura_traslado_autotransporte_nacional():
    invoice = Invoice(
        version_code="4.0",
        currency_code="XXX",
        type_code="T",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="No",
                total_dist_rec=Decimal("1"),
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                logistica_inversa_recoleccion_devolucion_id="Sí",
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        distancia_recorrida=Decimal("1"),
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2028-01-01T00:00:00",
                        lote_medicamento="LoteMedic1",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                    )
                ],
                autotransporte=_autotransporte(),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="a234567890",
                        nombre_figura="NombreFigura",
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 15: TRASLADO AUTOTRANSPORTE EXTRANJERO (SALIDA)
# ============================================================================
def create_factura_traslado_autotransporte_extranjero():
    domicilio_usa = UbicacionDomicilio(
        calle="ST",
        numero_exterior="214",
        colonia_id="N/A",
        referencia="WHITE HOUSE",
        municipio_id="N/A",
        estado_id="TX",
        pais_id="USA",
        codigo_postal_id="N/A",
    )

    invoice = Invoice(
        version_code="4.0",
        currency_code="XXX",
        type_code="T",
        expedition_zip_code="42501",
        series="SerieCCP31",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Salida",
                pais_origen_destino_id="USA",
                via_entrada_salida_id="01",
                total_dist_rec=Decimal("1"),
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                logistica_inversa_recoleccion_devolucion_id="Sí",
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        domicilio=domicilio_usa,
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        distancia_recorrida=Decimal("1"),
                        domicilio=domicilio_usa,
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2003-04-02T00:00:00",
                        lote_medicamento="LoteMedic1",
                        forma_farmaceutica_id="01",
                        condiciones_esp_transp_id="01",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        fraccion_arancelaria_id="6309000100",
                        tipo_materia_id="05",
                        descripcion_materia="otramateria",
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                    )
                ],
                autotransporte=_autotransporte(),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="NumLicencia1",
                        nombre_figura="NombreFigura1",
                        domicilio=domicilio_usa,
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 16: TRASLADO AUTOTRANSPORTE INTERNACIONAL ADUANERO (ENTRADA)
# ============================================================================
def create_factura_traslado_autotransporte_internacional_aduanero():
    domicilio_usa = UbicacionDomicilio(
        calle="ST",
        numero_exterior="214",
        colonia_id="N/A",
        referencia="WHITE HOUSE",
        municipio_id="N/A",
        estado_id="TX",
        pais_id="USA",
        codigo_postal_id="N/A",
    )

    invoice = Invoice(
        version_code="4.0",
        currency_code="XXX",
        type_code="T",
        expedition_zip_code="42501",
        series="SerieCCP31",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Entrada",
                pais_origen_destino_id="USA",
                via_entrada_salida_id="01",
                total_dist_rec=Decimal("1"),
                registro_istmo_id="Sí",
                ubicacion_polo_origen_id="01",
                ubicacion_polo_destino_id="01",
                unidad_peso_id="XBX",
                logistica_inversa_recoleccion_devolucion_id="Sí",
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="IMD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        domicilio=domicilio_usa,
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="XEXX010101000",
                        num_reg_id_trib="01010101",
                        residencia_fiscal_id="USA",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        distancia_recorrida=Decimal("1"),
                        domicilio=domicilio_usa,
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2003-04-02T00:00:00",
                        lote_medicamento="LoteMedic1",
                        forma_farmaceutica_id="01",
                        condiciones_esp_transp_id="01",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        fraccion_arancelaria_id="6309000100",
                        tipo_materia_id="05",
                        descripcion_materia="otramateria",
                        documentacion_aduanera=[
                            DocumentoAduanero(
                                tipo_documento_id="01",
                                num_pedimento="23  43  0472  8000448",
                                rfc_impo="EKU9003173C9",
                            )
                        ],
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                    )
                ],
                autotransporte=_autotransporte(),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="NumLicencia1",
                        nombre_figura="NombreFigura1",
                        domicilio=domicilio_usa,
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# HELPERS FERROVIARIO TRASLADO
# ============================================================================
def _ubicaciones_ferroviario_traslado_nacional():
    return [
        Ubicacion(
            tipo_ubicacion="Origen",
            id_ubicacion="OR101010",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario1",
            num_estacion_id="Q0736",
            nombre_estacion="SANTO NINO",
            fecha_hora_salida_llegada="2023-08-01T00:00:00",
            tipo_estacion_id="01",
            domicilio=UbicacionDomicilio(
                calle="Calle1",
                numero_exterior="211",
                numero_interior="212",
                colonia_id="1957",
                localidad_id="13",
                referencia="casa blanca",
                municipio_id="011",
                estado_id="CMX",
                pais_id="MEX",
                codigo_postal_id="13250",
            ),
        ),
        Ubicacion(
            tipo_ubicacion="Destino",
            id_ubicacion="DE202021",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario2",
            num_estacion_id="SC283",
            nombre_estacion="HUAXTITLA",
            fecha_hora_salida_llegada="2023-08-01T01:00:01",
            tipo_estacion_id="02",
            distancia_recorrida=Decimal("100"),
        ),
        Ubicacion(
            tipo_ubicacion="Destino",
            id_ubicacion="DE202022",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario2",
            num_estacion_id="TG0",
            nombre_estacion="NAVOJOA",
            fecha_hora_salida_llegada="2023-08-01T02:00:01",
            tipo_estacion_id="02",
            distancia_recorrida=Decimal("100"),
        ),
        Ubicacion(
            tipo_ubicacion="Destino",
            id_ubicacion="DE202023",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario2",
            num_estacion_id="E0029",
            nombre_estacion="TRES JAGUEYES",
            fecha_hora_salida_llegada="2023-08-01T03:00:01",
            tipo_estacion_id="02",
            distancia_recorrida=Decimal("100"),
        ),
        Ubicacion(
            tipo_ubicacion="Destino",
            id_ubicacion="DE202024",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario2",
            num_estacion_id="TI032",
            nombre_estacion="NAVOLATO",
            fecha_hora_salida_llegada="2023-08-01T04:00:01",
            tipo_estacion_id="02",
            distancia_recorrida=Decimal("100"),
        ),
    ]


def _transporte_ferroviario_traslado() -> TransporteFerroviario:
    return TransporteFerroviario(
        tipo_de_servicio_id="TS01",
        tipo_de_trafico_id="TT01",
        derechos_de_paso=[
            DerechoDePaso(tipo_derecho_de_paso_id="CDP114", kilometraje_pagado=Decimal("100"))
        ],
        carros=[
            Carro(
                tipo_carro_id="TC08",
                matricula_carro="A00012",
                guia_carro="123ASD",
                toneladas_netas_carro=Decimal("10"),
            )
        ],
    )


def _figura_traslado_ferroviario() -> TipoFigura:
    return TipoFigura(
        tipo_figura_id="02",
        rfc_figura="EKU9003173C9",
        nombre_figura="NombreFigura",
        partes_transporte=[ParteTransporte(parte_transporte_id="PT02")],
        domicilio=UbicacionDomicilio(
            calle="calle",
            numero_exterior="211",
            colonia_id="0814",
            localidad_id="01",
            referencia="casa blanca",
            municipio_id="010",
            estado_id="ZAC",
            pais_id="MEX",
            codigo_postal_id="99080",
        ),
    )


def _invoice_traslado_ferroviario_base(lading: LadingComplement) -> Invoice:
    return Invoice(
        version_code="4.0",
        currency_code="XXX",
        type_code="T",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(lading=lading),
    )


# ============================================================================
# EJEMPLO 17: TRASLADO FERROVIARIO NACIONAL
# ============================================================================
def create_factura_traslado_ferroviario_nacional():
    destino_final = Ubicacion(
        tipo_ubicacion="Destino",
        id_ubicacion="DE202025",
        rfc_remitente_destinatario="EKU9003173C9",
        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
        num_estacion_id="JM047",
        nombre_estacion="HUEHUETOCA",
        fecha_hora_salida_llegada="2023-08-01T05:00:01",
        tipo_estacion_id="03",
        distancia_recorrida=Decimal("100"),
        domicilio=UbicacionDomicilio(
            calle="Calle2",
            numero_exterior="214",
            numero_interior="215",
            colonia_id="0347",
            localidad_id="23",
            referencia="casa negra",
            municipio_id="004",
            estado_id="COA",
            pais_id="MEX",
            codigo_postal_id="25350",
        ),
    )

    lading = LadingComplement(
        transp_internac_id="No",
        total_dist_rec=Decimal("500"),
        registro_istmo_id="Sí",
        ubicacion_polo_origen_id="01",
        ubicacion_polo_destino_id="01",
        unidad_peso_id="XBX",
        peso_neto_total=Decimal("10"),
        ubicaciones=_ubicaciones_ferroviario_traslado_nacional() + [destino_final],
        mercancias=[
            Mercancia(
                bienes_transp_id="11121900",
                descripcion="Accesorios de equipo de telefonía",
                cantidad=Decimal("1.0"),
                clave_unidad_id="XBX",
                material_peligroso_id="No",
                denominacion_generica_prod="DenominacionGenericaProd1",
                denominacion_distintiva_prod="DenominacionDistintivaProd1",
                fabricante="Fabricante1",
                fecha_caducidad="2028-01-01T00:00:00",
                lote_medicamento="LoteMedic1",
                registro_sanitario_folio_autorizacion="RegistroSanita1",
                peso_en_kg=Decimal("1"),
                cantidad_transporta=[
                    CantidadTransporta(cantidad=Decimal("1"), id_origen="OR101010", id_destino="DE202025")
                ],
            )
        ],
        transporte_ferroviario=_transporte_ferroviario_traslado(),
        tipos_figura=[_figura_traslado_ferroviario()],
    )

    invoice = _invoice_traslado_ferroviario_base(lading)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 18: TRASLADO FERROVIARIO EXTRANJERO (SALIDA)
# ============================================================================
def create_factura_traslado_ferroviario_extranjero():
    destino_final = Ubicacion(
        tipo_ubicacion="Destino",
        id_ubicacion="DE202025",
        rfc_remitente_destinatario="XEXX010101000",
        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
        num_reg_id_trib="01010101",
        residencia_fiscal_id="USA",
        num_estacion_id="EF0001",
        nombre_estacion="NombreEstacion",
        fecha_hora_salida_llegada="2023-08-01T05:00:01",
        distancia_recorrida=Decimal("100"),
        domicilio=UbicacionDomicilio(
            calle="ST",
            numero_exterior="1234",
            colonia_id="1234",
            referencia="WHITE HOUSE",
            municipio_id="1234",
            estado_id="TX",
            pais_id="USA",
            codigo_postal_id="12345",
        ),
    )

    lading = LadingComplement(
        transp_internac_id="Sí",
        entrada_salida_merc_id="Salida",
        pais_origen_destino_id="USA",
        via_entrada_salida_id="04",
        total_dist_rec=Decimal("500"),
        registro_istmo_id="Sí",
        ubicacion_polo_origen_id="01",
        ubicacion_polo_destino_id="01",
        unidad_peso_id="XBX",
        peso_neto_total=Decimal("10"),
        regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
        ubicaciones=_ubicaciones_ferroviario_traslado_nacional() + [destino_final],
        mercancias=[
            Mercancia(
                bienes_transp_id="11121900",
                descripcion="Accesorios de equipo de telefonía",
                cantidad=Decimal("1.0"),
                clave_unidad_id="XBX",
                material_peligroso_id="No",
                denominacion_generica_prod="DenominacionGenericaProd1",
                denominacion_distintiva_prod="DenominacionDistintivaProd1",
                fabricante="Fabricante1",
                fecha_caducidad="2028-01-01T00:00:00",
                lote_medicamento="LoteMedic1",
                registro_sanitario_folio_autorizacion="RegistroSanita1",
                peso_en_kg=Decimal("1"),
                tipo_materia_id="05",
                descripcion_materia="otramateria",
                cantidad_transporta=[
                    CantidadTransporta(cantidad=Decimal("1"), id_origen="OR101010", id_destino="DE202025")
                ],
            )
        ],
        transporte_ferroviario=_transporte_ferroviario_traslado(),
        tipos_figura=[_figura_traslado_ferroviario()],
    )

    invoice = _invoice_traslado_ferroviario_base(lading)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 19: TRASLADO FERROVIARIO INTERNACIONAL ADUANERO (ENTRADA)
# ============================================================================
def create_factura_traslado_ferroviario_internacional_aduanero():
    destino_final = Ubicacion(
        tipo_ubicacion="Destino",
        id_ubicacion="DE202025",
        rfc_remitente_destinatario="EKU9003173C9",
        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
        num_estacion_id="JM047",
        nombre_estacion="HUEHUETOCA",
        fecha_hora_salida_llegada="2023-08-01T05:00:01",
        tipo_estacion_id="03",
        distancia_recorrida=Decimal("100"),
        domicilio=UbicacionDomicilio(
            calle="Calle2",
            numero_exterior="214",
            numero_interior="215",
            colonia_id="0347",
            localidad_id="23",
            referencia="casa negra",
            municipio_id="004",
            estado_id="COA",
            pais_id="MEX",
            codigo_postal_id="25350",
        ),
    )

    lading = LadingComplement(
        transp_internac_id="Sí",
        entrada_salida_merc_id="Entrada",
        pais_origen_destino_id="AFG",
        via_entrada_salida_id="04",
        total_dist_rec=Decimal("500"),
        registro_istmo_id="Sí",
        ubicacion_polo_origen_id="01",
        ubicacion_polo_destino_id="01",
        unidad_peso_id="XBX",
        peso_neto_total=Decimal("10"),
        regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="IMD")],
        ubicaciones=_ubicaciones_ferroviario_traslado_nacional() + [destino_final],
        mercancias=[
            Mercancia(
                bienes_transp_id="11121900",
                descripcion="Accesorios de equipo de telefonía",
                cantidad=Decimal("1.0"),
                clave_unidad_id="XBX",
                material_peligroso_id="No",
                denominacion_generica_prod="DenominacionGenericaProd1",
                denominacion_distintiva_prod="DenominacionDistintivaProd1",
                fabricante="Fabricante1",
                fecha_caducidad="2028-01-01T00:00:00",
                lote_medicamento="LoteMedic1",
                registro_sanitario_folio_autorizacion="RegistroSanita1",
                peso_en_kg=Decimal("1"),
                tipo_materia_id="05",
                descripcion_materia="otramateria",
                documentacion_aduanera=[
                    DocumentoAduanero(
                        tipo_documento_id="01",
                        num_pedimento="23  43  0472  8000448",
                        rfc_impo="EKU9003173C9",
                    )
                ],
                cantidad_transporta=[
                    CantidadTransporta(cantidad=Decimal("1"), id_origen="OR101010", id_destino="DE202025")
                ],
            )
        ],
        transporte_ferroviario=_transporte_ferroviario_traslado(),
        tipos_figura=[_figura_traslado_ferroviario()],
    )

    invoice = _invoice_traslado_ferroviario_base(lading)
    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 20: TRASLADO AÉREO NACIONAL
# ============================================================================
def create_factura_traslado_aereo_nacional():
    invoice = Invoice(
        version_code="4.0",
        currency_code="XXX",
        type_code="T",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(
            lading=LadingComplement(
                transp_internac_id="No",
                unidad_peso_id="XBX",
                peso_neto_total=Decimal("10"),
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR101010",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                        num_estacion_id="EA0417",
                        nombre_estacion="Loreto",
                        fecha_hora_salida_llegada="2023-08-01T00:00:00",
                        tipo_estacion_id="01",
                        domicilio=UbicacionDomicilio(
                            calle="Calle1",
                            numero_exterior="211",
                            numero_interior="212",
                            colonia_id="1957",
                            localidad_id="13",
                            referencia="casa blanca",
                            municipio_id="011",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="13250",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE202020",
                        rfc_remitente_destinatario="EKU9003173C9",
                        nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                        num_estacion_id="EA0418",
                        nombre_estacion="Los Cabos",
                        fecha_hora_salida_llegada="2023-08-01T00:00:01",
                        tipo_estacion_id="03",
                        domicilio=UbicacionDomicilio(
                            calle="Calle2",
                            numero_exterior="214",
                            numero_interior="215",
                            colonia_id="0347",
                            localidad_id="23",
                            referencia="casa negra",
                            municipio_id="004",
                            estado_id="COA",
                            pais_id="MEX",
                            codigo_postal_id="25350",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="11121900",
                        descripcion="Accesorios de equipo de telefonía",
                        cantidad=Decimal("1.0"),
                        clave_unidad_id="XBX",
                        material_peligroso_id="No",
                        denominacion_generica_prod="DenominacionGenericaProd1",
                        denominacion_distintiva_prod="DenominacionDistintivaProd1",
                        fabricante="Fabricante1",
                        fecha_caducidad="2028-01-01T00:00:00",
                        lote_medicamento="LoteMedic1",
                        registro_sanitario_folio_autorizacion="RegistroSanita1",
                        peso_en_kg=Decimal("1"),
                        valor_mercancia=Decimal("100"),
                        moneda_id="MXN",
                        cantidad_transporta=[
                            CantidadTransporta(
                                cantidad=Decimal("1"),
                                id_origen="OR101010",
                                id_destino="DE202020",
                            )
                        ],
                    )
                ],
                transporte_aereo=TransporteAereo(
                    perm_sct_id="TPAF01",
                    num_permiso_sct="Demo",
                    matricula_aeronave="61E5-WZ",
                    nombre_aseg="NombreAseg",
                    num_poliza_seguro="NumPolizaSeguro",
                    numero_guia="acUbYlBVTmlzx",
                    lugar_contrato="LugarContrato",
                    codigo_transportista_id="CA001",
                    rfc_embarcador="EKU9003173C9",
                    nombre_embarcador="Embarcador",
                ),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="EKU9003173C9",
                        num_licencia="a234567890",
                        nombre_figura="NombreFigura",
                    )
                ],
            )
        ),
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# HELPERS TRASLADO AÉREO / MARÍTIMO
# ============================================================================
def _transporte_aereo_base() -> TransporteAereo:
    return TransporteAereo(
        perm_sct_id="TPAF01",
        num_permiso_sct="Demo",
        matricula_aeronave="61E5-WZ",
        nombre_aseg="NombreAseg",
        num_poliza_seguro="NumPolizaSeguro",
        numero_guia="acUbYlBVTmlzx",
        lugar_contrato="LugarContrato",
        codigo_transportista_id="CA001",
        rfc_embarcador="EKU9003173C9",
        nombre_embarcador="Embarcador",
    )


def _invoice_traslado_base(lading: LadingComplement) -> Invoice:
    return Invoice(
        version_code="4.0",
        currency_code="XXX",
        type_code="T",
        expedition_zip_code="42501",
        series="Serie",
        date=datetime.now(),
        exchange_rate=Decimal("1"),
        export_code="01",
        issuer=InvoiceIssuer(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            tax_regime_code="601",
            tax_credentials=_kemper_credentials(),
        ),
        recipient=InvoiceRecipient(
            tin="EKU9003173C9",
            legal_name="ESCUELA KEMPER URGATE",
            zip_code="42501",
            tax_regime_code="601",
            cfdi_use_code="S01",
        ),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="UT421511",
                quantity=Decimal("1"),
                unit_of_measurement_code="H87",
                description="Transporte de carga por carretera",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            )
        ],
        complement=InvoiceComplement(lading=lading),
    )


# ============================================================================
# EJEMPLO 21: TRASLADO AÉREO EXTRANJERO (SALIDA)
# ============================================================================
def create_factura_traslado_aereo_extranjero():
    invoice = _invoice_traslado_base(
        LadingComplement(
            transp_internac_id="Sí",
            entrada_salida_merc_id="Salida",
            pais_origen_destino_id="USA",
            via_entrada_salida_id="03",
            unidad_peso_id="XBX",
            peso_neto_total=Decimal("10"),
            regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
            ubicaciones=[
                Ubicacion(
                    tipo_ubicacion="Origen",
                    id_ubicacion="OR101010",
                    rfc_remitente_destinatario="EKU9003173C9",
                    nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                    num_estacion_id="EA0417",
                    nombre_estacion="Loreto",
                    fecha_hora_salida_llegada="2023-08-01T00:00:00",
                    tipo_estacion_id="01",
                    domicilio=UbicacionDomicilio(
                        calle="Calle2",
                        numero_exterior="214",
                        numero_interior="215",
                        colonia_id="0347",
                        localidad_id="23",
                        referencia="casa negra",
                        municipio_id="004",
                        estado_id="COA",
                        pais_id="MEX",
                        codigo_postal_id="25350",
                    ),
                ),
                Ubicacion(
                    tipo_ubicacion="Destino",
                    id_ubicacion="DE202020",
                    rfc_remitente_destinatario="XEXX010101000",
                    nombre_remitente_destinatario="NombreRemitenteDestinatario",
                    num_reg_id_trib="01010101",
                    residencia_fiscal_id="USA",
                    num_estacion_id="EA0143",
                    nombre_estacion="Phoenix-Mesa Gateway",
                    fecha_hora_salida_llegada="2023-08-01T00:00:01",
                    domicilio=UbicacionDomicilio(
                        calle="ST",
                        numero_exterior="12344",
                        colonia_id="N/A",
                        referencia="WHITE HOUSE",
                        municipio_id="N/A",
                        estado_id="TX",
                        pais_id="USA",
                        codigo_postal_id="12345",
                    ),
                ),
            ],
            mercancias=[
                Mercancia(
                    bienes_transp_id="11121900",
                    descripcion="Accesorios de equipo de telefonía",
                    cantidad=Decimal("1.0"),
                    clave_unidad_id="XBX",
                    material_peligroso_id="No",
                    denominacion_generica_prod="DenominacionGenericaProd1",
                    denominacion_distintiva_prod="DenominacionDistintivaProd1",
                    fabricante="Fabricante1",
                    fecha_caducidad="2028-01-01T00:00:00",
                    lote_medicamento="LoteMedic1",
                    registro_sanitario_folio_autorizacion="RegistroSanita1",
                    peso_en_kg=Decimal("1"),
                    valor_mercancia=Decimal("100"),
                    moneda_id="MXN",
                    tipo_materia_id="05",
                    descripcion_materia="otramateria",
                    cantidad_transporta=[
                        CantidadTransporta(cantidad=Decimal("1"), id_origen="OR101010", id_destino="DE202020")
                    ],
                )
            ],
            transporte_aereo=_transporte_aereo_base(),
            tipos_figura=[
                TipoFigura(
                    tipo_figura_id="01",
                    rfc_figura="EKU9003173C9",
                    num_licencia="a234567890",
                    nombre_figura="NombreFigura",
                )
            ],
        )
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 22: TRASLADO AÉREO INTERNACIONAL ADUANERO (ENTRADA)
# ============================================================================
def create_factura_traslado_aereo_internacional_aduanero():
    invoice = _invoice_traslado_base(
        LadingComplement(
            transp_internac_id="Sí",
            entrada_salida_merc_id="Entrada",
            pais_origen_destino_id="AFG",
            via_entrada_salida_id="03",
            unidad_peso_id="XBX",
            peso_neto_total=Decimal("10"),
            regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="IMD")],
            ubicaciones=[
                Ubicacion(
                    tipo_ubicacion="Origen",
                    id_ubicacion="OR101010",
                    rfc_remitente_destinatario="EKU9003173C9",
                    nombre_remitente_destinatario="NombreRemitenteDestinatario1",
                    num_estacion_id="EA0417",
                    nombre_estacion="Loreto",
                    fecha_hora_salida_llegada="2023-08-01T00:00:00",
                    tipo_estacion_id="01",
                    domicilio=UbicacionDomicilio(
                        calle="Calle1",
                        numero_exterior="211",
                        numero_interior="212",
                        colonia_id="1957",
                        localidad_id="13",
                        referencia="casa blanca",
                        municipio_id="011",
                        estado_id="CMX",
                        pais_id="MEX",
                        codigo_postal_id="13250",
                    ),
                ),
                Ubicacion(
                    tipo_ubicacion="Destino",
                    id_ubicacion="DE202020",
                    rfc_remitente_destinatario="EKU9003173C9",
                    nombre_remitente_destinatario="NombreRemitenteDestinatario2",
                    num_estacion_id="EA0418",
                    nombre_estacion="Los Cabos",
                    fecha_hora_salida_llegada="2023-08-01T00:00:01",
                    tipo_estacion_id="03",
                    domicilio=UbicacionDomicilio(
                        calle="Calle2",
                        numero_exterior="214",
                        numero_interior="215",
                        colonia_id="0347",
                        localidad_id="23",
                        referencia="casa negra",
                        municipio_id="004",
                        estado_id="COA",
                        pais_id="MEX",
                        codigo_postal_id="25350",
                    ),
                ),
            ],
            mercancias=[
                Mercancia(
                    bienes_transp_id="11121900",
                    descripcion="Accesorios de equipo de telefonía",
                    cantidad=Decimal("1.0"),
                    clave_unidad_id="XBX",
                    material_peligroso_id="No",
                    denominacion_generica_prod="DenominacionGenericaProd1",
                    denominacion_distintiva_prod="DenominacionDistintivaProd1",
                    fabricante="Fabricante1",
                    fecha_caducidad="2028-01-01T00:00:00",
                    lote_medicamento="LoteMedic1",
                    registro_sanitario_folio_autorizacion="RegistroSanita1",
                    peso_en_kg=Decimal("1"),
                    valor_mercancia=Decimal("100"),
                    moneda_id="MXN",
                    tipo_materia_id="05",
                    descripcion_materia="otramateria",
                    documentacion_aduanera=[
                        DocumentoAduanero(
                            tipo_documento_id="01",
                            num_pedimento="23  43  0472  8000448",
                            rfc_impo="EKU9003173C9",
                        )
                    ],
                    cantidad_transporta=[
                        CantidadTransporta(cantidad=Decimal("1"), id_origen="OR101010", id_destino="DE202020")
                    ],
                )
            ],
            transporte_aereo=_transporte_aereo_base(),
            tipos_figura=[
                TipoFigura(
                    tipo_figura_id="01",
                    rfc_figura="EKU9003173C9",
                    num_licencia="a234567890",
                    nombre_figura="NombreFigura",
                )
            ],
        )
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# HELPERS TRASLADO MARÍTIMO
# ============================================================================
def _ubicaciones_maritimo_nacional():
    return [
        Ubicacion(
            tipo_ubicacion="Origen",
            id_ubicacion="OR101010",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario1",
            num_estacion_id="PM001",
            nombre_estacion="Rosarito",
            navegacion_trafico_id="Altura",
            fecha_hora_salida_llegada="2023-08-01T00:00:00",
            tipo_estacion_id="01",
            domicilio=UbicacionDomicilio(
                calle="Calle1",
                numero_exterior="211",
                numero_interior="212",
                colonia_id="1957",
                localidad_id="13",
                referencia="casa blanca",
                municipio_id="011",
                estado_id="CMX",
                pais_id="MEX",
                codigo_postal_id="13250",
            ),
        ),
        Ubicacion(
            tipo_ubicacion="Destino",
            id_ubicacion="DE202020",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario2",
            num_estacion_id="PM001",
            nombre_estacion="Rosarito",
            navegacion_trafico_id="Altura",
            fecha_hora_salida_llegada="2023-08-01T00:00:01",
            tipo_estacion_id="03",
            domicilio=UbicacionDomicilio(
                calle="Calle2",
                numero_exterior="214",
                numero_interior="215",
                colonia_id="0347",
                localidad_id="23",
                referencia="casa negra",
                municipio_id="004",
                estado_id="COA",
                pais_id="MEX",
                codigo_postal_id="25350",
            ),
        ),
    ]


def _mercancia_maritimo_traslado(documentacion_aduanera=None, tipo_materia_id=None, descripcion_materia=None):
    return Mercancia(
        bienes_transp_id="11121900",
        descripcion="Accesorios de equipo de telefonía",
        cantidad=Decimal("1.0"),
        clave_unidad_id="XBX",
        material_peligroso_id="No",
        denominacion_generica_prod="DenominacionGenericaProd1",
        denominacion_distintiva_prod="DenominacionDistintivaProd1",
        fabricante="Fabricante1",
        fecha_caducidad="2028-01-01T00:00:00",
        lote_medicamento="LoteMedic1",
        registro_sanitario_folio_autorizacion="RegistroSanita1",
        peso_en_kg=Decimal("1"),
        valor_mercancia=Decimal("100"),
        moneda_id="MXN",
        tipo_materia_id=tipo_materia_id,
        descripcion_materia=descripcion_materia,
        documentacion_aduanera=documentacion_aduanera,
        cantidad_transporta=[
            CantidadTransporta(cantidad=Decimal("1"), id_origen="OR101010", id_destino="DE202020")
        ],
        detalle_mercancia=DetalleMercancia(
            unidad_peso_merc_id="Tu",
            peso_bruto=Decimal("1"),
            peso_neto=Decimal("1"),
            peso_tara=Decimal("0.001"),
            num_piezas=1,
        ),
    )


# ============================================================================
# EJEMPLO 23: TRASLADO MARÍTIMO NACIONAL
# ============================================================================
def create_factura_traslado_maritimo_nacional():
    invoice = _invoice_traslado_base(
        LadingComplement(
            transp_internac_id="No",
            unidad_peso_id="XBX",
            peso_neto_total=Decimal("1"),
            ubicaciones=_ubicaciones_maritimo_nacional(),
            mercancias=[_mercancia_maritimo_traslado()],
            transporte_maritimo=_transporte_maritimo_base(),
            tipos_figura=[_figura_ferroviario()],
        )
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 24: TRASLADO MARÍTIMO EXTRANJERO (SALIDA)
# ============================================================================
def create_factura_traslado_maritimo_extranjero():
    ubicaciones = [
        Ubicacion(
            tipo_ubicacion="Origen",
            id_ubicacion="OR101010",
            rfc_remitente_destinatario="EKU9003173C9",
            nombre_remitente_destinatario="NombreRemitenteDestinatario1",
            num_estacion_id="PM001",
            nombre_estacion="Rosarito",
            navegacion_trafico_id="Altura",
            fecha_hora_salida_llegada="2023-08-01T00:00:00",
            tipo_estacion_id="01",
            domicilio=UbicacionDomicilio(
                calle="Calle1",
                numero_exterior="211",
                numero_interior="212",
                colonia_id="1957",
                localidad_id="13",
                referencia="casa blanca",
                municipio_id="011",
                estado_id="CMX",
                pais_id="MEX",
                codigo_postal_id="13250",
            ),
        ),
        Ubicacion(
            tipo_ubicacion="Destino",
            id_ubicacion="DE202020",
            rfc_remitente_destinatario="XEXX010101000",
            nombre_remitente_destinatario="NombreRemitenteDestinatario2",
            num_reg_id_trib="01010101",
            residencia_fiscal_id="USA",
            num_estacion_id="PM120",
            nombre_estacion="NombreEstacion",
            navegacion_trafico_id="Altura",
            fecha_hora_salida_llegada="2023-08-01T00:00:01",
            domicilio=UbicacionDomicilio(
                calle="ST",
                numero_exterior="12345",
                colonia_id="N/A",
                referencia="N/A",
                municipio_id="N/A",
                estado_id="TX",
                pais_id="USA",
                codigo_postal_id="12345",
            ),
        ),
    ]

    invoice = _invoice_traslado_base(
        LadingComplement(
            transp_internac_id="Sí",
            entrada_salida_merc_id="Salida",
            pais_origen_destino_id="USA",
            via_entrada_salida_id="02",
            unidad_peso_id="XBX",
            peso_neto_total=Decimal("1"),
            regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
            ubicaciones=ubicaciones,
            mercancias=[_mercancia_maritimo_traslado(tipo_materia_id="05", descripcion_materia="otramateria")],
            transporte_maritimo=_transporte_maritimo_base(),
            tipos_figura=[_figura_ferroviario()],
        )
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJEMPLO 25: TRASLADO MARÍTIMO INTERNACIONAL ADUANERO (ENTRADA)
# ============================================================================
def create_factura_traslado_maritimo_internacional_aduanero():
    invoice = _invoice_traslado_base(
        LadingComplement(
            transp_internac_id="Sí",
            entrada_salida_merc_id="Entrada",
            pais_origen_destino_id="AFG",
            via_entrada_salida_id="02",
            unidad_peso_id="XBX",
            peso_neto_total=Decimal("1"),
            regimen_aduaneros=[
                RegimenAduanero(regimen_aduanero_id="IMD"),
                RegimenAduanero(regimen_aduanero_id="IMD"),
            ],
            ubicaciones=_ubicaciones_maritimo_nacional(),
            mercancias=[
                _mercancia_maritimo_traslado(
                    tipo_materia_id="05",
                    descripcion_materia="otramateria",
                    documentacion_aduanera=[
                        DocumentoAduanero(
                            tipo_documento_id="01",
                            num_pedimento="23  43  0472  8000448",
                            rfc_impo="EKU9003173C9",
                        )
                    ],
                )
            ],
            transporte_maritimo=_transporte_maritimo_base(),
            tipos_figura=[_figura_ferroviario()],
        )
    )

    response = client.invoices.create(invoice)
    if response.succeeded:
        print(response.data)
    else:
        print(response.message)
        print(response.details)


# ============================================================================
# EJECUCION
# ============================================================================
if __name__ == "__main__":
    print("=== 1. Autotransporte Nacional ===")
    create_factura_autotransporte_nacional()

    print("\n=== 2. Autotransporte Nacional con Impuestos ===")
    create_factura_autotransporte_nacional_con_impuestos()

    print("\n=== 3. Autotransporte Extranjero (Salida) ===")
    create_factura_autotransporte_extranjero()

    print("\n=== 4. Autotransporte Internacional Aduanero (Entrada) ===")
    create_factura_autotransporte_internacional_aduanero()

    print("\n=== 5. Ferroviario Nacional ===")
    create_factura_ferroviario_nacional()

    print("\n=== 6. Ferroviario Extranjero (Salida) ===")
    create_factura_ferroviario_extranjero()

    print("\n=== 7. Ferroviario Internacional Aduanero (Entrada) ===")
    create_factura_ferroviario_internacional_aduanero()

    print("\n=== 8. Aéreo Nacional ===")
    create_factura_aereo_nacional()

    print("\n=== 9. Aéreo Extranjero (Salida) ===")
    create_factura_aereo_extranjero()

    print("\n=== 10. Aéreo Internacional Aduanero (Entrada) ===")
    create_factura_aereo_internacional_aduanero()

    print("\n=== 11. Marítimo Nacional ===")
    create_factura_maritimo_nacional()

    print("\n=== 12. Marítimo Extranjero (Salida) ===")
    create_factura_maritimo_extranjero()

    print("\n=== 13. Marítimo Internacional Aduanero (Entrada) - Ingreso ===")
    create_factura_maritimo_internacional_aduanero()

    print("\n=== 14. Traslado Autotransporte Nacional ===")
    create_factura_traslado_autotransporte_nacional()

    print("\n=== 15. Traslado Autotransporte Extranjero (Salida) ===")
    create_factura_traslado_autotransporte_extranjero()

    print("\n=== 16. Traslado Autotransporte Internacional Aduanero (Entrada) ===")
    create_factura_traslado_autotransporte_internacional_aduanero()

    print("\n=== 17. Traslado Ferroviario Nacional ===")
    create_factura_traslado_ferroviario_nacional()

    print("\n=== 18. Traslado Ferroviario Extranjero (Salida) ===")
    create_factura_traslado_ferroviario_extranjero()

    print("\n=== 19. Traslado Ferroviario Internacional Aduanero (Entrada) ===")
    create_factura_traslado_ferroviario_internacional_aduanero()

    print("\n=== 20. Traslado Aéreo Nacional ===")
    create_factura_traslado_aereo_nacional()

    print("\n=== 21. Traslado Aéreo Extranjero (Salida) ===")
    create_factura_traslado_aereo_extranjero()

    print("\n=== 22. Traslado Aéreo Internacional Aduanero (Entrada) ===")
    create_factura_traslado_aereo_internacional_aduanero()

    print("\n=== 23. Traslado Marítimo Nacional ===")
    create_factura_traslado_maritimo_nacional()

    print("\n=== 24. Traslado Marítimo Extranjero (Salida) ===")
    create_factura_traslado_maritimo_extranjero()

    print("\n=== 25. Traslado Marítimo Internacional Aduanero (Entrada) ===")
    create_factura_traslado_maritimo_internacional_aduanero()
