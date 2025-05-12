from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import CancelInvoiceRequest, CancelInvoiceResponse, CreatePdfRequest, FileResponse, Invoice, InvoiceStatusRequest, InvoiceStatusResponse, SendInvoiceRequest
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
        
    # create invoice
    def create(self, invoice: Invoice) -> ApiResponse[Invoice]:
        if invoice is None:
            raise ValueError("request_model cannot be null")

        endpoint = self._get_endpoint_by_type(invoice.type_code)
        return self.send_request("POST", endpoint, Invoice, payload=invoice)
    
    
    # cancel invoice
    def cancel(self, cancel_invoice_request: CancelInvoiceRequest) -> ApiResponse[CancelInvoiceResponse]:
        if cancel_invoice_request is None:
            raise ValueError("request_model cannot be null")
        
        endpoint = "invoices"
        return self.send_request("DELETE", endpoint, CancelInvoiceResponse, payload=cancel_invoice_request)
    
    # create invoice's pdf
    def get_pdf(self, create_pdf_request:CreatePdfRequest) -> ApiResponse[FileResponse]:
        if create_pdf_request is None:
            raise ValueError("request_model cannot be null")
        
        endpoint = "invoices/pdf"
        return self.send_request("POST", endpoint, FileResponse, payload=create_pdf_request)
    
    # get invoice's xml by id /api/v4/invoices/<id>/xml
    def get_xml(self, invoice_id: int) -> ApiResponse[FileResponse]:
        if invoice_id is None:
            raise ValueError("invoice_id cannot be null")
        
        endpoint = f"invoices/{invoice_id}/xml"
        return self.send_request("GET", endpoint, FileResponse)
  
    
    # send invoice by email
 
    def send(self, send_invoice_request : SendInvoiceRequest):
        if not send_invoice_request:
            raise ValueError("Invalid request")
        
        endpoint = "invoices/send"
        
        return self.send_request("POST", endpoint, bool, payload=send_invoice_request)
    
    # consultar estado de facturas
    def get_status(self, request: InvoiceStatusRequest) -> ApiResponse[InvoiceStatusResponse]:
        """
        Obtiene el estado de una factura.
        
        Args:
            request (InvoiceStatusRequest): Solicitud para consultar estado
        
        Returns:
            ApiResponse[InvoiceStatusResponse]: Respuesta con el estado de la factura
        """
        if request is None:
            raise ValueError("request cannot be null")
        
        endpoint = "invoices/status"
        return self.send_request("POST", endpoint, InvoiceStatusResponse, payload=request)
    
    