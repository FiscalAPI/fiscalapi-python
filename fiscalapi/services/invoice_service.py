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
    
    # create invoice
    def create(self, invoice: Invoice) -> ApiResponse[Invoice]:
        if invoice is None:
            raise ValueError("request_model cannot be null")

        endpoint = self._get_endpoint_by_type(invoice.type_code)
        return self.send_request("POST", endpoint, Invoice, payload=invoice)
    
    
     # helper method to determine the endpoint based on invoice type
    def _get_endpoint_by_type(self, type_code: str) -> str:
        if type_code == "I":
            return "invoices/income"
        elif type_code == "E":
            return "invoices/credit-note"
        elif type_code == "P":
            return "invoices/payment"
        else:
            raise ValueError(f"Unsupported invoice type: {type_code}")
    