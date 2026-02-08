from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import TaxFile
from fiscalapi.services.base_service import BaseService


class TaxFileService(BaseService):

    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[TaxFile]]:
        endpoint = f"tax-files?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[TaxFile])

    def get_by_id(self, tax_file_id: str) -> ApiResponse[TaxFile]:
        endpoint = f"tax-files/{tax_file_id}"
        return self.send_request("GET", endpoint, TaxFile)

    def create(self, tax_file: TaxFile) -> ApiResponse[TaxFile]:
        endpoint = "tax-files"
        return self.send_request("POST", endpoint, TaxFile, payload=tax_file)

    def delete(self, tax_file_id: str) -> ApiResponse[bool]:
        endpoint = f"tax-files/{tax_file_id}"
        return self.send_request("DELETE", endpoint, bool)

    def get_default_values(self, person_id: str) -> ApiResponse[list[TaxFile]]:
        """Obtiene el último par de certificados válidos y vigentes de una persona."""
        endpoint = f"tax-files/{person_id}/default-values"
        return self.send_request("GET", endpoint, list[TaxFile])

    def get_default_references(self, person_id: str) -> ApiResponse[list[TaxFile]]:
        """Obtiene el último par de IDs de certificados válidos y vigentes de una persona."""
        endpoint = f"tax-files/{person_id}/default-references"
        return self.send_request("GET", endpoint, list[TaxFile])
