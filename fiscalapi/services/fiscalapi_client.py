from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.services.catalog_service import CatalogService
from fiscalapi.services.invoice_service import InvoiceService
from fiscalapi.services.people_service import PeopleService
from fiscalapi.services.product_service import ProductService
from fiscalapi.services.tax_file_service import TaxFileService
from fiscalapi.services.api_key_service import ApiKeyService
from fiscalapi.services.download_catalog_service import DownloadCatalogService
from fiscalapi.services.download_rule_service import DownloadRuleService
from fiscalapi.services.download_request_service import DownloadRequestService



class FiscalApiClient:
    
    def __init__(self, settings: FiscalApiSettings):
        self.products = ProductService(settings)
        self.people = PeopleService(settings)
        self.tax_files = TaxFileService(settings)
        self.catalogs = CatalogService(settings)
        self.invoices = InvoiceService(settings)
        self.api_keys = ApiKeyService(settings)
        self.download_catalogs = DownloadCatalogService(settings)
        self.download_rules = DownloadRuleService(settings)
        self.download_requests = DownloadRequestService(settings)
        self.settings = settings