from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import DownloadRule, DownloadRequest
from fiscalapi.services.base_service import BaseService


class DownloadRuleService(BaseService):
    """Servicio para gestionar reglas de descarga de CFDI."""
    
     # get paged list of download rules
    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[DownloadRule]]:
        endpoint = f"download-rules?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[DownloadRule])
    
    # get download rule by id
    def get_by_id(self, download_rule_id: str) -> ApiResponse[DownloadRule]:
        endpoint = f"download-rules/{download_rule_id}"
        return self.send_request("GET", endpoint, DownloadRule)
    
    # create download rule
    def create(self, download_rule: DownloadRule) -> ApiResponse[DownloadRule]:
        endpoint = "download-rules"
        return self.send_request("POST", endpoint, DownloadRule, payload=download_rule)
    
    # create test download rule
    def create_test_rule(self) -> ApiResponse[DownloadRule]:
        endpoint = "download-rules/test"
        return self.send_request("POST", endpoint, DownloadRule)
    
    # update download rule
    def update(self, download_rule: DownloadRule) -> ApiResponse[DownloadRule]:
        endpoint = f"download-rules/{download_rule.id}"
        return self.send_request("PUT", endpoint, DownloadRule, payload=download_rule)
    
    # delete download rule
    def delete(self, download_rule_id: str) -> ApiResponse[bool]:
        endpoint = f"download-rules/{download_rule_id}"
        return self.send_request("DELETE", endpoint, bool)