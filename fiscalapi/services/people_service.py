from typing import Optional

from fiscalapi.models.common_models import ApiResponse, FiscalApiSettings, PagedList
from fiscalapi.models.fiscalapi_models import Person, PersonListFilters, TaxFile
from fiscalapi.services.base_service import BaseService
from fiscalapi.services.employee_service import EmployeeService
from fiscalapi.services.employer_service import EmployerService


class PeopleService(BaseService):

    def __init__(self, settings: FiscalApiSettings):
        super().__init__(settings)
        self._employee: Optional[EmployeeService] = None
        self._employer: Optional[EmployerService] = None

    @property
    def employee(self) -> EmployeeService:
        if self._employee is None:
            self._employee = EmployeeService(self.settings)
        return self._employee

    @property
    def employer(self) -> EmployerService:
        if self._employer is None:
            self._employer = EmployerService(self.settings)
        return self._employer

    def get_list(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        *,
        filters: Optional[PersonListFilters] = None,
    ) -> ApiResponse[PagedList[Person]]:
        """Obtiene una lista paginada de personas, con la página o con filtros. GET /api/v4/people

        Los filtros en None no se envían; sin página ni filtros, la lista es la de siempre (primera página).

        Args:
            page_number: Página, desde 1.
            page_size: Tamaño de página (1 a 50).
            filters: Búsqueda, tipo de persona y página; en lugar de page_number y page_size.

        Returns:
            ApiResponse con la página de personas.

        Raises:
            ValueError: Si se pasan filters junto con page_number o page_size.
        """
        endpoint = self._list_endpoint("people", page_number, page_size, filters)
        return self.send_request("GET", endpoint, PagedList[Person])
    
    # get person by id
    def get_by_id(self, person_id: str) -> ApiResponse[Person]:
        endpoint = f"people/{person_id}"
        return self.send_request("GET", endpoint, Person)

    def get_tax_files(self, person_id: str) -> ApiResponse[list[TaxFile]]:
        """Lista los certificados (CSD y FIEL) de una persona, solo metadatos, sin el archivo ni la contraseña."""
        endpoint = f"people/{person_id}/tax-files"
        return self.send_request("GET", endpoint, list[TaxFile])

    # create person
    def create(self, person: Person) -> ApiResponse[Person]:
        endpoint = "people"
        return self.send_request("POST", endpoint, Person, payload=person)
    
    # update person
    def update(self, person: Person) -> ApiResponse[Person]:
        endpoint = f"people/{person.id}"
        return self.send_request("PUT", endpoint, Person, payload=person)
    
    # delete person
    def delete(self, person_id: str) -> ApiResponse[bool]:
        endpoint = f"people/{person_id}"
        return self.send_request("DELETE", endpoint, bool)
    
