from typing import Optional

from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import (
    CancelInvoiceRequest,
    CancelInvoiceResponse,
    CreatePdfRequest,
    FileResponse,
    Invoice,
    InvoiceListFilters,
    InvoiceStatusRequest,
    InvoiceStatusResponse,
    SendInvoiceRequest,
)
from fiscalapi.services.base_service import IDEMPOTENCY_KEY_HEADER, BaseService


class InvoiceService(BaseService):
    """Servicio para gestionar facturas CFDI."""

    def get_list(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        *,
        filters: Optional[InvoiceListFilters] = None,
    ) -> ApiResponse[PagedList[Invoice]]:
        """Obtiene una lista paginada de facturas, con la página o con filtros. GET /api/v4/invoices

        Los filtros en None no se envían; sin página ni filtros, la lista es la de siempre (primera página, de la más
        antigua a la más reciente).

        Args:
            page_number: Página, desde 1.
            page_size: Tamaño de página (1 a 50).
            filters: Fechas, RFC, tipo, estatus, serie, folio, UUID, orden y página; en lugar de page_number y page_size.

        Returns:
            ApiResponse con la página de facturas.

        Raises:
            ValueError: Si se pasan filters junto con page_number o page_size.
        """
        endpoint = self._list_endpoint("invoices", page_number, page_size, filters)
        return self.send_request("GET", endpoint, PagedList[Invoice])

    def get_by_id(self, invoice_id: str, details: bool = False) -> ApiResponse[Invoice]:
        """Obtiene una factura por su ID."""
        endpoint = f"invoices/{invoice_id}"
        return self.send_request("GET", endpoint, Invoice, details=details)

    def create(self, invoice: Invoice, idempotency_key: Optional[str] = None) -> ApiResponse[Invoice]:
        """
        Crea una nueva factura CFDI.

        El tipo de factura se determina por el campo type_code del modelo Invoice:
        - 'I': Factura de ingreso
        - 'E': Nota de crédito
        - 'P': Complemento de pago
        - 'N': Nómina
        - 'T': Traslado

        Con idempotency_key (hasta 64 caracteres ASCII visibles, sin espacios) se envía el header Idempotency-Key:
        repetir la llave de idempotencia con la misma petición en 24 h devuelve la respuesta original; con otra petición
        responde 422, y mientras la original sigue en proceso, 409. Sin llave de idempotencia el header no se envía.

        Args:
            invoice: Modelo de factura con los datos requeridos.
            idempotency_key: Valor del header Idempotency-Key, o None para no enviarlo.

        Returns:
            ApiResponse con la factura creada y timbrada.
        """
        endpoint = "invoices"
        headers = {} if idempotency_key is None else {IDEMPOTENCY_KEY_HEADER: idempotency_key}
        return self.send_request("POST", endpoint, Invoice, payload=invoice, headers=headers)

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
