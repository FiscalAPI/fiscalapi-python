"""
Ejemplos de uso del servicio de timbres (StampService) en FiscalAPI.

Este archivo contiene ejemplos para:
- Listar transacciones de timbres
- Obtener una transaccion por ID
- Transferir timbres entre personas
- Retirar timbres
"""

from fiscalapi import FiscalApiClient, FiscalApiSettings, StampTransactionParams

# IDs de personas para los ejemplos
escuela_kemper_urgate_id = "2e7b988f-3a2a-4f67-86e9-3f931dd48581"
karla_fuente_nolasco_id = "109f4d94-63ea-4a21-ab15-20c8b87d8ee9"
organicos_navez_osorio_id = "f645e146-f80e-40fa-953f-fd1bd06d4e9f"
xochilt_casas_chavez_id = "e3b4edaa-e4d9-4794-9c5b-3dd5b7e372aa"
ingrid_xodar_jimenez_id = "9367249f-f0ee-43f4-b771-da2fff3f185f"
OSCAR_KALA_HAAK = "5fd9f48c-a6a2-474f-944b-88a01751d432"

# Configuracion del cliente
settings = FiscalApiSettings(
    # api_url="https://test.fiscalapi.com",
    # api_key="<API_KEY>",
    # tenant="<TENANT_KEY>",
    api_url="http://localhost:5001",
    api_key="sk_development_b470ea83_3c0f_4209_b933_85223b960d91",
    tenant="102e5f13-e114-41dd-bea7-507fce177281"
)

client = FiscalApiClient(settings=settings)


# ============================================================================
# 1. LISTAR TRANSACCIONES DE TIMBRES
# ============================================================================
def listar_transacciones():
    """
    Lista las transacciones de timbres con paginacion.
    """
    print("\n" + "=" * 60)
    print("1. LISTAR TRANSACCIONES DE TIMBRES")
    print("=" * 60)

    api_response = client.stamps.get_list(page_number=1, page_size=5)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 2. OBTENER TRANSACCION POR ID
# ============================================================================
def obtener_transaccion_por_id():
    """
    Obtiene una transaccion de timbres por su ID.
    """
    print("\n" + "=" * 60)
    print("2. OBTENER TRANSACCION POR ID")
    print("=" * 60)

    transaction_id = "77678d6d-94b1-4635-aa91-15cdd7423aab"

    api_response = client.stamps.get_by_id(transaction_id)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 3. TRANSFERIR TIMBRES
# ============================================================================
def transferir_timbres():
    """
    Transfiere timbres de una persona a otra.
    """
    print("\n" + "=" * 60)
    print("3. TRANSFERIR TIMBRES")
    print("=" * 60)

    params = StampTransactionParams(
        from_person_id=OSCAR_KALA_HAAK,
        to_person_id=karla_fuente_nolasco_id,
        amount=1,
        comments="Transferencia de prueba desde SDK Python"
    )

    api_response = client.stamps.transfer_stamps(params)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 4. RETIRAR TIMBRES
# ============================================================================
def retirar_timbres():
    """
    Retira timbres de una persona.
    """
    print("\n" + "=" * 60)
    print("4. RETIRAR TIMBRES")
    print("=" * 60)

    params = StampTransactionParams(
        from_person_id=OSCAR_KALA_HAAK,
        to_person_id=xochilt_casas_chavez_id,
        amount=1,
        comments="Retiro de timbres desde SDK Python"
    )

    api_response = client.stamps.withdraw_stamps(params)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# MAIN
# ============================================================================
def main():
    """
    Ejecuta todos los ejemplos de timbres.
    """
    # 1. Listar transacciones
    listar_transacciones()

    # 2. Obtener transaccion por ID
    obtener_transaccion_por_id()

    # 3. Transferir timbres
    transferir_timbres()

    # 4. Retirar timbres
    retirar_timbres()


if __name__ == "__main__":
    main()
