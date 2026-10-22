"""Modelos de tickets de Auto CFDI (endpoints /api/v4/tickets).

Un ticket es una venta pagada del punto de venta que el receptor puede autofacturar o que entra a una factura global.
Ingerirlo cobra 1 crédito de ticket. Los conceptos e impuestos llevan los nombres de los conceptos de las facturas.
"""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class TicketStatus(str, Enum):
    """Estados de un ticket, como llegan en ``Ticket.status`` (texto camelCase)."""

    PENDING = "pending"
    INVOICING = "invoicing"
    INVOICED = "invoiced"
    GLOBALIZING = "globalizing"
    GLOBALIZED = "globalized"
    CANCELLED = "cancelled"


class TicketEventType(str, Enum):
    """Tipos de hecho de la historia de un ticket, como llegan en ``TicketEvent.type``."""

    INGESTED = "ingested"
    INVOICING_STARTED = "invoicingStarted"
    INVOICED = "invoiced"
    INVOICE_REJECTED = "invoiceRejected"
    OUTCOME_UNKNOWN = "outcomeUnknown"
    LEASE_EXPIRED = "leaseExpired"
    GLOBALIZING = "globalizing"
    GLOBALIZED = "globalized"
    RELEASED_FROM_GLOBAL = "releasedFromGlobal"
    CANCELLED = "cancelled"
    RECOVERY_FAILED = "recoveryFailed"
    RECOVERED = "recovered"
    RESENT = "resent"
    RETURNED_TO_PENDING = "returnedToPending"


class TicketActorType(str, Enum):
    """Quién actuó en un hecho del ticket, como llega en ``TicketEvent.actor_type``."""

    TENANT = "tenant"
    PORTAL = "portal"
    SYSTEM = "system"


class TicketIssuer(BaseModel):
    """Emisor de un ticket: una persona del tenant, por su id."""

    id: Optional[str] = Field(default=None, alias="id", description="Id de la persona emisora.")

    model_config = ConfigDict(populate_by_name=True)


class TicketItemTax(BaseModel):
    """Impuesto de un concepto del ticket."""

    tax_code: Optional[str] = Field(default=None, alias="taxCode", description="Impuesto: 001 (ISR), 002 (IVA) o 003 (IEPS).")
    tax_type_code: Optional[str] = Field(default=None, alias="taxTypeCode", description="Tipo de factor: Tasa, Cuota o Exento.")
    tax_rate: Optional[Decimal] = Field(default=None, alias="taxRate", description="Tasa o cuota; se envía tal cual, sin redondear.")
    tax_flag_code: Optional[str] = Field(default=None, alias="taxFlagCode", description="T (traslado) o R (retención).")

    model_config = ConfigDict(populate_by_name=True)


class TicketItem(BaseModel):
    """Concepto de un ticket, con los nombres de los conceptos de las facturas (sin terceros, aduanas, predial ni partes)."""

    item_code: Optional[str] = Field(default=None, alias="itemCode", description="Clave de producto o servicio (c_ClaveProdServ).")
    item_sku: Optional[str] = Field(default=None, alias="itemSku", description="Número de identificación (SKU) del producto en el punto de venta.")
    quantity: Optional[Decimal] = Field(default=None, alias="quantity", description="Cantidad.")
    unit_of_measurement_code: Optional[str] = Field(default=None, alias="unitOfMeasurementCode", description="Clave de unidad (c_ClaveUnidad).")
    description: Optional[str] = Field(default=None, alias="description", description="Descripción.")
    unit_price: Optional[Decimal] = Field(default=None, alias="unitPrice", description="Valor unitario.")
    discount: Optional[Decimal] = Field(default=None, alias="discount", description="Descuento del concepto. Opcional.")
    tax_object_code: Optional[str] = Field(default=None, alias="taxObjectCode", description="Objeto de impuesto (c_ObjetoImp): 02 exige impuestos; 01, 03, 04 y 05 no admiten.")
    item_taxes: Optional[list[TicketItemTax]] = Field(default=None, alias="itemTaxes", description="Impuestos del concepto.")

    model_config = ConfigDict(populate_by_name=True)


class TicketEvent(BaseModel):
    """Un hecho de la historia del ticket (solo lectura; llega con ``details=True``).

    ``type`` y ``actor_type`` llegan como miembro del enum si el SDK los conoce y como texto si no.
    """

    type: Optional[Union[TicketEventType, str]] = Field(default=None, alias="type", union_mode="left_to_right", description="Tipo de hecho; uno que el SDK no conoce llega como texto.")
    occurred_at: Optional[datetime] = Field(default=None, alias="occurredAt", description="Momento del hecho.")
    actor_type: Optional[Union[TicketActorType, str]] = Field(default=None, alias="actorType", union_mode="left_to_right", description="Quién actuó; uno que el SDK no conoce llega como texto.")
    invoice_id: Optional[str] = Field(default=None, alias="invoiceId", description="Factura del hecho; None si no aplica.")

    model_config = ConfigDict(populate_by_name=True)


class Ticket(BaseModel):
    """Ticket de Auto CFDI: se envía en ``tickets.create`` y llega en ``tickets.get_list`` y ``tickets.get_by_id``.

    Los miembros de solo lectura (id, person_id, importes calculados, status, vigencia, facturas, created_at y events)
    los asigna el API: al crear quedan en None y no se envían.
    """

    id: Optional[str] = Field(default=None, alias="id", description="Id del ticket. Solo lectura.")
    issuer: Optional[TicketIssuer] = Field(default=None, alias="issuer", description="Emisor por referencia. Se envía al crear; no llega en las consultas.")
    person_id: Optional[str] = Field(default=None, alias="personId", description="Persona emisora del tenant. Solo lectura.")
    folio: Optional[str] = Field(default=None, alias="folio", description="Folio del punto de venta (no es el folio del CFDI).")
    series: Optional[str] = Field(default=None, alias="series", description="Serie del punto de venta. Opcional.")
    payment_date: Optional[datetime] = Field(default=None, alias="paymentDate", description="Momento del pago en hora civil de México; un datetime sin zona viaja como yyyy-MM-ddTHH:mm:ss.")
    payment_form_code: Optional[str] = Field(default=None, alias="paymentFormCode", description="Forma de pago (c_FormaPago), por ejemplo 01 (efectivo).")
    currency_code: Optional[str] = Field(default=None, alias="currencyCode", description="Moneda (c_Moneda). Opcional: sin ella, el API usa MXN.")
    exchange_rate: Optional[Decimal] = Field(default=None, alias="exchangeRate", description="Tipo de cambio. Opcional.")
    expedition_zip_code: Optional[str] = Field(default=None, alias="expeditionZipCode", description="Código postal de expedición. Opcional: sin él, el API usa el del emisor.")
    subtotal: Optional[Decimal] = Field(default=None, alias="subtotal", description="Subtotal calculado por el API. Solo lectura.")
    total_transferred_taxes: Optional[Decimal] = Field(default=None, alias="totalTransferredTaxes", description="Total de impuestos trasladados calculado por el API. Solo lectura.")
    total_withheld_taxes: Optional[Decimal] = Field(default=None, alias="totalWithheldTaxes", description="Total de impuestos retenidos calculado por el API. Solo lectura.")
    total: Optional[Decimal] = Field(default=None, alias="total", description="Total que cobró el punto de venta: debe cuadrar al centavo con el calculado (si no, 422).")
    status: Optional[Union[TicketStatus, str]] = Field(default=None, alias="status", union_mode="left_to_right", description="Estado del ticket. Solo lectura; uno que el SDK no conoce llega como texto.")
    self_invoice_eligible: Optional[bool] = Field(default=None, alias="selfInvoiceEligible", description="Si hoy el receptor puede autofacturarlo. Solo lectura.")
    eligible_until: Optional[datetime] = Field(default=None, alias="eligibleUntil", description="Último momento de la ventana de autofactura; None si no cierra. Solo lectura.")
    invoice_id: Optional[str] = Field(default=None, alias="invoiceId", description="Factura individual (estado invoiced). Solo lectura.")
    global_invoice_id: Optional[str] = Field(default=None, alias="globalInvoiceId", description="Factura global (estado globalized). Solo lectura.")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt", description="Fecha de alta. Solo lectura.")
    items: Optional[list[TicketItem]] = Field(default=None, alias="items", description="Conceptos. Obligatorios al crear; en las consultas solo llegan con details=True.")
    events: Optional[list[TicketEvent]] = Field(default=None, alias="events", description="Historia del ticket en orden. Solo lectura; solo llega con details=True.")

    model_config = ConfigDict(populate_by_name=True)


class TicketIngestionResult(BaseModel):
    """Respuesta de ``tickets.create``: un ticket nuevo (201) y la repetición con la misma llave de idempotencia y el mismo
    cuerpo devuelven la misma respuesta original."""

    id: Optional[str] = Field(default=None, alias="id", description="Id del ticket.")
    ticket_code: Optional[str] = Field(default=None, alias="ticketCode", description="Código sin guiones, como lo lleva el QR; se imprime en grupos (XXXX-XXXX-XXXX).")
    qr_url: Optional[str] = Field(default=None, alias="qrUrl", description="URL del portal de autofactura que abre el ticket.")
    status: Optional[Union[TicketStatus, str]] = Field(default=None, alias="status", union_mode="left_to_right", description="Estado actual (al ingerir, pending); uno que el SDK no conoce llega como texto.")
    self_invoice_eligible: Optional[bool] = Field(default=None, alias="selfInvoiceEligible", description="Si hoy el receptor puede autofacturarlo.")
    eligible_until: Optional[datetime] = Field(default=None, alias="eligibleUntil", description="Último momento de la ventana de autofactura; None si no cierra.")
    subtotal: Optional[Decimal] = Field(default=None, alias="subtotal", description="Subtotal calculado.")
    total_transferred_taxes: Optional[Decimal] = Field(default=None, alias="totalTransferredTaxes", description="Total de impuestos trasladados calculado.")
    total_withheld_taxes: Optional[Decimal] = Field(default=None, alias="totalWithheldTaxes", description="Total de impuestos retenidos calculado.")
    total: Optional[Decimal] = Field(default=None, alias="total", description="Total calculado (cuadra con el enviado).")

    model_config = ConfigDict(populate_by_name=True)


class TicketCodeResult(BaseModel):
    """Código de un ticket y la URL de su QR, para reimprimirlo (GET /api/v4/tickets/{id}/code)."""

    ticket_code: Optional[str] = Field(default=None, alias="ticketCode", description="Código sin guiones, el mismo de la ingesta.")
    qr_url: Optional[str] = Field(default=None, alias="qrUrl", description="URL del portal de autofactura que abre el ticket.")

    model_config = ConfigDict(populate_by_name=True)


class TicketListFilters(BaseModel):
    """Filtros de ``tickets.get_list`` (GET /api/v4/tickets). Cada filtro aplica solo si se asigna; los que quedan en
    None no se envían. ``from_`` lleva el guion bajo porque ``from`` es palabra reservada de Python."""

    status: Optional[list[Union[TicketStatus, str]]] = Field(default=None, alias="status", description="Uno o más estados; se envían repitiendo la llave status.")
    person_id: Optional[str] = Field(default=None, alias="personId", description="Persona emisora.")
    details: Optional[bool] = Field(default=None, alias="details", description="Con true, cada ticket trae sus conceptos con impuestos (sin la historia).")
    global_invoice_id: Optional[str] = Field(default=None, alias="globalInvoiceId", description="Factura global que ampara los tickets.")
    from_: Optional[date] = Field(default=None, alias="from", description="Primer día del pago (incluido), en fecha civil de México.")
    to: Optional[date] = Field(default=None, alias="to", description="Último día del pago (incluido), en fecha civil de México.")
    page_number: Optional[int] = Field(default=None, alias="pageNumber", description="Página, desde 1. Sin ella, el API devuelve la primera.")
    page_size: Optional[int] = Field(default=None, alias="pageSize", description="Tamaño de página (1 a 50). Sin él, el API usa 10.")

    model_config = ConfigDict(populate_by_name=True)

    def to_query_params(self) -> list[tuple[str, str]]:
        """Los filtros asignados como pares de la query string: ``status`` se repite por cada estado, y ``details``
        solo viaja como ``true`` (``False`` no se envía)."""
        params: list[tuple[str, str]] = []
        for key, value in self.model_dump(mode="json", by_alias=True, exclude_none=True).items():
            values = value if isinstance(value, list) else [value]
            params.extend((key, "true" if item is True else str(item)) for item in values if item is not False)
        return params
