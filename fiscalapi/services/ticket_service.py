"""Servicio de tickets de Auto CFDI: ingesta, consulta con filtros, código para reimprimir y cancelación."""

from typing import Optional
from urllib.parse import urlencode

from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.ticket_models import Ticket, TicketCodeResult, TicketIngestionResult, TicketListFilters
from fiscalapi.services.base_service import BaseService

IDEMPOTENCY_KEY_HEADER = "Idempotency-Key"


class TicketService(BaseService):
    """Service for Auto CFDI tickets (endpoints /api/v4/tickets)."""

    def create(self, ticket: Ticket, idempotency_key: Optional[str] = None) -> ApiResponse[TicketIngestionResult]:
        """Ingest a ticket and charge 1 ticket credit. POST /api/v4/tickets

        With ``idempotency_key`` (up to 64 characters) the ``Idempotency-Key`` header is sent: repeating the key with
        the same body answers 200 with the original ticket without charging again; with another body, 422. Without it
        the header is not sent. An active folio and series of the issuer answers 409.

        Args:
            ticket: Ticket to ingest.
            idempotency_key: Value of the Idempotency-Key header, or None to not send it.

        Returns:
            ApiResponse containing the TicketIngestionResult (code and QR URL to print).

        Raises:
            ValueError: If ticket is None.
        """
        if ticket is None:
            raise ValueError("Se requiere el ticket.")

        headers = {} if idempotency_key is None else {IDEMPOTENCY_KEY_HEADER: idempotency_key}
        return self.send_request("POST", "tickets", TicketIngestionResult, payload=ticket, headers=headers)

    def get_list(self, filters: Optional[TicketListFilters] = None) -> ApiResponse[PagedList[Ticket]]:
        """List the tenant's tickets with the given filters (none: all of them, first page). GET /api/v4/tickets

        Args:
            filters: Status (one or more; the ``status`` key repeats), person, payment date range and page.

        Returns:
            ApiResponse containing a PagedList of Ticket, ordered by payment date.
        """
        params = filters.to_query_params() if filters is not None else []
        endpoint = f"tickets?{urlencode(params)}" if params else "tickets"
        return self.send_request("GET", endpoint, PagedList[Ticket])

    def get_by_id(self, ticket_id: str, details: bool = False) -> ApiResponse[Ticket]:
        """Get a ticket; with ``details`` it also brings its items and history. GET /api/v4/tickets/{id}

        Args:
            ticket_id: Ticket id.
            details: Include items and events.

        Returns:
            ApiResponse containing the Ticket.

        Raises:
            ValueError: If ticket_id is empty.
        """
        self._ensure_ticket_id(ticket_id)
        return self.send_request("GET", f"tickets/{ticket_id}", Ticket, details=details)

    def get_code(self, ticket_id: str) -> ApiResponse[TicketCodeResult]:
        """Get the ticket code and its QR URL, to reprint it. GET /api/v4/tickets/{id}/code

        Args:
            ticket_id: Ticket id.

        Returns:
            ApiResponse containing the TicketCodeResult.

        Raises:
            ValueError: If ticket_id is empty.
        """
        self._ensure_ticket_id(ticket_id)
        return self.send_request("GET", f"tickets/{ticket_id}/code", TicketCodeResult)

    def cancel(self, ticket_id: str) -> ApiResponse[bool]:
        """Cancel a pending ticket (409 in any other status); the ticket credit is not refunded. DELETE /api/v4/tickets/{id}

        Args:
            ticket_id: Ticket id.

        Returns:
            ApiResponse containing True if the ticket was cancelled.

        Raises:
            ValueError: If ticket_id is empty.
        """
        self._ensure_ticket_id(ticket_id)
        return self.send_request("DELETE", f"tickets/{ticket_id}", bool)

    @staticmethod
    def _ensure_ticket_id(ticket_id: str) -> None:
        """Guard against an empty id, which would otherwise hit the list (GET) or the collection (DELETE)."""
        if not ticket_id or not ticket_id.strip():
            raise ValueError("Se requiere el id del ticket.")
