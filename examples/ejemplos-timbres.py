"""
Ejemplos de uso del servicio de timbres (StampService) en FiscalAPI.

Este archivo contiene ejemplos para:
- Listar transacciones de timbres
- Obtener una transaccion por ID
- Transferir timbres entre personas
- Retirar timbres
- Transferir y retirar creditos de validacion SAT
"""

from fiscalapi import CreditType, FiscalApiClient, FiscalApiSettings, StampTransactionParams

# IDs de personas para los ejemplos
TEST_LOCAL_ID = "e0dee1ae-3822-4469-af67-36de8e870a98"
LOCAL_TEST_INC_ID = "0d469952-2174-4bcf-856c-218edf7f5215"

# Configuracion del cliente
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="<API_KEY>",
    tenant="<TENANT_KEY>"
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

    Toma el ID de la primera transaccion del listado para que el ejemplo sea auto-suficiente.
    """
    print("\n" + "=" * 60)
    print("2. OBTENER TRANSACCION POR ID")
    print("=" * 60)

    listado = client.stamps.get_list(page_number=1, page_size=1)
    if not listado.succeeded or not listado.data.items:
        print("No hay transacciones para consultar.")
        return listado

    transaction_id = listado.data.items[0].id

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
        from_person_id=TEST_LOCAL_ID,
        to_person_id=LOCAL_TEST_INC_ID,
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
        from_person_id=TEST_LOCAL_ID,
        to_person_id=LOCAL_TEST_INC_ID,
        amount=1,
        comments="Retiro de timbres desde SDK Python"
    )

    api_response = client.stamps.withdraw_stamps(params)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 5. TRANSFERIR CREDITOS DE VALIDACION
# ============================================================================
def transferir_creditos_de_validacion():
    """
    Transfiere creditos de validacion SAT de una persona a otra.

    Es el mismo endpoint que los timbres; lo unico que cambia es credit_type. Los saldos nunca
    se mezclan: VALIDATION mueve available_validation_balance, STAMP mueve available_balance.
    """
    print("\n" + "=" * 60)
    print("5. TRANSFERIR CREDITOS DE VALIDACION")
    print("=" * 60)

    params = StampTransactionParams(
        from_person_id=TEST_LOCAL_ID,
        to_person_id=LOCAL_TEST_INC_ID,
        amount=1,
        comments="Transferencia de creditos de validacion desde SDK Python",
        credit_type=CreditType.VALIDATION
    )

    api_response = client.stamps.transfer_stamps(params)
    print(f"Response: {api_response}")
    return api_response


# ============================================================================
# 6. RETIRAR CREDITOS DE VALIDACION
# ============================================================================
def retirar_creditos_de_validacion():
    """
    Retira creditos de validacion SAT de una persona.

    Un retiro es una transferencia con origen y destino invertidos.
    """
    print("\n" + "=" * 60)
    print("6. RETIRAR CREDITOS DE VALIDACION")
    print("=" * 60)

    params = StampTransactionParams(
        from_person_id=LOCAL_TEST_INC_ID,
        to_person_id=TEST_LOCAL_ID,
        amount=1,
        comments="Retiro de creditos de validacion desde SDK Python",
        credit_type=CreditType.VALIDATION
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

    # 5. Transferir creditos de validacion
    transferir_creditos_de_validacion()

    # 6. Retirar creditos de validacion
    retirar_creditos_de_validacion()


if __name__ == "__main__":
    main()
