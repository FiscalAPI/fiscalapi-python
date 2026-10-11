"""
Ejemplos de uso del servicio de tickets de Auto CFDI (TicketService) en FiscalAPI.

Este archivo contiene ejemplos para:
- Ingerir un ticket (venta pagada del punto de venta) con Idempotency-Key
- Listar los tickets pendientes de un emisor en un periodo (para la factura global)
- Consultar el detalle, reimprimir el codigo y cancelar un ticket

Reglas del endpoint POST /api/v4/tickets:
- Ingerir un ticket cobra 1 credito de ticket al emisor.
- Con Idempotency-Key, repetir la misma key con el mismo cuerpo responde 200 con el ticket original sin cobrar otra vez.
- El total debe cuadrar al centavo con los conceptos e impuestos (si no, 422 con data.expectedTotal y data.computedTotal).
- Un folio y serie ya activos del emisor responden 409 (data.existingTicketId).
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from fiscalapi import (
    FiscalApiClient,
    FiscalApiSettings,
    Ticket,
    TicketIssuer,
    TicketItem,
    TicketItemTax,
    TicketListFilters,
    TicketStatus,
)

# ID de la persona emisora (con CSD y creditos de ticket)
ISSUER_ID = "<PERSON_ID>"

# Configuracion del cliente
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="<API_KEY>",
    tenant="<TENANT_KEY>"
)

client = FiscalApiClient(settings=settings)


def construir_ticket() -> Ticket:
    """
    Arma el ticket de una venta: un refresco de 100 + IVA 16 % = 116, pagado en efectivo.
    payment_date es hora civil de Mexico (datetime sin zona).
    """
    return Ticket(
        issuer=TicketIssuer(id=ISSUER_ID),
        folio="F-1001",
        series="A",
        payment_date=datetime(2026, 10, 15, 12, 30, 0),
        payment_form_code="01",
        total=Decimal("116.00"),
        items=[TicketItem(
            item_code="50202306",
            item_sku="SKU-1",
            quantity=Decimal("1"),
            unit_of_measurement_code="H87",
            description="Refresco",
            unit_price=Decimal("100.00"),
            tax_object_code="02",
            item_taxes=[TicketItemTax(tax_code="002", tax_type_code="Tasa", tax_rate=Decimal("0.160000"), tax_flag_code="T")],
        )],
    )


def construir_filtros() -> TicketListFilters:
    """
    Tickets pendientes del emisor en octubre de 2026 (fechas civiles de Mexico, ambas incluidas).
    """
    return TicketListFilters(
        status=[TicketStatus.PENDING],
        person_id=ISSUER_ID,
        from_=date(2026, 10, 1),
        to=date(2026, 10, 31),
        page_number=1,
        page_size=50,
    )


# ============================================================================
# 1. INGERIR UN TICKET
# ============================================================================
def ingerir_ticket() -> Optional[str]:
    """
    Ingiere el ticket y devuelve su id; imprime el codigo y la URL del QR que van en el ticket de venta.
    """
    response = client.tickets.create(construir_ticket(), idempotency_key="pos-01-F-1001")
    if not response.succeeded:
        # 409: folio y serie ya activos; 422: total que no cuadra, emisor sin CSD o sin creditos de ticket, etc.
        # error_data trae el data del error: existingTicketId (409) o expectedTotal y computedTotal (422).
        print(f"Error {response.http_status_code}: {response.details} {response.error_data}")
        return None

    print(f"Codigo: {response.data.ticket_code} QR: {response.data.qr_url}")
    return response.data.id


# ============================================================================
# 2. LISTAR TICKETS PENDIENTES
# ============================================================================
def listar_pendientes() -> None:
    """
    Lista los tickets pendientes del periodo, ordenados por fecha de pago.
    """
    response = client.tickets.get_list(construir_filtros())
    if not response.succeeded:
        print(f"Error: {response.details}")
        return

    for ticket in response.data.items:
        print(f"- {ticket.series or ''}{ticket.folio} {ticket.payment_date} {ticket.total} {ticket.status}")


# ============================================================================
# 3. DETALLE, CODIGO Y CANCELACION
# ============================================================================
def consultar_y_cancelar(ticket_id: str) -> None:
    """
    Consulta el detalle con conceptos e historia, reimprime el codigo y cancela el ticket (solo en estado pending;
    el credito de ticket no se devuelve).
    """
    print(client.tickets.get_by_id(ticket_id, details=True))
    print(client.tickets.get_code(ticket_id))
    print(client.tickets.cancel(ticket_id))


if __name__ == "__main__":
    nuevo_ticket_id = ingerir_ticket()
    listar_pendientes()
    if nuevo_ticket_id:
        consultar_y_cancelar(nuevo_ticket_id)
