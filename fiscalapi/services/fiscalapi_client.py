from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.products_service import ProductService


class FiscalApiClient:
    def __init__(self, settings: FiscalApiSettings):
        self.products = ProductService(settings)
        #self.invoice_service = InvoiceService(settings)
        # Otros servicios concretos pueden ser inicializados aquí