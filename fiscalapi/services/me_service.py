"""Servicio de la persona de la credencial con que se llama al API (GET /api/v4/me)."""

from fiscalapi.models.common_models import ApiResponse
from fiscalapi.models.me_models import MeInfo
from fiscalapi.services.base_service import BaseService


class MeService(BaseService):
    """Service for the person of the API key (endpoint /api/v4/me)."""

    def get(self) -> ApiResponse[MeInfo]:
        """Get the person of the API key: id, name, RFC and email, tenant, the environment that answers, whether it is
        the owner, what it can do and its balances. GET /api/v4/me

        Useful to validate a credential: with an API key or a tenant that are not valid the API answers 401.

        Returns:
            ApiResponse containing the MeInfo.
        """
        return self.send_request("GET", "me", MeInfo)
