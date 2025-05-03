from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import Person, Product
from fiscalapi.services.base_service import BaseService


class PeopleService(BaseService):
    
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
    
