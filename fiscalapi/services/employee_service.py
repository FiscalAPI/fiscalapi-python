from fiscalapi.models.common_models import ApiResponse
from fiscalapi.models.fiscalapi_models import EmployeeData
from fiscalapi.services.base_service import BaseService


class EmployeeService(BaseService):
    """Servicio para gestionar empleados (sub-recurso de personas)."""

    def get_by_id(self, person_id: str) -> ApiResponse[EmployeeData]:
        endpoint = f"people/{person_id}/employee"
        return self.send_request("GET", endpoint, EmployeeData)

    def create(self, employee: EmployeeData) -> ApiResponse[EmployeeData]:
        endpoint = f"people/{employee.employee_person_id}/employee"
        return self.send_request("POST", endpoint, EmployeeData, payload=employee)

    def update(self, employee: EmployeeData) -> ApiResponse[EmployeeData]:
        endpoint = f"people/{employee.employee_person_id}/employee"
        return self.send_request("PUT", endpoint, EmployeeData, payload=employee)

    def delete(self, person_id: str) -> ApiResponse[bool]:
        endpoint = f"people/{person_id}/employee"
        return self.send_request("DELETE", endpoint, bool)
