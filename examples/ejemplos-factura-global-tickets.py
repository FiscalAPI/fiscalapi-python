"""
Ejemplo de factura global de tickets de Auto CFDI (POST /api/v4/invoices) en FiscalAPI.

La global de tickets es una factura de ingreso estandar (invoices.create) con global_information, el emisor por
referencia (issuer.id) y ticket_id en cada concepto:
- Cada ticket va en un concepto por grupo de objeto de impuesto e impuestos (un ticket con IVA 16 % y 0 % lleva dos
  conceptos con el mismo ticket_id); la suma de sus conceptos debe reflejar el ticket (si no, 400 en items[i].ticketId).
- Si algun ticket ya no esta pendiente, 409 con data.unavailableTickets (en error_data): no se cobra el timbre ni queda
  tomado ningun ticket.
- Una global lleva una sola moneda, tipo de cambio y lugar de expedicion, y hasta 1,500 conceptos: este ejemplo asume
  tickets en MXN de un solo lugar de expedicion.
- Una global sin ticket_id no marca los tickets.
"""

from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal

from fiscalapi import (
    FiscalApiClient,
    FiscalApiSettings,
    GlobalInformation,
    Invoice,
    InvoiceIssuer,
    InvoiceItem,
    InvoiceRecipient,
    ItemTax,
    Ticket,
    TicketItem,
    TicketListFilters,
    TicketStatus,
)

# ID de la persona emisora (con CSD)
ISSUER_ID = "<PERSON_ID>"

# Importes del CFDI: 6 decimales, redondeo lejos de cero en el medio (como los calcula el API)
SIX_DECIMALS = Decimal("0.000001")

# Configuracion del cliente
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="<API_KEY>",
    tenant="<TENANT_KEY>"
)

client = FiscalApiClient(settings=settings)


# ============================================================================
# 1. TICKETS PENDIENTES DEL PERIODO, CON SUS CONCEPTOS
# ============================================================================
def tickets_pendientes() -> list[Ticket]:
    """
    Tickets pendientes del emisor en septiembre de 2026, con el detalle de cada uno (conceptos e impuestos).
    """
    tickets: list[Ticket] = []
    page_number = 1
    while True:
        response = client.tickets.get_list(TicketListFilters(
            status=[TicketStatus.PENDING],
            person_id=ISSUER_ID,
            from_=date(2026, 9, 1),
            to=date(2026, 9, 30),
            page_number=page_number,
            page_size=50,
        ))
        if not response.succeeded:
            raise RuntimeError(f"Error {response.http_status_code}: {response.details}")
        for summary in response.data.items:
            tickets.append(client.tickets.get_by_id(summary.id, details=True).data)
        if not response.data.has_next_page:
            return tickets
        page_number += 1


# ============================================================================
# 2. UN CONCEPTO POR TICKET Y GRUPO DE IMPUESTOS
# ============================================================================
def firma_de_impuestos(item: TicketItem) -> str:
    """Objeto de impuesto e impuestos del concepto, sin importar el orden de los impuestos."""
    impuestos = sorted(
        f"{tax.tax_code}|{tax.tax_type_code}|{tax.tax_rate.quantize(SIX_DECIMALS)}|{tax.tax_flag_code}"
        for tax in item.item_taxes or []
    )
    return ";".join([item.tax_object_code or "", *impuestos])


def conceptos_del_ticket(ticket: Ticket) -> list[InvoiceItem]:
    """
    Valor unitario = suma de cantidad x valor unitario (6 decimales por concepto); descuento = suma de descuentos.
    """
    grupos: dict[str, list[TicketItem]] = {}
    for item in ticket.items or []:
        grupos.setdefault(firma_de_impuestos(item), []).append(item)

    return [
        InvoiceItem(
            ticket_id=ticket.id,
            item_code="01010101",
            item_sku=ticket.folio,  # NoIdentificacion: folio del ticket
            quantity=Decimal("1"),
            unit_of_measurement_code="ACT",
            description="Venta",
            unit_price=sum(
                ((item.quantity * item.unit_price).quantize(SIX_DECIMALS, rounding=ROUND_HALF_UP) for item in items),
                Decimal("0"),
            ),
            discount=sum((item.discount or Decimal("0") for item in items), Decimal("0")),
            tax_object_code=items[0].tax_object_code,
            item_taxes=[
                ItemTax(
                    tax_code=tax.tax_code,
                    tax_type_code=tax.tax_type_code,
                    tax_rate=tax.tax_rate,
                    tax_flag_code=tax.tax_flag_code,
                )
                for tax in items[0].item_taxes or []
            ],
        )
        for items in grupos.values()
    ]


# ============================================================================
# 3. LA FACTURA GLOBAL
# ============================================================================
def factura_global(tickets: list[Ticket]) -> Invoice:
    """
    Global mensual de septiembre de 2026 a publico en general. La forma de pago es la del ticket de mayor monto.
    """
    lugar_de_expedicion = tickets[0].expedition_zip_code
    mayor = max(tickets, key=lambda ticket: ticket.total)
    return Invoice(
        version_code="4.0",
        series="G",
        date=datetime.now(),
        payment_form_code=mayor.payment_form_code,
        payment_method_code="PUE",
        currency_code="MXN",
        type_code="I",
        expedition_zip_code=lugar_de_expedicion,
        export_code="01",
        issuer=InvoiceIssuer(id=ISSUER_ID),
        recipient=InvoiceRecipient(
            tin="XAXX010101000",
            legal_name="PUBLICO EN GENERAL",
            zip_code=lugar_de_expedicion,
            tax_regime_code="616",
            cfdi_use_code="S01",
        ),
        global_information=GlobalInformation(periodicity_code="04", month_code="09", year=2026),
        items=[concepto for ticket in tickets for concepto in conceptos_del_ticket(ticket)],
    )


def timbrar_global() -> None:
    tickets = tickets_pendientes()
    if not tickets:
        print("No hay tickets pendientes en el periodo.")
        return

    response = client.invoices.create(factura_global(tickets))
    if response.succeeded:
        print(f"Global timbrada: {response.data.uuid}")
    elif response.http_status_code == 409:
        # Algun ticket ya no estaba pendiente: no se cobro el timbre ni quedo tomado ningun ticket.
        for unavailable in response.error_data["unavailableTickets"]:
            print(f"- {unavailable['ticketId']}: {unavailable['status']}")
    else:
        # 400 en items[i].ticketId: los conceptos de ese ticket no lo reflejan (importes, descuentos o impuestos).
        print(f"Error {response.http_status_code}: {response.details}")


if __name__ == "__main__":
    timbrar_global()
