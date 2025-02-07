from fiscalapi.models.common_models import ApiResponse, CatalogDto, PagedList
from fiscalapi.services.base_service import BaseService


class CatalogService(BaseService):
    
    # get list of catalogs available in fiscalapi
    def get_list(self) -> ApiResponse[list[str]]:
        endpoint = "catalogs"
        return self.send_request("GET", endpoint, list[str])

    # get record by catalog name and its id
    def get_record_by_id(self, catalog_name: str, id: str) -> ApiResponse[CatalogDto]:
        endpoint = f"catalogs/{catalog_name}/key/{id}"
        return self.send_request("GET", endpoint, CatalogDto)

    # Search whithin a catalog by catalog name and search text
    def search_catalog(self, catalog_name: str, search_text: str, page_number: int = 1, page_size: int = 50) -> ApiResponse[PagedList[CatalogDto]]:
        endpoint = f"catalogs/{catalog_name}/{search_text}?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[CatalogDto])