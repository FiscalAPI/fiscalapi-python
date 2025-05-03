from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import ApiKey
from fiscalapi.services.base_service import BaseService


class ApiKeyService(BaseService):
    
    # get paged list of api keys
    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[ApiKey]]:
        endpoint = f"apikeys?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[ApiKey])
    
    # get apikey by id
    def get_by_id(self, id: str) -> ApiResponse[ApiKey]:
        endpoint = f"apikeys/{id}"
        return self.send_request("GET", endpoint, ApiKey)
    
    # create apikey
    def create(self, model: ApiKey) -> ApiResponse[ApiKey]:
        endpoint = "apikeys"
        return self.send_request("POST", endpoint, ApiKey, payload=model)
    
    # update apikey
    def update(self, model: ApiKey) -> ApiResponse[ApiKey]:
        endpoint = f"apikeys/{model.id}"
        return self.send_request("PUT", endpoint, ApiKey, payload=model)
    
    # delete apikey by id
    def delete(self, id: str) -> ApiResponse[bool]:
        endpoint = f"apikeys/{id}"
        return self.send_request("DELETE", endpoint, bool)
