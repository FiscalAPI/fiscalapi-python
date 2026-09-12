"""
Ejemplos de uso del servicio de validaciones SAT (SatValidationService) en FiscalAPI.

Este archivo contiene ejemplos para:
- Listar los tipos de validacion disponibles
- Obtener un tipo de validacion por ID
- Listar los estatus posibles de un tipo de validacion
- Validar un CFDI timbrado (todas las validaciones)
- Validar un RFC en listas negras (sin CFDI)
- Consultar el saldo de creditos de validacion

Reglas del endpoint POST /api/v4/sat-validations:
- Se envia xml (CFDI timbrado en base64) o tin (RFC), nunca ambos y nunca ninguno.
- Con xml se puede solicitar cualquier tipo de validacion.
- Con tin solo se pueden solicitar listas negras (sat.blacklist.69b, sat.blacklist.69bbis).
- Cada tipo solicitado consume un credito de validacion. El cobro es todo o nada: si el saldo
  no alcanza para todos, no se ejecuta ninguno y la API responde 403.
"""

import base64
from pathlib import Path

from fiscalapi import (
    FiscalApiClient,
    FiscalApiSettings,
    SatValidationRequest,
    SatValidationTypeIds,
)

# CFDI timbrado real usado por los ejemplos
RUTA_CFDI = Path(r"C:\facturas\FacturaXml.xml")

# RFC del emisor del CFDI anterior, para los ejemplos de listas negras por RFC
RFC_EMISOR = "MAX0611157H8"

# ID de la persona duena del API key: es a quien se le cobran los creditos de validacion
LOCAL_TEST_INC_ID = "0d469952-2174-4bcf-856c-218edf7f5215"

# Configuracion del cliente
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="<API_KEY>",
    tenant="<TENANT_KEY>"
)

client = FiscalApiClient(settings=settings)


def leer_cfdi_en_base64() -> str:
    """
    Lee el CFDI timbrado del disco y lo codifica en base64, que es lo que espera el campo xml.
    """
    return base64.b64encode(RUTA_CFDI.read_bytes()).decode("ascii")


def imprimir_resultados(api_response) -> None:
    """
    Imprime un resultado por linea: veredicto, tipo, estatus y los hechos del caso si los hay.
    """
    if not api_response.succeeded:
        print(f"Error: {api_response.details}")
        return

    for result in api_response.data:
        veredicto = "PASSED" if result.passed else "FAILED"
        print(f"[{veredicto}] {result.type.id.value} -> {result.status.id.value}")
        if result.status.details:
            print(f"          {result.status.details}")


# ============================================================================
# 1. LISTAR TIPOS DE VALIDACION
# ============================================================================
def listar_tipos_de_validacion():
    """
    Lista los tipos de validacion SAT disponibles, en el orden del catalogo.
    """
    print("\n" + "=" * 60)
    print("1. LISTAR TIPOS DE VALIDACION")
    print("=" * 60)

    api_response = client.sat_validations.get_types()

    if api_response.succeeded:
        for validation_type in api_response.data:
            print(f"{validation_type.id.value}: {validation_type.description[:80]}...")
    else:
        print(f"Error: {api_response.details}")

    return api_response


# ============================================================================
# 2. OBTENER TIPO DE VALIDACION POR ID
# ============================================================================
def obtener_tipo_por_id():
    """
    Obtiene un tipo de validacion por su ID.
    """
    print("\n" + "=" * 60)
    print("2. OBTENER TIPO DE VALIDACION POR ID")
    print("=" * 60)

    api_response = client.sat_validations.get_type_by_id(SatValidationTypeIds.CFDI_STATUS)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 3. LISTAR ESTATUS DE UN TIPO DE VALIDACION
# ============================================================================
def listar_estatus_de_un_tipo():
    """
    Lista los estatus que un tipo de validacion puede tomar al ejecutarse.
    No ejecuta la validacion ni consume creditos.
    """
    print("\n" + "=" * 60)
    print("3. LISTAR ESTATUS DE UN TIPO DE VALIDACION")
    print("=" * 60)

    api_response = client.sat_validations.get_statuses(SatValidationTypeIds.CFDI_STATUS)

    if api_response.succeeded:
        for status in api_response.data:
            print(f"{status.id.value}: {status.description[:80]}...")
    else:
        print(f"Error: {api_response.details}")

    return api_response


# ============================================================================
# 4. VALIDAR UN CFDI TIMBRADO (TODAS LAS VALIDACIONES)
# ============================================================================
def validar_cfdi_completo():
    """
    Ejecuta las siete validaciones SAT sobre un CFDI timbrado. Consume 7 creditos.
    """
    print("\n" + "=" * 60)
    print("4. VALIDAR UN CFDI TIMBRADO (TODAS LAS VALIDACIONES)")
    print("=" * 60)

    request = SatValidationRequest(
        xml=leer_cfdi_en_base64(),
        validation_types=[
            SatValidationTypeIds.XML_STRUCTURE,
            SatValidationTypeIds.CERTIFICATE_VALIDITY,
            SatValidationTypeIds.CFDI_SELLO,
            SatValidationTypeIds.TFD_SELLO,
            SatValidationTypeIds.CFDI_STATUS,
            SatValidationTypeIds.BLACKLIST_69B,
            SatValidationTypeIds.BLACKLIST_69B_BIS,
        ]
    )

    api_response = client.sat_validations.validate(request)
    imprimir_resultados(api_response)
    return api_response


# ============================================================================
# 5. VALIDAR UN RFC EN LISTAS NEGRAS (SIN CFDI)
# ============================================================================
def validar_listas_negras_por_rfc():
    """
    Consulta un RFC en las listas negras 69-B y 69-B Bis sin enviar el CFDI.
    Con tin solo se pueden solicitar listas negras. Consume 2 creditos.
    """
    print("\n" + "=" * 60)
    print("5. VALIDAR UN RFC EN LISTAS NEGRAS (SIN CFDI)")
    print("=" * 60)

    request = SatValidationRequest(
        tin=RFC_EMISOR,
        validation_types=[
            SatValidationTypeIds.BLACKLIST_69B,
            SatValidationTypeIds.BLACKLIST_69B_BIS,
        ]
    )

    api_response = client.sat_validations.validate(request)
    imprimir_resultados(api_response)
    return api_response


# ============================================================================
# 6. CONSULTAR SALDO DE CREDITOS DE VALIDACION
# ============================================================================
def consultar_saldo_de_validaciones():
    """
    Consulta el saldo de creditos de validacion de la persona duena del API key, que es a
    quien la API le cobra cada validacion ejecutada.

    Es independiente del saldo de timbres: los saldos nunca se mezclan.
    """
    print("\n" + "=" * 60)
    print("6. CONSULTAR SALDO DE CREDITOS DE VALIDACION")
    print("=" * 60)

    api_response = client.people.get_by_id(LOCAL_TEST_INC_ID)

    if api_response.succeeded and api_response.data:
        print(f"Timbres disponibles:      {api_response.data.available_balance}")
        print(f"Validaciones disponibles: {api_response.data.available_validation_balance}")
    else:
        print(f"Error: {api_response.details}")

    return api_response


# ============================================================================
# MAIN
# ============================================================================
def main():
    """
    Ejecuta todos los ejemplos de validaciones SAT.
    """
    # 1. Listar tipos de validacion
    listar_tipos_de_validacion()

    # 2. Obtener tipo de validacion por ID
    obtener_tipo_por_id()

    # 3. Listar estatus de un tipo de validacion
    listar_estatus_de_un_tipo()

    # 4. Saldo antes de validar
    consultar_saldo_de_validaciones()

    # 5. Validar un CFDI timbrado (consume 7 creditos)
    validar_cfdi_completo()

    # 6. Validar un RFC en listas negras (consume 2 creditos)
    validar_listas_negras_por_rfc()

    # 7. Saldo despues de validar: debe haber bajado 9 creditos
    consultar_saldo_de_validaciones()


if __name__ == "__main__":
    main()
