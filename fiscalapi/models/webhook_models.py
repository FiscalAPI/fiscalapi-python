"""Modelos de los eventos de webhook de FiscalAPI: el mismo sobre para todo tipo de evento.

Un ``WebhookEvent`` lo devuelve ``fiscalapi.webhooks.verify`` después de validar la firma de la entrega. Es una
notificación ligera: para el estado autoritativo del recurso (el orden de llegada no está garantizado), consulte
``data.related_object`` con el servicio de su tipo (por ejemplo ``client.invoices.get_by_id``).
"""

from datetime import datetime, timezone
from typing import Final, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WebhookEventTypes:
    """Tipos de evento de webhook, como llegan en ``WebhookEvent.type``.

    Los de un cambio de estado nombran el estado al que llegó el recurso. Son una ayuda para comparar
    (``event.type == WebhookEventTypes.INVOICE_CANCELED``): el catálogo puede crecer y un tipo desconocido se ignora.
    """

    INVOICE_CANCELLATION_REQUESTED: Final = "invoice.cancellation_requested"
    """La factura pasó de vigente a cancelación en proceso (``V`` → ``C``)."""

    INVOICE_CANCELED: Final = "invoice.canceled"
    """La cancelación en proceso terminó y la factura quedó cancelada (``C`` → ``X``)."""

    INVOICE_CANCELLATION_REJECTED: Final = "invoice.cancellation_rejected"
    """La cancelación en proceso se rechazó y la factura volvió a vigente (``C`` → ``V``)."""

    DOWNLOAD_REQUEST_COMPLETED: Final = "download_request.completed"
    """La solicitud de descarga masiva terminó con éxito (→ ``3``)."""

    DOWNLOAD_REQUEST_ABANDONED: Final = "download_request.abandoned"
    """La solicitud de descarga masiva se abandonó (→ ``-1``). No implica un error: el motivo está en la solicitud
    (``client.download_requests.get_by_id``)."""

    DOWNLOAD_RULE_SUSPENDED: Final = "download_rule.suspended"
    """La regla de descarga masiva quedó suspendida (``2`` → ``4``)."""

    WEBHOOK_ENDPOINT_TEST: Final = "webhook_endpoint.test"
    """Prueba de un endpoint: no se suscribe; solo llega al pulsar "Enviar prueba"
    (``POST webhook-endpoints/{id}/test``), y solo a ese endpoint. Su ``related_object`` es el endpoint mismo
    (``webhook_endpoint``), sin persona ni estados."""


class WebhookRelatedObject(BaseModel):
    """El recurso al que se refiere un ``WebhookEvent``."""

    id: Optional[str] = Field(default=None, alias="id", description="Id del recurso: el que reciben los get_by_id de los servicios del SDK.")
    type: Optional[str] = Field(default=None, alias="type", description="Tipo de recurso: invoice, download_request, download_rule o webhook_endpoint; el conjunto puede crecer.")
    url: Optional[str] = Field(default=None, alias="url", description="Ruta relativa del GET v4 del recurso (por ejemplo /api/v4/invoices/{id}), sin host: el mismo evento es idéntico en pruebas y en producción. Para leer el recurso use su servicio con id.")

    model_config = ConfigDict(populate_by_name=True)


class WebhookEventData(BaseModel):
    """Datos de un ``WebhookEvent``."""

    related_object: Optional[WebhookRelatedObject] = Field(default=None, alias="relatedObject", description="El recurso que cambió de estado.")
    status: Optional[str] = Field(default=None, alias="status", description="Estado al que llegó el recurso, con los códigos públicos de la API v4 (factura V, C, X; solicitud de descarga 1, 2, 3, -1; regla de descarga 1..4, -1); None si el tipo de evento no lo lleva.")
    previous_status: Optional[str] = Field(default=None, alias="previousStatus", description="Estado del que salió el recurso, con los mismos códigos que status; None si no aplica.")

    model_config = ConfigDict(populate_by_name=True)


class WebhookEvent(BaseModel):
    """Un evento de webhook de FiscalAPI: el mismo sobre para todo tipo de evento, sin clases por tipo.

    Lo devuelve ``fiscalapi.webhooks.verify``. Los campos que esta versión del SDK no conoce se ignoran sin error.
    """

    id: Optional[str] = Field(default=None, alias="id", description="Id del evento; es también el header webhook-id y no cambia entre reintentos: úselo para descartar entregas repetidas.")
    type: Optional[str] = Field(default=None, alias="type", description="Tipo de evento (ver WebhookEventTypes). Es texto y no un enum: un tipo que esta versión del SDK no conoce llega tal cual, sin error, y se ignora.")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt", description="Momento del cambio de estado, en UTC (tzinfo timezone.utc), al segundo.")
    person_id: Optional[str] = Field(default=None, alias="personId", description="Persona del tenant dueña del recurso; None si el recurso no tiene una (factura emitida por valores).")
    data: Optional[WebhookEventData] = Field(default=None, alias="data", description="El recurso que cambió y sus estados.")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("created_at")
    @classmethod
    def _in_utc(cls, value: Optional[datetime]) -> Optional[datetime]:
        # El back envía UTC con Z; un valor con otro desfase se convierte y uno sin zona se toma como UTC.
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
