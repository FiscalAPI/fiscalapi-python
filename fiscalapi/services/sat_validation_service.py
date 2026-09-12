"""Servicio para ejecutar y consultar validaciones SAT sobre un CFDI."""

from fiscalapi.models.common_models import ApiResponse
from fiscalapi.models.sat_validation_models import (
    SatValidationRequest,
    SatValidationResult,
    SatValidationType,
    SatValidationTypeStatus,
)
from fiscalapi.services.base_service import BaseService


class SatValidationService(BaseService):
    """Service for running SAT validations against a CFDI."""

    def get_types(self) -> ApiResponse[list[SatValidationType]]:
        """List the available SAT validation types.

        Returns:
            ApiResponse containing the active validation types, in catalog order.
        """
        endpoint = "sat-validations"
        return self.send_request("GET", endpoint, list[SatValidationType])

    def get_type_by_id(self, validation_type_id: str) -> ApiResponse[SatValidationType]:
        """Get a SAT validation type by its id.

        Args:
            validation_type_id: Validation type id, e.g. ``sat.cfdi.status``.

        Returns:
            ApiResponse containing the SatValidationType object.

        Raises:
            ValueError: If validation_type_id is empty.
        """
        self._ensure_validation_type_id(validation_type_id)
        # El id se interpola tal cual: lleva puntos y la API lo espera sin codificar ni recortar.
        endpoint = f"sat-validations/{validation_type_id}"
        return self.send_request("GET", endpoint, SatValidationType)

    def get_statuses(self, validation_type_id: str) -> ApiResponse[list[SatValidationTypeStatus]]:
        """List the statuses a SAT validation type can take when executed.

        Read-only: it neither runs the validator nor consumes validation credits.

        Args:
            validation_type_id: Validation type id, e.g. ``sat.cfdi.status``.

        Returns:
            ApiResponse containing the statuses of the validation type.

        Raises:
            ValueError: If validation_type_id is empty.
        """
        self._ensure_validation_type_id(validation_type_id)
        # El id se interpola tal cual: lleva puntos y la API lo espera sin codificar ni recortar.
        endpoint = f"sat-validations/{validation_type_id}/statuses"
        return self.send_request("GET", endpoint, list[SatValidationTypeStatus])

    def validate(self, request: SatValidationRequest) -> ApiResponse[list[SatValidationResult]]:
        """Run SAT validations against a CFDI or a TIN.

        Send ``xml`` or ``tin``, never both and never neither: with ``xml`` any validation type can be
        requested; with ``tin`` only the blacklists (``sat.blacklist.69b``, ``sat.blacklist.69bbis``).

        Each requested type consumes one validation credit. The charge is all or nothing and happens
        before running: if the balance does not cover every requested type, none of them run and the API
        responds 403.

        Args:
            request: SatValidationRequest with the CFDI or TIN and the validation types to run.

        Returns:
            ApiResponse containing one SatValidationResult per executed type, in catalog order.

        Raises:
            ValueError: If request is None.
        """
        if request is None:
            raise ValueError("Se requiere la solicitud de validación.")

        endpoint = "sat-validations"
        return self.send_request("POST", endpoint, list[SatValidationResult], payload=request)

    @staticmethod
    def _ensure_validation_type_id(validation_type_id: str) -> None:
        """Guard against an empty id, which would otherwise hit the list endpoint."""
        if not validation_type_id or not validation_type_id.strip():
            raise ValueError("Se requiere el id del tipo de validación (por ejemplo sat.cfdi.status).")
