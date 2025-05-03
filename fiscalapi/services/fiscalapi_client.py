from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.catalog_service import CatalogService
from fiscalapi.services.invoice_service import InvoiceService
from fiscalapi.services.people_service import PeopleService
from fiscalapi.services.product_service import ProductService
from fiscalapi.services.tax_file_servive import TaxFileService
from fiscalapi.services.api_key_service import ApiKeyService



class FiscalApiClient:
    
    def __init__(self, settings: FiscalApiSettings):
        self.products = ProductService(settings)
        self.people = PeopleService(settings)
        self.tax_files = TaxFileService(settings)
        self.catalogs = CatalogService(settings)
        self.invoices = InvoiceService(settings)
        self.api_keys = ApiKeyService(settings)
        self.settings = settings