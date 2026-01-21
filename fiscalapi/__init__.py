"""
FiscalAPI Python SDK

SDK oficial para integración con FiscalAPI, la plataforma de facturación
electrónica (CFDI 4.0) y servicios fiscales de México.

Ejemplo de uso:
    >>> from fiscalapi import FiscalApiClient, FiscalApiSettings
    >>> settings = FiscalApiSettings(api_url="...", api_key="...", tenant="...")
    >>> client = FiscalApiClient(settings=settings)
    >>> response = client.invoices.get_list(page_number=1, page_size=10)
"""

# Modelos base
from .models.common_models import (
    ApiResponse,
    BaseDto,
    CatalogDto,
    FiscalApiSettings,
    PagedList,
    ValidationFailure,
)

# Modelos de dominio
from .models.fiscalapi_models import (
    ApiKey,
    CancelInvoiceRequest,
    CancelInvoiceResponse,
    CreatePdfRequest,
    DownloadRequest,
    DownloadRule,
    EmployeeData,
    EmployerData,
    FileResponse,
    GlobalInformation,
    Invoice,
    InvoiceIssuer,
    InvoiceItem,
    InvoicePayment,
    InvoiceRecipient,
    InvoiceResponse,
    InvoiceStatusRequest,
    InvoiceStatusResponse,
    ItemTax,
    MetadataItem,
    PaidInvoice,
    PaidInvoiceTax,
    Person,
    Product,
    ProductTax,
    RelatedInvoice,
    SendInvoiceRequest,
    TaxCredential,
    TaxFile,
    Xml,
    XmlComplement,
    XmlGlobalInformation,
    XmlIssuer,
    XmlItem,
    XmlItemCustomsInformation,
    XmlItemPropertyAccount,
    XmlItemTax,
    XmlRecipient,
    XmlRelated,
    XmlTax,
)

# Servicios
from .services.base_service import BaseService
from .services.api_key_service import ApiKeyService
from .services.catalog_service import CatalogService
from .services.download_catalog_service import DownloadCatalogService
from .services.download_request_service import DownloadRequestService
from .services.download_rule_service import DownloadRuleService
from .services.employee_service import EmployeeService
from .services.employer_service import EmployerService
from .services.invoice_service import InvoiceService
from .services.people_service import PeopleService
from .services.product_service import ProductService
from .services.tax_file_service import TaxFileService

# Cliente principal
from .services.fiscalapi_client import FiscalApiClient

__all__ = [
    # Modelos base
    "ApiResponse",
    "BaseDto",
    "CatalogDto",
    "FiscalApiSettings",
    "PagedList",
    "ValidationFailure",
    # Modelos de dominio
    "ApiKey",
    "CancelInvoiceRequest",
    "CancelInvoiceResponse",
    "CreatePdfRequest",
    "DownloadRequest",
    "DownloadRule",
    "EmployeeData",
    "EmployerData",
    "FileResponse",
    "GlobalInformation",
    "Invoice",
    "InvoiceIssuer",
    "InvoiceItem",
    "InvoicePayment",
    "InvoiceRecipient",
    "InvoiceResponse",
    "InvoiceStatusRequest",
    "InvoiceStatusResponse",
    "ItemTax",
    "MetadataItem",
    "PaidInvoice",
    "PaidInvoiceTax",
    "Person",
    "Product",
    "ProductTax",
    "RelatedInvoice",
    "SendInvoiceRequest",
    "TaxCredential",
    "TaxFile",
    "Xml",
    "XmlComplement",
    "XmlGlobalInformation",
    "XmlIssuer",
    "XmlItem",
    "XmlItemCustomsInformation",
    "XmlItemPropertyAccount",
    "XmlItemTax",
    "XmlRecipient",
    "XmlRelated",
    "XmlTax",
    # Servicios
    "BaseService",
    "ApiKeyService",
    "CatalogService",
    "DownloadCatalogService",
    "DownloadRequestService",
    "DownloadRuleService",
    "EmployeeService",
    "EmployerService",
    "InvoiceService",
    "PeopleService",
    "ProductService",
    "TaxFileService",
    # Cliente principal
    "FiscalApiClient",
]
