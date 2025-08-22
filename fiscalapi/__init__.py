# fiscalapi/__init__.py

# Re-exportar modelos de common_models
from .models.common_models import (
    ApiResponse,
    PagedList,
    ValidationFailure,
    BaseDto,
    CatalogDto,
    FiscalApiSettings,
)

# Re-exportar modelos de fiscalapi_models
from .models.fiscalapi_models import (
    ProductTax,
    Product,
    Person,
    TaxFile,
    TaxCredential,
    InvoiceIssuer,
    InvoiceRecipient,
    ItemTax,
    InvoiceItem,
    GlobalInformation,
    RelatedInvoice,
    PaidInvoiceTax,
    PaidInvoice,
    InvoicePayment,
    InvoiceResponse,
    Invoice,
    CancelInvoiceRequest,
    CancelInvoiceResponse,
    CreatePdfRequest,
    FileResponse,
    SendInvoiceRequest,
    InvoiceStatusRequest,
    InvoiceStatusResponse,
    ApiKey,
    DownloadRule,
    DownloadRequest,
    MetadataItem,
    XmlGlobalInformation,
    XmlIssuer,
    XmlRecipient,
    XmlRelated,
    XmlTax,
    XmlItemCustomsInformation,
    XmlItemPropertyAccount,
    XmlItemTax,
    XmlItem,
    XmlComplement,
    Xml,
)

# Re-exportar servicios
from .services.catalog_service import CatalogService
from .services.invoice_service import InvoiceService
from .services.people_service import PeopleService
from .services.product_service import ProductService
from .services.tax_file_servive import TaxFileService 
from .services.api_key_service import ApiKeyService
from .services.download_catalog_service import DownloadCatalogService
from .services.download_rule_service import DownloadRuleService
from .services.download_request_service import DownloadRequestService

# Re-exportar la clase FiscalApiClient
# (asumiendo que la definición está en fiscalapi/services/fiscalapi_client.py)
from .services.fiscalapi_client import FiscalApiClient

__all__ = [
    # Modelos
    "ApiResponse",
    "PagedList",
    "ValidationFailure",
    "BaseDto",
    "CatalogDto",
    "FiscalApiSettings",
    "ProductTax",
    "Product",
    "Person",
    "TaxFile",
    "TaxCredential",
    "InvoiceIssuer",
    "InvoiceRecipient",
    "ItemTax",
    "InvoiceItem",
    "GlobalInformation",
    "RelatedInvoice",
    "PaidInvoiceTax",
    "PaidInvoice",
    "InvoicePayment",
    "InvoiceResponse",
    "Invoice",
    "CancelInvoiceRequest",
    "CancelInvoiceResponse",
    "CreatePdfRequest",
    "FileResponse",
    "SendInvoiceRequest",
    "InvoiceStatusRequest",
    "InvoiceStatusResponse",
    "ApiKey",
    "DownloadRule",
    "DownloadRequest",
    "MetadataItem",
    "XmlGlobalInformation",
    "XmlIssuer",
    "XmlRecipient",
    "XmlRelated",
    "XmlTax",
    "XmlItemCustomsInformation",
    "XmlItemPropertyAccount",
    "XmlItemTax",
    "XmlItem",
    "XmlComplement",
    "Xml",
    
    # Servicios
    "CatalogService",
    "InvoiceService",
    "PeopleService",
    "ProductService",
    "TaxFileService",
    "ApiKeyService",
    "DownloadCatalogService",
    "DownloadRuleService",
    "DownloadRequestService",
    
    # Cliente principal
    "FiscalApiClient",
]
