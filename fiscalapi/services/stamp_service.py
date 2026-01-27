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
        """Transfer stamps from one person to another.

        Args:
            request: StampTransactionParams containing transfer details.

        Returns:
            ApiResponse containing a boolean indicating success.
        """
        endpoint = "stamps"
        return self.send_request("POST", endpoint, bool, payload=request)

    def withdraw_stamps(self, request: StampTransactionParams) -> ApiResponse[bool]:
        """Withdraw stamps from a person (convenience wrapper for transfer_stamps).

        Args:
            request: StampTransactionParams containing withdrawal details.

        Returns:
            ApiResponse containing a boolean indicating success.
        """
        return self.transfer_stamps(request)
