# ============================================================================
# CONFIGURACION
# ============================================================================
#
# Ejemplos de Factura de Comercio Exterior - Modo POR REFERENCIAS.
#
# Cada caso de uso expone dos funciones:
#   1. xxx_update_people()   -> Sincroniza emisor (issuer_id) y receptor
#                               (recipient_id) en el sistema usando
#                               client.people.update(...).
#   2. xxx_por_referencias() -> Llama primero a xxx_update_people() y luego
#                               crea la factura enviando issuer/recipient
#                               unicamente con su `id`.
#
# Los IDs estan centralizados al inicio del archivo. Los datos de items,
# complementos (comercioExterior y cartaPorte), totales y decimales se
# conservan identicos a los del archivo por valores.
# ============================================================================

from datetime import datetime
from decimal import Decimal

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
    Person,
)
from fiscalapi.models.comercio_exterior_models import (
    ComercioExteriorComplement,
    ComercioExteriorEmisor,
    ComercioExteriorEmisorDomicilio,
    ComercioExteriorReceptor,
    ComercioExteriorReceptorDomicilio,
    ComercioExteriorDestinatario,
    ComercioExteriorDestinatarioDomicilio,
    ComercioExteriorMercancia,
)
from fiscalapi.models.carta_porte_models import (
    CartaPorteComplement,
    Ubicacion,
    UbicacionDomicilio,
    Mercancia,
    Autotransporte,
    TipoFigura,
    RegimenAduanero,
)


settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="API_KEY",
    tenant="TENANT_ID"
)

client = FiscalApiClient(settings=settings)

# Valores centralizados para todos los ejemplos (cambia aqui una sola vez)
current_date = datetime.fromisoformat("2026-05-19T08:56:40")
tipo_cambio = Decimal("17.3477")
issuer_id = "2e7b988f-3a2a-4f67-86e9-3f931dd48581"  # ESCUELA KEMPER URGATE
recipient_id = "109f4d94-63ea-4a21-ab15-20c8b87d8ee9"  # KARLA FUENTES



# Helper: Emisor Kemper estandar para client.people.update(...)
def kemper_issuer_person():
    return Person(
        id=issuer_id,
        tin="EKU9003173C9",
        legal_name="ESCUELA KEMPER URGATE",
        sat_tax_regime_id="601",
        zip_code="42501",
        email="kemper@fiscalapi.com",
    )


# Helper: Imprimir respuesta de la API de forma legible
def print_response(response):
    if response.succeeded:
        print(response.data.number)
    else:
        print(response)


# ============================================================================
# 1. Factura CE Ingreso Con Carta Porte 31
# ============================================================================
def factura_ce_ingreso_con_carta_porte_31_update_people():
    client.people.update(kemper_issuer_person())
    client.people.update(Person(
        id=recipient_id,
        tin="XEXX010101000",
        legal_name="Persona Fisica Extranjera",
        zip_code="42501",
        sat_tax_regime_id="616",
        sat_cfdi_use_id="S01",
        country_id="USA",
        foreign_tin="123456789",
        email="karla.fuentes@fiscalapi.com",
    ))


def factura_ce_ingreso_con_carta_porte_31_por_referencias():
    print("=== 1. Factura CE Ingreso Con Carta Porte 31 (Por Referencias) ===")
    factura_ce_ingreso_con_carta_porte_31_update_people()

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="99",
        payment_method_code="PUE",
        currency_code="USD",
        type_code="I",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        payment_conditions="CondicionesDePago",
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=recipient_id),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="SERV02",
                quantity=Decimal("1.000000"),
                unit_of_measurement_code="HUR",
                description="FLETE",
                unit_price=Decimal("2300.000000"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                    ItemTax(tax_code="003", tax_type_code="Tasa", tax_rate=Decimal("0.300000"), tax_flag_code="R"),
                ],
            ),
            InvoiceItem(
                item_code="50161509",
                item_sku="A0001",
                quantity=Decimal("1.000000"),
                unit_of_measurement_code="H87",
                description="Gomitas",
                unit_price=Decimal("120.000000"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                ],
            ),
            InvoiceItem(
                item_code="50307037",
                item_sku="A0002",
                quantity=Decimal("1.000000"),
                unit_of_measurement_code="H87",
                description="Pulparindo",
                unit_price=Decimal("100.000000"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                ],
            ),
        ],
        complement=InvoiceComplement(
            carta_porte=CartaPorteComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Salida",
                pais_origen_destino_id="ALB",
                via_entrada_salida_id="01",
                total_dist_rec=Decimal("120.00"),
                unidad_peso_id="KGM",
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR000001",
                        rfc_remitente_destinatario="XAXX010101000",
                        nombre_remitente_destinatario="Origen Nacional",
                        fecha_hora_salida_llegada="2026-04-27T08:00:00",
                        domicilio=UbicacionDomicilio(
                            calle="xola",
                            numero_exterior="531",
                            colonia_id="0496",
                            localidad_id="03",
                            municipio_id="014",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="03100",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE000001",
                        rfc_remitente_destinatario="XAXX010101000",
                        nombre_remitente_destinatario="Destino Nacional",
                        fecha_hora_salida_llegada="2026-04-27T20:00:00",
                        distancia_recorrida=Decimal("120.00"),
                        domicilio=UbicacionDomicilio(
                            calle="Av Coyoacan",
                            numero_exterior="120",
                            colonia_id="2624",
                            localidad_id="03",
                            municipio_id="014",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="03100",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="50433238",
                        descripcion="Gomitas",
                        cantidad=Decimal("1"),
                        clave_unidad_id="XPK",
                        peso_en_kg=Decimal("10.000"),
                        valor_mercancia=Decimal("1200.00"),
                        moneda_id="USD",
                        fraccion_arancelaria_id="2005800100",
                        tipo_materia_id="04",
                    ),
                    Mercancia(
                        bienes_transp_id="50433238",
                        descripcion="Pulparindo",
                        cantidad=Decimal("1"),
                        clave_unidad_id="XPK",
                        peso_en_kg=Decimal("10.000"),
                        valor_mercancia=Decimal("1000.00"),
                        moneda_id="USD",
                        fraccion_arancelaria_id="2005800100",
                        tipo_materia_id="04",
                    ),
                ],
                autotransporte=Autotransporte(
                    perm_sct_id="TPAF02",
                    num_permiso_sct="123456",
                    config_vehicular_id="C2",
                    peso_bruto_vehicular=Decimal("1"),
                    placa_vm="555TTT",
                    anio_modelo_vm=2023,
                    asegura_resp_civil="ODISEA",
                    poliza_resp_civil="3456YUHNB234RT",
                ),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="KAHO641101B39",
                        num_licencia="D0908240",
                        nombre_figura="OSCAR KALA HAAK",
                    )
                ],
            ),
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="CIF",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="Av Siempre viva",
                        numero_exterior="123",
                        colonia_id="0001",
                        localidad_id="06",
                        municipio_id="025",
                        estado_id="COA",
                        pais_id="MEX",
                        codigo_postal_id="26015",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    num_reg_id_trib="123456789",
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="Clinton ST",
                        numero_exterior="10002",
                        estado="NY",
                        pais_id="USA",
                        codigo_postal="10002-0000",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="A0001",
                        fraccion_arancelaria_id="4011101099",
                        cantidad_aduana=Decimal("1.000"),
                        unidad_aduana_id="06",
                        valor_unitario_aduana=Decimal("120.00"),
                        valor_dolares=Decimal("120.00"),
                    ),
                    ComercioExteriorMercancia(
                        no_identificacion="A0002",
                        fraccion_arancelaria_id="8407210299",
                        cantidad_aduana=Decimal("1.000"),
                        unidad_aduana_id="06",
                        valor_unitario_aduana=Decimal("100.00"),
                        valor_dolares=Decimal("100.00"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 2. Factura CE Ingreso Diferentes Monedas
# ============================================================================
def factura_ce_ingreso_diferentes_monedas_update_people():
    client.people.update(kemper_issuer_person())
    client.people.update(Person(
        id=recipient_id,
        tin="XEXX010101000",
        legal_name="Persona Fisica Extranjera",
        zip_code="42501",
        sat_tax_regime_id="616",
        sat_cfdi_use_id="S01",
        country_id="USA",
        foreign_tin="123456789",
        email="karla.fuentes@fiscalapi.com",
    ))


def factura_ce_ingreso_diferentes_monedas_por_referencias():
    print("=== 2. Factura CE Ingreso Diferentes Monedas (Por Referencias) ===")
    factura_ce_ingreso_diferentes_monedas_update_people()

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="99",
        payment_method_code="PPD",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        payment_conditions="CondicionesDePago",
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=recipient_id),
        items=[
            InvoiceItem(
                item_code="50211503",
                item_sku="131494-1055",
                quantity=Decimal("2"),
                unit_of_measurement_code="H87",
                description="Cigarros",
                unit_price=Decimal("200.00"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                    ItemTax(tax_code="001", tax_type_code="Tasa", tax_rate=Decimal("0.100000"), tax_flag_code="R"),
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.106666"), tax_flag_code="R"),
                ],
            ),
        ],
        complement=InvoiceComplement(
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FOB",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    num_reg_id_trib="123456789",
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="ST. A",
                        estado="TX",
                        pais_id="USA",
                        codigo_postal="00000",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="131494-1055",
                        fraccion_arancelaria_id="2402200100",
                        cantidad_aduana=Decimal("2.00"),
                        unidad_aduana_id="01",
                        valor_unitario_aduana=Decimal("11.74"),
                        valor_dolares=Decimal("23.47"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 3. Factura CE Kit Parte
# ============================================================================
def factura_ce_kit_parte_update_people():
    client.people.update(kemper_issuer_person())
    client.people.update(Person(
        id=recipient_id,
        tin="XEXX010101000",
        legal_name="U.S. 0026 SW",
        zip_code="42501",
        sat_tax_regime_id="616",
        sat_cfdi_use_id="CP01",
        country_id="USA",
        foreign_tin="123456789",
        email="karla.fuentes@fiscalapi.com",
    ))


def factura_ce_kit_parte_por_referencias():
    print("=== 3. Factura CE Kit Parte (Por Referencias) ===")
    factura_ce_kit_parte_update_people()

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="01",
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        payment_conditions="CondicionesDePago",
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=recipient_id),
        items=[
            InvoiceItem(
                item_code="51241200",
                item_sku="131494-1055",
                quantity=Decimal("1.0"),
                unit_of_measurement_code="H87",
                description="FORMULA MAGISTRAL",
                unit_price=Decimal("200.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            ),
            InvoiceItem(
                item_code="51241200",
                item_sku="131494-1055",
                quantity=Decimal("1.0"),
                unit_of_measurement_code="H87",
                description="FORMULA MAGISTRAL",
                unit_price=Decimal("200.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            ),
        ],
        complement=InvoiceComplement(
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FOB",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    num_reg_id_trib="123456789",
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="ST. A",
                        estado="TX",
                        pais_id="USA",
                        codigo_postal="00000",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="131494-1055",
                        fraccion_arancelaria_id="2402200100",
                        cantidad_aduana=Decimal("2"),
                        unidad_aduana_id="01",
                        valor_unitario_aduana=Decimal("10.00"),
                        valor_dolares=Decimal("20.00"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 4. Factura CE Receptor Extranjero
# ============================================================================
def factura_ce_receptor_extranjero_update_people():
    client.people.update(kemper_issuer_person())
    client.people.update(Person(
        id=recipient_id,
        tin="XEXX010101000",
        legal_name="U.S. 0026 SW",
        zip_code="42501",
        sat_tax_regime_id="616",
        sat_cfdi_use_id="CP01",
        country_id="USA",
        foreign_tin="123456789",
        email="karla.fuentes@fiscalapi.com",
    ))


def factura_ce_receptor_extranjero_por_referencias():
    print("=== 4. Factura CE Receptor Extranjero (Por Referencias) ===")
    factura_ce_receptor_extranjero_update_people()

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="99",
        payment_method_code="PPD",
        currency_code="USD",
        type_code="I",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        payment_conditions="CondicionesDePago",
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=recipient_id),
        items=[
            InvoiceItem(
                item_code="50211503",
                item_sku="131494-1055",
                quantity=Decimal("2"),
                unit_of_measurement_code="H87",
                description="Cigarros",
                unit_price=Decimal("200.00"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                    ItemTax(tax_code="001", tax_type_code="Tasa", tax_rate=Decimal("0.100000"), tax_flag_code="R"),
                ],
            ),
        ],
        complement=InvoiceComplement(
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FOB",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    num_reg_id_trib="123456789",
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="ST. A",
                        estado="TX",
                        pais_id="USA",
                        codigo_postal="00000",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="131494-1055",
                        fraccion_arancelaria_id="2402200100",
                        cantidad_aduana=Decimal("117.64"),
                        unidad_aduana_id="01",
                        valor_unitario_aduana=Decimal("3.40"),
                        valor_dolares=Decimal("400.00"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 5. Factura CE Receptor Nacional
# ============================================================================
def factura_ce_receptor_nacional_update_people():
    client.people.update(kemper_issuer_person())
    client.people.update(Person(
        id=recipient_id,
        tin="URE180429TM6",
        legal_name="UNIVERSIDAD ROBOTICA ESPAÑOLA",
        zip_code="86991",
        sat_tax_regime_id="601",
        sat_cfdi_use_id="G01",
        email="karla.fuentes@fiscalapi.com",
    ))


def factura_ce_receptor_nacional_por_referencias():
    print("=== 5. Factura CE Receptor Nacional (Por Referencias) ===")
    factura_ce_receptor_nacional_update_people()

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="99",
        payment_method_code="PPD",
        currency_code="USD",
        type_code="I",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        payment_conditions="CondicionesDePago",
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=recipient_id),
        items=[
            InvoiceItem(
                item_code="50211503",
                item_sku="131494-1055",
                quantity=Decimal("2"),
                unit_of_measurement_code="H87",
                description="Cigarros",
                unit_price=Decimal("200.00"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                    ItemTax(tax_code="001", tax_type_code="Tasa", tax_rate=Decimal("0.100000"), tax_flag_code="R"),
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.106666"), tax_flag_code="R"),
                ],
            ),
        ],
        complement=InvoiceComplement(
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FOB",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia="0214",
                        localidad="01",
                        municipio="014",
                        estado="QUE",
                        pais_id="MEX",
                        codigo_postal="76199",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="131494-1055",
                        fraccion_arancelaria_id="2402200100",
                        cantidad_aduana=Decimal("117.64"),
                        unidad_aduana_id="01",
                        valor_unitario_aduana=Decimal("3.40"),
                        valor_dolares=Decimal("400.00"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 6. Factura CE Traslado Con Carta Porte 31
# ============================================================================
def factura_ce_traslado_con_carta_porte_31_update_people():
    # Traslado (tipo "T"): receptor debe ser el mismo RFC que el emisor.
    # Se referencia issuer_id (Kemper) tambien como receptor; se actualiza
    # el Person con sat_cfdi_use_id para satisfacer la validacion del receptor.
    client.people.update(Person(
        id=issuer_id,
        tin="EKU9003173C9",
        legal_name="ESCUELA KEMPER URGATE",
        zip_code="42501",
        sat_tax_regime_id="601",
        sat_cfdi_use_id="S01",
        email="kemper@fiscalapi.com",
    ))


def factura_ce_traslado_con_carta_porte_31_por_referencias():
    print("=== 6. Factura CE Traslado Con Carta Porte 31 (Por Referencias) ===")
    factura_ce_traslado_con_carta_porte_31_update_people()

    invoice = Invoice(
        version_code="4.0",
        currency_code="XXX",
        type_code="T",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=issuer_id),
        items=[
            InvoiceItem(
                item_code="78101800",
                item_sku="TR01",
                quantity=Decimal("1.0"),
                unit_of_measurement_code="H87",
                description="TRANSPORTE DE CARGA",
                unit_price=Decimal("0.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            ),
            InvoiceItem(
                item_code="32101622",
                item_sku="UT421511",
                quantity=Decimal("100.00"),
                unit_of_measurement_code="XBX",
                description="MEMORIA FLASH",
                unit_price=Decimal("0.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            ),
        ],
        complement=InvoiceComplement(
            carta_porte=CartaPorteComplement(
                transp_internac_id="Sí",
                entrada_salida_merc_id="Salida",
                pais_origen_destino_id="ALB",
                via_entrada_salida_id="01",
                total_dist_rec=Decimal("120.00"),
                unidad_peso_id="KGM",
                regimen_aduaneros=[RegimenAduanero(regimen_aduanero_id="EXD")],
                ubicaciones=[
                    Ubicacion(
                        tipo_ubicacion="Origen",
                        id_ubicacion="OR000001",
                        rfc_remitente_destinatario="XAXX010101000",
                        nombre_remitente_destinatario="Origen Nacional",
                        fecha_hora_salida_llegada="2026-04-27T08:00:00",
                        domicilio=UbicacionDomicilio(
                            calle="xola",
                            numero_exterior="531",
                            colonia_id="0496",
                            localidad_id="03",
                            municipio_id="014",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="03100",
                        ),
                    ),
                    Ubicacion(
                        tipo_ubicacion="Destino",
                        id_ubicacion="DE000001",
                        rfc_remitente_destinatario="XAXX010101000",
                        nombre_remitente_destinatario="Destino Nacional",
                        fecha_hora_salida_llegada="2026-04-27T20:00:00",
                        distancia_recorrida=Decimal("120.00"),
                        domicilio=UbicacionDomicilio(
                            calle="Av Coyoacan",
                            numero_exterior="120",
                            colonia_id="2624",
                            localidad_id="03",
                            municipio_id="014",
                            estado_id="CMX",
                            pais_id="MEX",
                            codigo_postal_id="03100",
                        ),
                    ),
                ],
                mercancias=[
                    Mercancia(
                        bienes_transp_id="50433238",
                        descripcion="Gomitas",
                        cantidad=Decimal("1"),
                        clave_unidad_id="XPK",
                        peso_en_kg=Decimal("10.000"),
                        valor_mercancia=Decimal("1200.00"),
                        moneda_id="USD",
                        fraccion_arancelaria_id="2005800100",
                        tipo_materia_id="04",
                    ),
                    Mercancia(
                        bienes_transp_id="50433238",
                        descripcion="Pulparindo",
                        cantidad=Decimal("1"),
                        clave_unidad_id="XPK",
                        peso_en_kg=Decimal("10.000"),
                        valor_mercancia=Decimal("1000.00"),
                        moneda_id="USD",
                        fraccion_arancelaria_id="2005800100",
                        tipo_materia_id="04",
                    ),
                ],
                autotransporte=Autotransporte(
                    perm_sct_id="TPAF02",
                    num_permiso_sct="123456",
                    config_vehicular_id="C2",
                    peso_bruto_vehicular=Decimal("1"),
                    placa_vm="555TTT",
                    anio_modelo_vm=2023,
                    asegura_resp_civil="ODISEA",
                    poliza_resp_civil="3456YUHNB234RT",
                ),
                tipos_figura=[
                    TipoFigura(
                        tipo_figura_id="01",
                        rfc_figura="KAHO641101B39",
                        num_licencia="D0908240",
                        nombre_figura="OSCAR KALA HAAK",
                    )
                ],
            ),
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FOB",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="ST. A",
                        estado="TX",
                        pais_id="USA",
                        codigo_postal="00000",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="UT421511",
                        fraccion_arancelaria_id="2402200100",
                        cantidad_aduana=Decimal("100.00"),
                        unidad_aduana_id="01",
                        valor_unitario_aduana=Decimal("1.00"),
                        valor_dolares=Decimal("0.00"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 7. Factura CE Traslado Traslado Mercancia Propia
# ============================================================================
def factura_ce_traslado_traslado_mercancia_propia_update_people():
    # Traslado (tipo "T"): receptor debe ser el mismo RFC que el emisor.
    # Se referencia issuer_id (Kemper) tambien como receptor; se actualiza
    # el Person con sat_cfdi_use_id para satisfacer la validacion del receptor.
    client.people.update(Person(
        id=issuer_id,
        tin="EKU9003173C9",
        legal_name="ESCUELA KEMPER URGATE",
        zip_code="42501",
        sat_tax_regime_id="601",
        sat_cfdi_use_id="S01",
        email="kemper@fiscalapi.com",
    ))


def factura_ce_traslado_traslado_mercancia_propia_por_referencias():
    print("=== 7. Factura CE Traslado Traslado Mercancia Propia (Por Referencias) ===")
    factura_ce_traslado_traslado_mercancia_propia_update_people()

    invoice = Invoice(
        version_code="4.0",
        currency_code="USD",
        type_code="T",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=issuer_id),
        items=[
            InvoiceItem(
                item_code="50211503",
                item_sku="131494-1055",
                quantity=Decimal("1.0"),
                unit_of_measurement_code="H87",
                description="My description...",
                unit_price=Decimal("0.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            ),
        ],
        complement=InvoiceComplement(
            comercio_exterior=ComercioExteriorComplement(
                motivo_traslado_id="02",
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FCA",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="SW Street.",
                        numero_exterior="12345",
                        localidad="Oregon",
                        estado="OR",
                        pais_id="USA",
                        codigo_postal="12345",
                    ),
                ),
                destinatarios=[
                    ComercioExteriorDestinatario(
                        num_reg_id_trib="123456789",
                        nombre="EKU9003173C9",
                        domicilios=[
                            ComercioExteriorDestinatarioDomicilio(
                                calle="SW Street.",
                                numero_exterior="12345",
                                localidad="Oregon",
                                estado="OR",
                                pais_id="USA",
                                codigo_postal="12345",
                            ),
                        ],
                    ),
                ],
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="131494-1055",
                        fraccion_arancelaria_id="0101210100",
                        cantidad_aduana=Decimal("1"),
                        unidad_aduana_id="07",
                        valor_unitario_aduana=Decimal("22.64"),
                        valor_dolares=Decimal("22.64"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 8. Factura CE Traslado Traslado
# ============================================================================
def factura_ce_traslado_traslado_update_people():
    # Traslado (tipo "T"): receptor debe ser el mismo RFC que el emisor.
    # Se referencia issuer_id (Kemper) tambien como receptor; se actualiza
    # el Person con sat_cfdi_use_id para satisfacer la validacion del receptor.
    client.people.update(Person(
        id=issuer_id,
        tin="EKU9003173C9",
        legal_name="ESCUELA KEMPER URGATE",
        zip_code="42501",
        sat_tax_regime_id="601",
        sat_cfdi_use_id="G01",
        email="kemper@fiscalapi.com",
    ))


def factura_ce_traslado_traslado_por_referencias():
    print("=== 8. Factura CE Traslado Traslado (Por Referencias) ===")
    factura_ce_traslado_traslado_update_people()

    invoice = Invoice(
        version_code="4.0",
        currency_code="USD",
        type_code="T",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=issuer_id),
        items=[
            InvoiceItem(
                item_code="50211503",
                item_sku="131494-1055",
                quantity=Decimal("2"),
                unit_of_measurement_code="H87",
                description="Cigarros",
                unit_price=Decimal("200.00"),
                discount=Decimal("0"),
                tax_object_code="01",
                item_taxes=[],
            ),
        ],
        complement=InvoiceComplement(
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FOB",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="ST. A",
                        estado="TX",
                        pais_id="USA",
                        codigo_postal="00000",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="131494-1055",
                        fraccion_arancelaria_id="2402200100",
                        cantidad_aduana=Decimal("117.64"),
                        unidad_aduana_id="01",
                        valor_unitario_aduana=Decimal("3.40"),
                        valor_dolares=Decimal("400.00"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# 9. Factura CE Unidades De Medida No Equivalentes
# ============================================================================
def factura_ce_unidades_de_medida_no_equivalentes_update_people():
    client.people.update(kemper_issuer_person())
    client.people.update(Person(
        id=recipient_id,
        tin="XEXX010101000",
        legal_name="U.S. 0026 SW",
        zip_code="42501",
        sat_tax_regime_id="616",
        sat_cfdi_use_id="CP01",
        country_id="USA",
        foreign_tin="123456789",
        email="karla.fuentes@fiscalapi.com",
    ))


def factura_ce_unidades_de_medida_no_equivalentes_por_referencias():
    print("=== 9. Factura CE Unidades De Medida No Equivalentes (Por Referencias) ===")
    factura_ce_unidades_de_medida_no_equivalentes_update_people()

    invoice = Invoice(
        version_code="4.0",
        payment_form_code="99",
        payment_method_code="PPD",
        currency_code="USD",
        type_code="I",
        expedition_zip_code="42501",
        series="CCE",
        date=current_date,
        payment_conditions="CondicionesDePago",
        export_code="02",
        issuer=InvoiceIssuer(id=issuer_id),
        recipient=InvoiceRecipient(id=recipient_id),
        items=[
            InvoiceItem(
                item_code="50201708",
                item_sku="131494-1055",
                quantity=Decimal("1.000"),
                unit_of_measurement_code="H87",
                description="Bebida",
                unit_price=Decimal("100.00"),
                discount=Decimal("0"),
                tax_object_code="02",
                item_taxes=[
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T"),
                    ItemTax(tax_code="001", tax_type_code="Tasa", tax_rate=Decimal("0.100000"), tax_flag_code="R"),
                    ItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.106666"), tax_flag_code="R"),
                ],
            ),
        ],
        complement=InvoiceComplement(
            comercio_exterior=ComercioExteriorComplement(
                clave_de_pedimento_id="A1",
                certificado_origen=0,
                incoterm_id="FOB",
                tipo_cambio_usd=tipo_cambio,
                emisor=ComercioExteriorEmisor(
                    domicilio=ComercioExteriorEmisorDomicilio(
                        calle="CALLE DEL PAPEL",
                        colonia_id="0214",
                        localidad_id="01",
                        municipio_id="014",
                        estado_id="QUE",
                        pais_id="MEX",
                        codigo_postal_id="76199",
                    ),
                ),
                receptor=ComercioExteriorReceptor(
                    num_reg_id_trib="123456789",
                    domicilio=ComercioExteriorReceptorDomicilio(
                        calle="ST. A",
                        estado="TX",
                        pais_id="USA",
                        codigo_postal="00000",
                    ),
                ),
                mercancias=[
                    ComercioExteriorMercancia(
                        no_identificacion="131494-1055",
                        fraccion_arancelaria_id="2009310201",
                        cantidad_aduana=Decimal("0.500"),
                        unidad_aduana_id="08",
                        valor_unitario_aduana=Decimal("200.00"),
                        valor_dolares=Decimal("100.00"),
                    ),
                ],
            ),
        ),
    )

    print_response(client.invoices.create(invoice))


# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
     factura_ce_ingreso_con_carta_porte_31_por_referencias()
    # factura_ce_ingreso_diferentes_monedas_por_referencias()
    # factura_ce_kit_parte_por_referencias()
    # factura_ce_receptor_extranjero_por_referencias()
    # factura_ce_receptor_nacional_por_referencias()
    # factura_ce_traslado_con_carta_porte_31_por_referencias()
    # factura_ce_traslado_traslado_mercancia_propia_por_referencias()
    # factura_ce_traslado_traslado_por_referencias()
    # factura_ce_unidades_de_medida_no_equivalentes_por_referencias()
