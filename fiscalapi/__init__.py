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

# Modelos de Carta Porte
from .models.carta_porte_models import (
    UbicacionDomicilio,
    TipoFiguraDomicilio,
    RegimenAduanero,
    Ubicacion,
    DocumentoAduanero,
    GuiaIdentificacion,
    CantidadTransporta,
    DetalleMercancia,
    Mercancia,
    Remolque,
    Autotransporte,
    RemolqueCCP,
    ContenedorMaritimo,
    TransporteMaritimo,
    TransporteAereo,
    DerechoDePaso,
    CarroContenedor,
    Carro,
    TransporteFerroviario,
    ParteTransporte,
    TipoFigura,
    CartaPorteComplement,
)

# Modelos de Comercio Exterior
from .models.comercio_exterior_models import (
    ComercioExteriorEmisorDomicilio,
    ComercioExteriorReceptorDomicilio,
    ComercioExteriorDestinatarioDomicilio,
    ComercioExteriorEmisor,
    ComercioExteriorPropietario,
    ComercioExteriorReceptor,
    ComercioExteriorDestinatario,
    ComercioExteriorMercanciaDescripcionEspecifica,
    ComercioExteriorMercancia,
    ComercioExteriorComplement,
)

# Modelos de firma de manifiestos
from .models.manifest_models import (
    SignManifestRequest,
    SignManifestResponse,
)
from .models.sat_validation_models import (
    SatValidationTypeIds,
    SatValidationStatusIds,
    SatValidationRequest,
    SatValidationType,
    SatValidationTypeStatus,
    SatValidationStatus,
    SatValidationResult,
)
# Modelos de tickets (Auto CFDI)
from .models.ticket_models import (
    TicketStatus,
    TicketEventType,
    TicketActorType,
    TicketIssuer,
    TicketItemTax,
    TicketItem,
    TicketEvent,
    Ticket,
    TicketIngestionResult,
    TicketCodeResult,
    TicketListFilters,
)

# Modelos de webhooks
from .models.webhook_models import (
    WebhookEventTypes,
    WebhookRelatedObject,
    WebhookEventData,
    WebhookEvent,
)

# Modelos de dominio
from .models.fiscalapi_models import (
    # Product models
    ProductTax,
    Product,
    # Person models
    CreditBalance,
    Person,
    EmployeeData,
    EmployerData,
    TaxFile,
    # Invoice issuer/recipient models
    InvoiceIssuerEmployerData,
    InvoiceRecipientEmployeeData,
    TaxCredential,
    InvoiceIssuer,
    InvoiceRecipient,
    # Invoice item models
    ItemTax,
    ItemOnBehalfOf,
    ItemCustomsInfo,
    ItemPropertyInfo,
    ItemPart,
    InvoiceItem,
    # Invoice related models
    GlobalInformation,
    RelatedInvoice,
    PaidInvoiceTax,
    PaidInvoice,
    InvoicePayment,
    # Complement models
    LocalTax,
    LocalTaxesComplement,
    PaymentComplement,
    PayrollStockOptions,
    PayrollOvertime,
    PayrollEarning,
    PayrollBalanceCompensation,
    PayrollOtherPayment,
    PayrollRetirement,
    PayrollSeverance,
    PayrollEarningsComplement,
    PayrollDeduction,
    PayrollDisability,
    PayrollComplement,
    InvoiceComplement,
    # Invoice models
    InvoiceResponse,
    Invoice,
    CancelInvoiceRequest,
    CancelInvoiceResponse,
    CreatePdfRequest,
    FileResponse,
    SendInvoiceRequest,
    InvoiceStatusRequest,
    InvoiceStatusResponse,
    # API Key models
    ApiKey,
    # Download models
    DownloadRule,
    DownloadRequest,
    MetadataItem,
    # XML models
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
    # Stamp models
    CreditType,
    StampTransactionType,
    StampTransactionStatus,
    UserLookupDto,
    StampTransaction,
    StampTransactionParams,
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
from .services.sat_validation_service import SatValidationService
from .services.stamp_service import StampService
from .services.manifest_service import ManifestService
from .services.ticket_service import TicketService

# Cliente principal
from .services.fiscalapi_client import FiscalApiClient

# Verificación de webhooks (fiscalapi.webhooks.verify)
from . import webhooks
from .webhooks import WebhookVerificationException

__all__ = [
    # Modelos base
    "ApiResponse",
    "BaseDto",
    "CatalogDto",
    "FiscalApiSettings",
    "PagedList",
    "ValidationFailure",
    # Product models
    "ProductTax",
    "Product",
    # Person models
    "CreditBalance",
    "Person",
    "EmployeeData",
    "EmployerData",
    "TaxFile",
    # Invoice issuer/recipient models
    "InvoiceIssuerEmployerData",
    "InvoiceRecipientEmployeeData",
    "TaxCredential",
    "InvoiceIssuer",
    "InvoiceRecipient",
    # Invoice item models
    "ItemTax",
    "ItemOnBehalfOf",
    "ItemCustomsInfo",
    "ItemPropertyInfo",
    "ItemPart",
    "InvoiceItem",
    # Invoice related models
    "GlobalInformation",
    "RelatedInvoice",
    "PaidInvoiceTax",
    "PaidInvoice",
    "InvoicePayment",
    # Complement models
    "LocalTax",
    "LocalTaxesComplement",
    "PaymentComplement",
    "PayrollStockOptions",
    "PayrollOvertime",
    "PayrollEarning",
    "PayrollBalanceCompensation",
    "PayrollOtherPayment",
    "PayrollRetirement",
    "PayrollSeverance",
    "PayrollEarningsComplement",
    "PayrollDeduction",
    "PayrollDisability",
    "PayrollComplement",
    "InvoiceComplement",
    # Carta Porte models
    "UbicacionDomicilio",
    "TipoFiguraDomicilio",
    "RegimenAduanero",
    "Ubicacion",
    "DocumentoAduanero",
    "GuiaIdentificacion",
    "CantidadTransporta",
    "DetalleMercancia",
    "Mercancia",
    "Remolque",
    "Autotransporte",
    "RemolqueCCP",
    "ContenedorMaritimo",
    "TransporteMaritimo",
    "TransporteAereo",
    "DerechoDePaso",
    "CarroContenedor",
    "Carro",
    "TransporteFerroviario",
    "ParteTransporte",
    "TipoFigura",
    "CartaPorteComplement",
    # Comercio Exterior models
    "ComercioExteriorEmisorDomicilio",
    "ComercioExteriorReceptorDomicilio",
    "ComercioExteriorDestinatarioDomicilio",
    "ComercioExteriorEmisor",
    "ComercioExteriorPropietario",
    "ComercioExteriorReceptor",
    "ComercioExteriorDestinatario",
    "ComercioExteriorMercanciaDescripcionEspecifica",
    "ComercioExteriorMercancia",
    "ComercioExteriorComplement",
    # Invoice models
    "InvoiceResponse",
    "Invoice",
    "CancelInvoiceRequest",
    "CancelInvoiceResponse",
    "CreatePdfRequest",
    "FileResponse",
    "SendInvoiceRequest",
    "InvoiceStatusRequest",
    "InvoiceStatusResponse",
    # API Key models
    "ApiKey",
    # Download models
    "DownloadRule",
    "DownloadRequest",
    "MetadataItem",
    # XML models
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
    # Stamp models
    "CreditType",
    "StampTransactionType",
    "StampTransactionStatus",
    "UserLookupDto",
    "StampTransaction",
    "StampTransactionParams",
    # Manifest models
    "SignManifestRequest",
    "SignManifestResponse",
    # SAT validation models
    "SatValidationTypeIds",
    "SatValidationStatusIds",
    "SatValidationRequest",
    "SatValidationType",
    "SatValidationTypeStatus",
    "SatValidationStatus",
    "SatValidationResult",
    # Ticket models (Auto CFDI)
    "TicketStatus",
    "TicketEventType",
    "TicketActorType",
    "TicketIssuer",
    "TicketItemTax",
    "TicketItem",
    "TicketEvent",
    "Ticket",
    "TicketIngestionResult",
    "TicketCodeResult",
    "TicketListFilters",
    # Webhook models
    "WebhookEventTypes",
    "WebhookRelatedObject",
    "WebhookEventData",
    "WebhookEvent",
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
    "SatValidationService",
    "StampService",
    "ManifestService",
    "TicketService",
    # Cliente principal
    "FiscalApiClient",
    # Webhooks
    "webhooks",
    "WebhookVerificationException",
]
