from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import (
    CancelInvoiceRequest,
    CancelInvoiceResponse,
    CreatePdfRequest,
    FileResponse,
    Invoice,
    InvoiceStatusRequest,
    InvoiceStatusResponse,
    SendInvoiceRequest,
)
from fiscalapi.services.base_service import BaseService


class InvoiceService(BaseService):
    """Servicio para gestionar facturas CFDI."""

    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[Invoice]]:
        """Obtiene una lista paginada de facturas."""
        endpoint = f"invoices?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[Invoice])

    def get_by_id(self, invoice_id: str, details: bool = False) -> ApiResponse[Invoice]:
        """Obtiene una factura por su ID."""
        endpoint = f"invoices/{invoice_id}"
        return self.send_request("GET", endpoint, Invoice, details=details)

    def create(self, invoice: Invoice) -> ApiResponse[Invoice]:
        """
        Crea una nueva factura CFDI.

        El tipo de factura se determina por el campo type_code del modelo Invoice:
        - 'I': Factura de ingreso
        - 'E': Nota de crédito
        - 'P': Complemento de pago
        - 'N': Nómina
        - 'T': Traslado

        Args:
            invoice: Modelo de factura con los datos requeridos.

        Returns:
            ApiResponse con la factura creada y timbrada.
        """
        endpoint = "invoices"
        return self.send_request("POST", endpoint, Invoice, payload=invoice)

    def cancel(self, cancel_invoice_request: CancelInvoiceRequest) -> ApiResponse[CancelInvoiceResponse]:
        """Cancela una factura."""
        endpoint = "invoices"
        return self.send_request("DELETE", endpoint, CancelInvoiceResponse, payload=cancel_invoice_request)

    def get_pdf(self, create_pdf_request: CreatePdfRequest) -> ApiResponse[FileResponse]:
        """Genera el PDF de una factura."""
        endpoint = "invoices/pdf"
        return self.send_request("POST", endpoint, FileResponse, payload=create_pdf_request)

    def get_xml(self, invoice_id: str) -> ApiResponse[FileResponse]:
        """Obtiene el XML de una factura por su ID."""
        endpoint = f"invoices/{invoice_id}/xml"
        return self.send_request("GET", endpoint, FileResponse)

    def send(self, send_invoice_request: SendInvoiceRequest) -> ApiResponse[bool]:
        """Envía una factura por correo electrónico."""
        endpoint = "invoices/send"
        return self.send_request("POST", endpoint, bool, payload=send_invoice_request)

    def get_status(self, request: InvoiceStatusRequest) -> ApiResponse[InvoiceStatusResponse]:
        """Consulta el estado de una factura en el SAT."""
        endpoint = "invoices/status"
        return self.send_request("POST", endpoint, InvoiceStatusResponse, payload=request)
