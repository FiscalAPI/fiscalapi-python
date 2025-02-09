from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import Invoice
from fiscalapi.services.base_service import BaseService


class InvoiceService(BaseService):
    
    # get paged list of invoices
    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[Invoice]]:
        endpoint = f"invoices?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[Invoice])
    
    # get invoice by id
    def get_by_id(self, invoice_id: int, details: bool = False) -> ApiResponse[Invoice]:
        endpoint = f"invoices/{invoice_id}"
        return self.send_request("GET", endpoint, Invoice, details=details)
    