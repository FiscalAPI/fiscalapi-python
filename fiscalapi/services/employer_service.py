from fiscalapi.models.common_models import ApiResponse
from fiscalapi.models.fiscalapi_models import EmployerData
from fiscalapi.services.base_service import BaseService


class EmployerService(BaseService):
    """Servicio para gestionar empleadores (sub-recurso de personas)."""

    def get_by_id(self, person_id: str) -> ApiResponse[EmployerData]:
        endpoint = f"people/{person_id}/employer"
        return self.send_request("GET", endpoint, EmployerData)

    def create(self, employer: EmployerData) -> ApiResponse[EmployerData]:
        endpoint = f"people/{employer.person_id}/employer"
        return self.send_request("POST", endpoint, EmployerData, payload=employer)

    def update(self, employer: EmployerData) -> ApiResponse[EmployerData]:
        endpoint = f"people/{employer.person_id}/employer"
        return self.send_request("PUT", endpoint, EmployerData, payload=employer)

    def delete(self, person_id: str) -> ApiResponse[bool]:
        endpoint = f"people/{person_id}/employer"
        return self.send_request("DELETE", endpoint, bool)
