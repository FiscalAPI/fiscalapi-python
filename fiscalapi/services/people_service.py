from typing import Optional

from fiscalapi.models.common_models import ApiResponse, FiscalApiSettings, PagedList
from fiscalapi.models.fiscalapi_models import Person
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

    # get paged list of people
    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[Person]]:
        endpoint = f"people?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[Person])
    
    # get person by id
    def get_by_id(self, person_id: str) -> ApiResponse[Person]:
        endpoint = f"people/{person_id}"
        return self.send_request("GET", endpoint, Person)
    
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
    
