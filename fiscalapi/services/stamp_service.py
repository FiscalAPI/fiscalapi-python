"""Servicio para gestionar transacciones de timbres (stamps)."""

from fiscalapi.models import (
    ApiResponse,
    FiscalApiSettings,
    PagedList,
    StampTransaction,
    StampTransactionParams,
)
from fiscalapi.services.base_service import BaseService


class StampService(BaseService):
    """Service for managing stamp transactions (timbres)."""

    def __init__(self, settings: FiscalApiSettings):
        super().__init__(settings)

    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[StampTransaction]]:
        """List stamp transactions with pagination.

        Args:
            page_number: Page number (1-based).
            page_size: Number of items per page.

        Returns:
            ApiResponse containing a PagedList of StampTransaction objects.
        """
        endpoint = f"stamps?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[StampTransaction])

    def get_by_id(self, transaction_id: str) -> ApiResponse[StampTransaction]:
        """Get a stamp transaction by ID.

        Args:
            transaction_id: The unique identifier of the stamp transaction.

        Returns:
            ApiResponse containing the StampTransaction object.
        """
        endpoint = f"stamps/{transaction_id}"
        return self.send_request("GET", endpoint, StampTransaction)

    def transfer_stamps(self, request: StampTransactionParams) -> ApiResponse[bool]:
        """Transfer stamps or validation credits from one person to another.

        Use ``request.credit_type`` to pick which balance moves: ``CreditType.STAMP`` (default) moves
        stamps, ``CreditType.VALIDATION`` moves SAT validation credits. The two balances never mix.

        Args:
            request: StampTransactionParams containing transfer details.

        Returns:
            ApiResponse containing a boolean indicating success.
        """
        endpoint = "stamps"
        return self.send_request("POST", endpoint, bool, payload=request)

    def withdraw_stamps(self, request: StampTransactionParams) -> ApiResponse[bool]:
        """Withdraw stamps or validation credits from a person.

        A withdrawal is a transfer with the origin and destination swapped: the API exposes a single
        transfer endpoint, so this is an alias of :meth:`transfer_stamps` kept for readability at the
        call site. Build ``request`` with the person you are withdrawing from as ``from_person_id``.

        Args:
            request: StampTransactionParams containing withdrawal details.

        Returns:
            ApiResponse containing a boolean indicating success.
        """
        return self.transfer_stamps(request)
