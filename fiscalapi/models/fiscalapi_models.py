from decimal import Decimal
from pydantic import ConfigDict, EmailStr, Field
from fiscalapi.models.common_models import BaseDto, CatalogDto
from typing import Literal, Optional
from datetime import datetime

# products models

class ProductTax(BaseDto):
    """Modelo impuesto de producto."""
    
    rate: Decimal = Field(ge=0, le=1, alias="rate", description="Tasa de impuesto")
    
    tax_id: Optional[Literal["001", "002", "003"]] = Field(default=None, alias="taxId", description="Impuesto")
    tax: Optional[CatalogDto] = Field(default=None, alias="tax", description="Impuesto expandido")

    tax_flag_id: Optional[Literal["T", "R"]] = Field(default=None, alias="taxFlagId", description="Traslado o Retención")
    tax_flag: Optional[CatalogDto] = Field(default=None, alias="taxFlag", description="Traslado o Retención expandido")
    
    tax_type_id: Optional[Literal["Tasa", "Cuota", "Exento"]] = Field(default=None, alias="taxTypeId", description="Tipo de impuesto")
    tax_type: Optional[CatalogDto] = Field(default=None, alias="taxType",  description="Tipo de impuesto expandido")
    
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )

class Product(BaseDto):
    """Modelo producto."""
    description: str = Field(alias="description")
    unit_price: Decimal = Field(alias="unitPrice")
    
    sat_unit_measurement_id: Optional[str] = Field(default="H87", alias="satUnitMeasurementId", description="Unidad de medida SAT")
    sat_unit_measurement: Optional[CatalogDto] = Field(default=None, alias="satUnitMeasurement", description="Unidad de medida SAT expandida")
    
    sat_tax_object_id: Optional[str] = Field(default="02", alias="satTaxObjectId", description="Objeto de impuesto SAT")
    sat_tax_object: Optional[CatalogDto] = Field(default=None, alias="satTaxObject", description="Objeto de impuesto SAT expandido")
    
    sat_product_code_id: Optional[str] = Field(default="01010101", alias="satProductCodeId", description="Código de producto SAT")
    sat_product_code: Optional[CatalogDto] = Field(default=None, alias="satProductCode", description="Código de producto SAT expandido")
    
    product_taxes: Optional[list[ProductTax]] = Field(default=None, alias="productTaxes", description="Impuestos del producto")
    
    
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )

# people models

class Person(BaseDto):
    """Modelo persona en FiscalAPI."""

    legal_name: Optional[str] = Field(default=None, alias="legalName", description="Razón social de la persona sin régimen de capital.")
    email: Optional[EmailStr] = Field(default=None, alias="email", description="Correo electrónico de la persona.")
    password: Optional[str]  = Field(default=None, alias="password", description="Contraseña para acceder al dashboard.")
    capital_regime: Optional[str] = Field(default=None, alias="CapitalRegime", description="Régimen de capital de la persona.")
    sat_tax_regime_id: Optional[Literal["601", "603", "605", "606", "607", "608", "610", "611", "612", "614", "615", "616", "620", "621", "622", "623", "624", "625", "626"]] = Field(default=None, alias="satTaxRegimeId", description="Código del régimen fiscal del emisor.")
    sat_tax_regime: Optional[CatalogDto] = Field(default=None, alias="satTaxRegime", description="Código del régimen fiscal expandido.")
    sat_cfdi_use_id: Optional[Literal["G01", "G02", "G03", "I01", "I02", "I03", "I04", "I05", "I06", "I07", "I08", "D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "S01", "CP01", "CN01"]] = Field(default=None, alias="satCfdiUseId", description="Código de uso del CFDI.")
    sat_cfdi_use: Optional[CatalogDto] = Field(default=None, alias="cfdiUse", description="Código de uso del CFDI expandido.")
    user_type_id: Optional[Literal["T","C", "U"]] = Field(default=None, alias="userTypeId", description="Tipo de persona.")
    user_type: Optional[CatalogDto] = Field(default=None, alias="userType", description="Tipo de persona expandido.")
    tin: Optional[str] = Field(default=None, alias="tin", description="RFC del emisor (Tax Identification Number).")
    zip_code: Optional[str] = Field(default=None, alias="zipCode", description="Código postal del emisor.")
    base64_photo: Optional[str] = Field(default=None, alias="base64Photo", description="Foto de perfil en formato base64.")
    tax_password: Optional[str] = Field(default=None, alias="taxPassword", description="Contraseña de los certificados CSD del emisor.")
    available_balance: Optional[Decimal] = Field(default=None, alias="availableBalance", description="Saldo disponible en la cuenta.")
    committed_balance: Optional[Decimal] = Field(default=None, alias="committedBalance", description="Saldo en tránsito.")
    tenant_id: Optional[str] = Field(default=None, alias="tenantId", description="ID del tenant al que pertenece el emisor.")
    tenant: Optional[CatalogDto] = Field(default=None, alias="tenant", description="Tenant expandido.")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )
    
    
class TaxFile(BaseDto):
        """Modelo TaxFile que representa un componente de un par CSD: certificado (.cer) o llave privada (.key)."""

        person_id: Optional[str] = Field(default=None, alias="personId", description="Id de la persona propietaria del certificado.")
        tin: Optional[str] = Field(default=None, alias="tin", description="RFC del propietario del certificado. Debe coincidir con el RFC del certificado.")
        base64_file: Optional[str] = Field(default=None, alias="base64File", description="Archivo certificado o llave privada en formato base64.")
        file_type: Literal[0, 1] = Field(default=None, alias="fileType", description="Tipo de archivo: 0 para certificado, 1 para llave privada.")
        password: Optional[str] = Field(default=None, alias="password", description="Contraseña de la llave privada.")
        valid_from: Optional[datetime] = Field(default=None, alias="validFrom", description="Fecha de inicio de vigencia del certificado o llave privada.")
        valid_to: Optional[datetime] = Field(default=None, alias="validTo", description="Fecha de fin de vigencia del certificado o llave privada.")
        sequence: Optional[int] = Field(default=None, alias="sequence", description="Numero de secuencia que identifica el par entre certificado y llave privada.")

        model_config = ConfigDict(
            populate_by_name=True
        )
        

# invoices models


class TaxCredential(BaseDto):
    """Modelo para los sellos del emisor (archivos .cer y .key)."""
    base64_file: str = Field(..., alias="base64File", description="Archivo en formato base64.")
    file_type: Literal[0, 1] = Field(..., alias="fileType", description="Tipo de archivo: 0 para certificado, 1 para llave privada.")
    password: str = Field(..., alias="password", description="Contraseña del archivo .key independientemente de si es un archivo .cer o .key.")

class InvoiceIssuer(BaseDto):
    """Modelo para el emisor de la factura."""
    id: Optional[str] = Field(default=None, alias="id", description="ID de la persona (emisora) en fiscalapi.")
    tin: Optional[str] = Field(default=None, alias="tin", description="RFC del emisor (Tax Identification Number).")
    legal_name: Optional[str] = Field(default=None, alias="legalName", description="Razón social del emisor sin regimen de capital.")
    tax_regime_code: Optional[str] = Field(default=None, alias="taxRegimeCode", description="Código del régimen fiscal del emisor.")
    tax_credentials: Optional[list[TaxCredential]] = Field(default=None, alias="taxCredentials", description="Sellos del emisor (archivos .cer y .key).")

class InvoiceRecipient(BaseDto):
    """Modelo para el receptor de la factura."""
    id: Optional[str] = Field(default=None, alias="id", description="ID de la persona (receptora) en fiscalapi.")
    tin: Optional[str] = Field(default=None, alias="tin", description="RFC del receptor (Tax Identification Number).")
    legal_name: Optional[str] = Field(default=None, alias="legalName", description="Razón social del receptor sin regimen de capital.")
    tax_regime_code: Optional[str] = Field(default=None, alias="taxRegimeCode", description="Código del régimen fiscal del receptor.")
    cfdi_use_code: Optional[str] = Field(default=None, alias="cfdiUseCode", description="Código del uso CFDI.")
    zip_code: Optional[str] = Field(default=None, alias="zipCode", description="Código postal del receptor. Debe coincidir con el código postal de su constancia de residencia fiscal.")
    email: Optional[str] = Field(default=None, description="Correo electrónico del receptor.")

class ItemTax(BaseDto):
    """Modelo para los impuestos aplicables a un producto o servicio."""
    tax_code: str = Field(..., alias="taxCode", description="Código del impuesto.")
    tax_type_code: str = Field(..., alias="taxTypeCode", description="Tipo de factor.")
    tax_rate: Decimal = Field(..., alias="taxRate", description="Tasa del impuesto.")
    tax_flag_code: Optional[Literal["T", "R"]] = Field(default=None, alias="taxFlagCode", description="Código que indica la naturaleza del impuesto. (T)raslado o (R)etención.")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )


class InvoiceItem(BaseDto):
    """Modelo para los conceptos de la factura (productos o servicios)."""
    id: Optional[str] = Field(default=None, alias="id", description="ID del producto en fiscalapi.")
    item_code: Optional[str] = Field(default=None, alias="itemCode", description="Código SAT del producto o servicio.")
    quantity: Decimal = Field(..., alias="quantity", description="Cantidad del producto o servicio.")
    discount: Optional[Decimal] = Field(default=None, alias="discount", description="Cantidad monetaria del descuento aplicado.")
    unit_of_measurement_code: Optional[str] = Field(default=None, alias="unitOfMeasurementCode", description="Código SAT de la unidad de medida.")
    description: Optional[str] = Field(default=None,alias="description", description="Descripción del producto o servicio.")
    unit_price: Optional[Decimal] = Field(default=None, alias="unitPrice", description="Precio unitario del producto o servicio.")
    tax_object_code: Optional[str] = Field(default=None, alias="taxObjectCode", description="Código SAT de obligaciones de impuesto.")
    item_sku: Optional[str] = Field(default=None, alias="itemSku", description="SKU o clave del sistema externo.")
    item_taxes: Optional[list[ItemTax]] = Field(default=None, alias="itemTaxes", description="Impuestos aplicables al producto o servicio.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )

class GlobalInformation(BaseDto):
    """Modelo para la información global de la factura global."""
    periodicity_code: str = Field(..., alias="periodicityCode", description="Código SAT de la periodicidad de la factura global.")
    month_code: str = Field(..., alias="monthCode", description="Código SAT del mes de la factura global.")
    year: int = Field(..., description="Año de la factura global a 4 dígitos.")

class RelatedInvoice(BaseDto):
    """Modelo para representar la relacion entre la factura actual y otras facturas previas."""
    relationship_type_code: str = Field(..., alias="relationshipTypeCode", description="Código de la relación de la factura relacionada.")
    uuid: str = Field(..., description="UUID de la factura relacionada.")

class PaidInvoiceTax(BaseDto):
    """Modelo para los impuestos aplicables a la factura pagada."""
    tax_code: str = Field(..., alias="taxCode", description="Código del impuesto.")
    tax_type_code: str = Field(..., alias="taxTypeCode", description="Tipo de factor.")
    tax_rate: Decimal = Field(..., alias="taxRate", description="Tasa del impuesto.")
    tax_flag_code: Optional[Literal["T", "R"]] = Field(default=None, alias="taxFlagCode", description="Código que indica la naturaleza del impuesto. (T)raslado o (R)etención.")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )
    
class PaidInvoice(BaseDto):
    """Modelo para las facturas pagadas con el pago recibido."""
    uuid: str = Field(..., alias="uuid", description="UUID de la factura pagada.")
    series: str = Field(..., alias="series", description="Serie de la factura pagada.")
       
    partiality_number: int = Field(..., alias="partialityNumber", description="Número de parcialidad.")
    sub_total: Decimal = Field(..., alias="subTotal", description="Subtotal de la factura pagada.")
    previous_balance: Decimal = Field(..., alias="previousBalance", description="Saldo anterior de la factura pagada.")
    payment_amount: Decimal = Field(..., alias="paymentAmount", description="Monto pagado de la factura.")
    remaining_balance: Decimal = Field(..., alias="remainingBalance", description="Saldo restante de la factura pagada.")
    
    number: str = Field(..., alias="number", description="Folio de la factura pagada.")
    currency_code: str = Field(default="MXN", alias="currencyCode", description="Código de la moneda utilizada en la factura pagada.")
    tax_object_code: str = Field(..., alias="taxObjectCode", description="Código de obligaciones de impuesto.")
    equivalence: Optional[Decimal] = Field(default=1, description="Equivalencia de la moneda. Este campo es obligatorio cuando la moneda del documento relacionado (PaidInvoice.CurrencyCode) difiere de la moneda en que se realiza el pago ( InvoicePayment.CurrencyCode).")
    paid_invoice_taxes: list[PaidInvoiceTax] = Field(..., alias="paidInvoiceTaxes", description="Impuestos aplicables a la factura pagada.")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )
    

    
class InvoicePayment(BaseDto):
    """Modelo para los pagos recibidos para liquidar la factura."""
    payment_date: str = Field(..., alias="paymentDate", description="Fecha de pago.")
    payment_form_code: str = Field(..., alias="paymentFormCode", description="Código de la forma de pago.")
    
    currency_code: Literal ["MXN", "USD", "EUR"] = Field(default="MXN", alias="currencyCode", description="Código de la moneda utilizada en el pago.")
    exchange_rate: Optional[Decimal] = Field(default=1, alias="exchangeRate", description="Tipo de cambio FIX conforme a la moneda registrada en la factura. Si la moneda es MXN, el tipo de cambio debe ser 1..")
    amount: Decimal = Field(..., description="Monto del pago.")
    source_bank_tin: str = Field(..., alias="sourceBankTin", description="RFC del banco origen. (Rfc del banco emisor del pago)")
    source_bank_account: str = Field(..., alias="sourceBankAccount", description="Cuenta bancaria origen. (Cuenta bancaria del banco emisor del pago)")
    target_bank_tin: str = Field(..., alias="targetBankTin", description="RFC del banco destino. (Rfc del banco receptor del pago)")
    target_bank_account: str = Field(..., alias="targetBankAccount", description="Cuenta bancaria destino (Cuenta bancaria del banco receptor del pago)")
    paid_invoices: list[PaidInvoice] = Field(..., alias="paidInvoices", description="Facturas pagadas con el pago recibido.")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )



class InvoiceResponse(BaseDto):
    """Modelo para la respuesta del SAT después del timbrado de la factura."""
    id: Optional[str] = Field(default=None, description="ID de la respuesta.")
    invoice_id: Optional[str] = Field(default=None, alias="invoiceId", description="ID de la factura a la que pertenece la respuesta.")
    invoice_uuid: Optional[str] = Field(default=None, alias="invoiceUuid", description="Folio Fiscal (UUID) proporcionado por el SAT tras el timbrado de la factura.")
    invoice_certificate_number: Optional[str] = Field(default=None, alias="invoiceCertificateNumber", description="Número de certificado del emisor.")
    invoice_base64_sello: Optional[str] = Field(default=None, alias="invoiceBase64Sello", description="Sello digital del CFDI en formato Base64.")
    invoice_signature_date: Optional[datetime] = Field(default=None, alias="invoiceSignatureDate", description="Fecha y hora de la firma electrónica del CFDI por parte del emisor.")
    invoice_base64_qr_code: Optional[str] = Field(default=None, alias="invoiceBase64QrCode", description="Imagen del código QR en formato Base64.")
    invoice_base64: Optional[str] = Field(default=None, alias="invoiceBase64", description="XML de la factura en formato Base64.")
    sat_base64_sello: Optional[str] = Field(default=None, alias="satBase64Sello", description="Sello digital del SAT en formato Base64.")
    sat_base64_original_string: Optional[str] = Field(default=None, alias="satBase64OriginalString", description="Cadena original de la factura codificada en Base64.")
    sat_certificate_number: Optional[str] = Field(default=None, alias="satCertificateNumber", description="Número de certificado del SAT.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    
class Invoice(BaseDto):
    """Modelo para la factura."""
    version_code: Optional[str] = Field(default="4.0", alias="versionCode", description="Código de la versión de la factura.")
    consecutive: Optional[int] = Field(default=None, description="Consecutivo de facturas por cuenta. Se incrementa con cada factura generada en tu cuenta independientemente del RFC emisor.")
    number: Optional[str] = Field(default=None, description="Consecutivo de facturas por RFC emisor. Se incrementa por cada factura generada por el mismo RFC emisor.")
    subtotal: Optional[Decimal] = Field(default=None, description="Subtotal de la factura. Generado automáticamente por Fiscalapi.")
    discount: Optional[Decimal] = Field(default=None, description="Descuento aplicado a la factura. Generado automáticamente por Fiscalapi a partir de los descuentos aplicados a los productos o servicios.")
    total: Optional[Decimal] = Field(default=None, description="Total de la factura. Generado automáticamente por Fiscalapi.")
    uuid: Optional[str] = Field(default=None, description="UUID de la factura, es el folio fiscal asignado por el SAT al momento del timbrado.")
    status: Optional[CatalogDto] = Field(default=None, description="El estatus de la factura")
    series: str = Field(..., description="Número de serie que utiliza el contribuyente para control interno.")
    date: datetime = Field(..., description="Fecha y hora de expedición del comprobante fiscal.")
    payment_form_code: Optional[str] = Field(default=None, alias="paymentFormCode", description="Código de la forma de pago.")
    currency_code: Literal["MXN", "USD", "EUR", "XXX"] = Field(default="MXN", alias="currencyCode", description="Código de la moneda utilizada.")
    type_code: Optional[Literal["I", "E", "T", "N", "P"]] = Field(default="I", alias="typeCode", description="Código de tipo de factura.")
    expedition_zip_code: str = Field(..., alias="expeditionZipCode", description="Código postal del emisor.")
    export_code: Optional[Literal["01", "02", "03", "04"]] = Field(default="01", alias="exportCode", description="Código que identifica si la factura ampara una operación de exportación.")
    payment_method_code: Optional[Literal["PUE", "PPD"]] = Field(default=None, alias="paymentMethodCode", description="Código de método para la factura de pago.")
    exchange_rate: Optional[Decimal] = Field(default=1, alias="exchangeRate", description="Tipo de cambio FIX.")
    issuer: Optional[InvoiceIssuer] = Field(..., description="El emisor de la factura.")
    recipient: Optional[InvoiceRecipient] = Field(..., description="El receptor de la factura.")
    items: Optional[list[InvoiceItem]] = Field(default_factory=list, description="Conceptos de la factura (productos o servicios).")
    global_information: Optional[GlobalInformation] = Field(default=None, alias="globalInformation", description="Información global de la factura.")
    related_invoices: Optional[list[RelatedInvoice]] = Field(default=None, alias="relatedInvoices", description="Facturas relacionadas.")
    payments: Optional[list[InvoicePayment]] = Field(default=None, description="Pago o pagos recibidos para liquidar la factura cuando la factura es un complemento de pago.")
    responses: Optional[list[InvoiceResponse]] = Field(default=None, description="Respuestas del SAT. Contiene la información de timbrado de la factura.")
    

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )


        
class CancelInvoiceRequest(BaseDto):
    """Modelo de cancelación de factura."""
    id: Optional[str] = Field(default=None, alias="id", description="ID de la factura a cancelar. Obligatorio cuando se cancela por referencias.")
    invoice_uuid: Optional[str] = Field(default=None, alias="invoiceUuid", description="UUID de la factura a cancelar. Obligatorio cuando se cancela por valores.")
    tin: Optional[str] = Field(default=None, alias="tin", description="RFC del emisor de la factura. Obligatorio cuando se cancela por valores.")
    cancellation_reason_code: Literal["01", "02", "03", "04"] = Field(..., alias="cancellationReasonCode", description="Código del motivo de cancelación.")
    replacement_uuid: Optional[str] = Field(default=None, alias="replacementUuid", description="UUID de la factura de reemplazo. Obligatorio si el motivo de cancelación es '01'.")
    tax_credentials: Optional[list[TaxCredential]] = Field(default=None, alias="taxCredentials", description="Sellos del emisor. Obligatorio cuando se cancela por valores.")

    model_config = ConfigDict(populate_by_name=True)

class CancelInvoiceResponse(BaseDto):
    """Modelo de respuesta para la cancelación de factura."""
    base64_cancellation_acknowledgement: str = Field(default=None, alias="base64CancellationAcknowledgement", description="Acuse de cancelación en formato base64. Contiene el XML del acuse de cancelación del SAT codificado en base64.")
    invoice_uuids: Optional[dict[str, str]] = Field(default=None, alias="invoiceUuids", description="Diccionario de UUIDs de facturas con su respectivo código de estatus de cancelación. La llave es el UUID de la factura y el valor es el código de estatus.")

    model_config = ConfigDict(populate_by_name=True)


class CreatePdfRequest(BaseDto):
    """Modelo para la generación de PDF de una factura."""
    invoice_id: str = Field(..., alias="invoiceId", description="ID de la factura para la cual se generará el PDF.")
    band_color: Optional[str] = Field(default=None, alias="bandColor", description="Color de la banda del PDF en formato hexadecimal. Ejemplo: '#FFA500'.")
    font_color: Optional[str] = Field(default=None, alias="fontColor", description="Color de la fuente del texto sobre la banda en formato hexadecimal. Ejemplo: '#FFFFFF'.")
    base64_logo: Optional[str] = Field(default=None, alias="base64Logo", description="Logotipo en formato base64 que se mostrará en el PDF.")

    model_config = ConfigDict(populate_by_name=True)

class FileResponse(BaseDto):
    """Modelo de respuesta para la generación de PDF o recuperación de XML."""
    base64_file: Optional[str] = Field(default=None, alias="base64File", description="Contenido del archivo en formato base64.")
    file_name: Optional[str] = Field(default=None, alias="fileName", description="Nombre del archivo generado.")
    file_extension: Optional[str] = Field(default=None, alias="fileExtension", description="Extensión del archivo. Ejemplo: '.pdf'.")

    model_config = ConfigDict(populate_by_name=True)


class SendInvoiceRequest(BaseDto):
    """Modelo para el envío de facturas por correo electrónico."""
    invoice_id: str = Field(..., alias="invoiceId", description="ID de la factura para la cual se enviará el PDF.")
    to_email: str = Field(..., alias="toEmail", description="Correo electrónico del destinatario.")
    band_color: Optional[str] = Field(default=None, alias="bandColor", description="Color de la banda del PDF en formato hexadecimal. Ejemplo: '#FFA500'.")
    font_color: Optional[str] = Field(default=None, alias="fontColor", description="Color de la fuente del texto sobre la banda en formato hexadecimal. Ejemplo: '#FFFFFF'.")
    base64_logo: Optional[str] = Field(default=None, alias="base64Logo", description="Logotipo en formato base64 que se mostrará en el PDF.")

    model_config = ConfigDict(populate_by_name=True)


class InvoiceStatusRequest(BaseDto):
    """Modelo para consultar estado de facturas."""
    id: Optional[str] = Field(default=None, description="Id de la factura a consultar")
    issuer_tin: Optional[str] = Field(default=None, alias="issuerTin", description="RFC Emisor la factura")
    recipient_tin: Optional[str] = Field(default=None, alias="recipientTin", description="RFC Receptor de la factura")
    invoice_total: Optional[Decimal] = Field(default=None, alias="invoiceTotal", description="Total de la factura")
    invoice_uuid: Optional[str] = Field(default=None, alias="invoiceUuid", description="Folio fiscal factura a consultar")
    last8_digits_issuer_signature: Optional[str] = Field(default=None, alias="last8DigitsIssuerSignature", description="Últimos ocho caracteres del sello digital del emisor")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )

class InvoiceStatusResponse(BaseDto):
    """Modelo de respuesta de consulta de estado de facturas."""
    status_code: str = Field(..., alias="statusCode", description="Código de estatus retornado por el SAT")
    status: str = Field(..., description="Estado actual de la factura. Posibles valores: 'Vigente' | 'Cancelado' | 'No Encontrado'")
    cancelable_status: str = Field(..., alias="cancelableStatus", description="Indica si la factura es cancelable. Posibles valores: 'Cancelable con aceptación' | 'No cancelable' | 'Cancelable sin aceptación'")
    cancellation_status: str = Field(..., alias="cancellationStatus", description="Detalle del estatus de cancelación")
    efos_validation: str = Field(..., alias="efosValidation", description="Codigo que indica si el RFC Emisor se encuentra dentro de la lista negra de EFOS")

    model_config = ConfigDict(populate_by_name=True)
    


class ApiKey(BaseDto):
    """Modelo de clave de autenticación en fiscalapi."""
    
    id: Optional[str] = Field(default=None, alias="id", description="El identificador único de la API key.")
    environment: Optional[str] = Field(default=None, alias="environment", description="El entorno al que pertenece la API key.")
    api_key_value: Optional[str] = Field(default=None, alias="apiKeyValue", description="El API key. Este valor es el que se utiliza para autenticar las solicitudes.")
    person_id: Optional[str] = Field(default=None, alias="personId", description="El identificador único de la persona a la que pertenece la API key.")
    tenant_id: Optional[str] = Field(default=None, alias="tenantId", description="El identificador único del tenant al que pertenece la API key.")
    api_key_status: Optional[int] = Field(default=None, alias="apiKeyStatus", description="El estado de la API key. 0=Revocada, 1=Activa")
    description: Optional[str] = Field(default=None, alias="description", description="Nombre o description de la API key.")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )
    
    
#Download Models

class DownloadRule(BaseDto):
    """Representa una plantilla para crear solicitudes de descarga de CFDI o metadatos."""
    
    person_id: Optional[str] = Field(default=None, alias="personId", description="ID de la persona asociada.")
    person: Optional[Person] = Field(default=None, description="Información de la persona.")
    tin: Optional[str] = Field(default=None, description="RFC de la regla de descarga.")
    description: Optional[str] = Field(default=None, description="Descripción de la regla.")
    
    # 1 Pendiente, 2 Aprobada, 3 Rechazada, 4 Abandonada
    download_rule_status_id: Optional[str] = Field(default=None, alias="downloadRuleStatusId", description="Estado de la regla de descarga (1 Pendiente, 2 Aprobada, 3 Rechazada, 4 Abandonada).")
    download_rule_status: Optional[CatalogDto] = Field(default=None, alias="downloadRuleStatus", description="Estado de la regla de descarga.")
    
    # CFDI, Metadata
    sat_query_type_id: Optional[str] = Field(default=None, alias="satQueryTypeId", description="Tipo de consulta SAT (CFDI, Metadata).")
    sat_query_type: Optional[CatalogDto] = Field(default=None, alias="satQueryType", description="Tipo de consulta SAT.")
    
    # Emitidos, Recibidos
    download_type_id: Optional[str] = Field(default=None, alias="downloadTypeId", description="Tipo de descarga (Emitidos, Recibidos).")
    download_type: Optional[CatalogDto] = Field(default=None, alias="downloadType", description="Tipo de descarga.")
    
    # Vigente, Cancelado
    sat_invoice_status_id: Optional[str] = Field(default=None, alias="satInvoiceStatusId", description="Estado del comprobante SAT (Vigente, Cancelado).")
    sat_invoice_status: Optional[CatalogDto] = Field(default=None, alias="satInvoiceStatus", description="Estado del comprobante SAT.")

    model_config = ConfigDict(
        populate_by_name=True
    )
    
    
class DownloadRequest(BaseDto):
    """Representa una solicitud de descarga de CFDI o metadatos del SAT."""
    
    consecutive: Optional[int] = Field(default=None, description="Consecutivo de la solicitud.")
    sat_request_id: Optional[str] = Field(default=None, alias="satRequestId", description="ID de solicitud SAT utilizado para rastrear la solicitud en el sistema SAT.")
    download_rule_id: Optional[str] = Field(default=None, alias="downloadRuleId", description="ID de la regla asociada con la solicitud.")
    
    download_type_id: Optional[str] = Field(default=None, alias="downloadTypeId", description="ID del tipo de descarga.")
    download_type: Optional[CatalogDto] = Field(default=None, alias="downloadType", description="Tipo de descarga.")
    
    download_request_type_id: Optional[str] = Field(default=None, alias="downloadRequestTypeId", description="ID del tipo de solicitud de descarga.")
    download_request_type: Optional[CatalogDto] = Field(default=None, alias="downloadRequestType", description="Tipo de solicitud de descarga.")
    
    recipient_tin: Optional[str] = Field(default=None, alias="recipientTin", description="RFC del receptor. CFDIs específicos o metadatos del RFC receptor dado.")
    issuer_tin: Optional[str] = Field(default=None, alias="issuerTin", description="RFC del emisor. CFDIs específicos o metadatos del RFC emisor dado.")
    requester_tin: Optional[str] = Field(default=None, alias="requesterTin", description="RFC quien está solicitando la consulta.")
    
    start_date: Optional[datetime] = Field(default=None, alias="startDate", description="Fecha inicial para la solicitud asociada.")
    end_date: Optional[datetime] = Field(default=None, alias="endDate", description="Fecha final para la solicitud asociada.")
    
    sat_query_type_id: Optional[str] = Field(default=None, alias="satQueryTypeId", description="Tipo de solicitud para la petición. CFDI o Metadata.")
    sat_query_type: Optional[CatalogDto] = Field(default=None, alias="satQueryType", description="Tipo de consulta SAT.")
    
    sat_invoice_type_id: Optional[str] = Field(default=None, alias="satInvoiceTypeId", description="Tipo de factura específico a solicitar. Ingreso, Egreso, Traslado, Nómina, Pago, Todos.")
    sat_invoice_type: Optional[CatalogDto] = Field(default=None, alias="satInvoiceType", description="Tipo de comprobante SAT.")
    
    sat_invoice_status_id: Optional[str] = Field(default=None, alias="satInvoiceStatusId", description="Estado de los CFDIs a solicitar.")
    sat_invoice_status: Optional[CatalogDto] = Field(default=None, alias="satInvoiceStatus", description="Estado del comprobante SAT.")
    
    sat_invoice_complement_id: Optional[str] = Field(default=None, alias="satInvoiceComplementId", description="Complementos de CFDIs para la solicitud.")
    sat_invoice_complement: Optional[CatalogDto] = Field(default=None, alias="satInvoiceComplement", description="Complemento del comprobante SAT.")
    
    sat_request_status_id: Optional[str] = Field(default=None, alias="satRequestStatusId", description="Estado actual de la solicitud. DESCONOCIDO, ACEPTADA, EN PROCESO, TERMINADA, ERROR, RECHAZADA, VENCIDA.")
    sat_request_status: Optional[CatalogDto] = Field(default=None, alias="satRequestStatus", description="Estado de la solicitud SAT.")
    
    download_request_status_id: Optional[str] = Field(default=None, alias="downloadRequestStatusId", description="ID del estado de la solicitud de Fiscalapi.")
    download_request_status: Optional[CatalogDto] = Field(default=None, alias="downloadRequestStatus", description="Estado de la solicitud de descarga Fiscalapi.")
    
    last_attempt_date: Optional[datetime] = Field(default=None, alias="lastAttemptDate", description="Fecha del último intento para la solicitud asociada.")
    next_attempt_date: Optional[datetime] = Field(default=None, alias="nextAttemptDate", description="Fecha del siguiente intento para la solicitud asociada.")
    
    invoice_count: Optional[int] = Field(default=None, alias="invoiceCount", description="Número de CFDIs encontrados para la solicitud cuando la solicitud ha terminado.")
    package_ids: Optional[list[str]] = Field(default_factory=list, alias="packageIds", description="Lista de IDs de paquetes disponibles para descarga cuando la solicitud ha terminado.")
    is_ready_to_download: Optional[bool] = Field(default=None, alias="isReadyToDownload", description="Indica si la solicitud está lista para descarga, se vuelve verdadero cuando la solicitud ha terminado y los paquetes están disponibles.")
    retries_count: Optional[int] = Field(default=None, alias="retriesCount", description="Número total de reintentos realizados para esta solicitud a través de todas las re-presentaciones.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )


class MetadataItem(BaseDto):
    """Representa un elemento de metadatos de CFDI."""
    
    invoice_uuid: Optional[str] = Field(default=None, alias="invoiceUuid", description="Folio de la factura - UUID.")
    issuer_tin: Optional[str] = Field(default=None, alias="issuerTin", description="RFC del emisor del comprobante.")
    issuer_name: Optional[str] = Field(default=None, alias="issuerName", description="Nombre o razón social del emisor.")
    recipient_tin: Optional[str] = Field(default=None, alias="recipientTin", description="RFC del receptor del comprobante.")
    recipient_name: Optional[str] = Field(default=None, alias="recipientName", description="Nombre o razón social del receptor.")
    pac_tin: Optional[str] = Field(default=None, alias="pacTin", description="RFC del Proveedor Autorizado de Certificación (PAC).")
    invoice_date: Optional[datetime] = Field(default=None, alias="invoiceDate", description="Fecha y hora de emisión del comprobante.")
    sat_certification_date: Optional[datetime] = Field(default=None, alias="satCertificationDate", description="Fecha y hora de certificación por el SAT.")
    amount: Optional[Decimal] = Field(default=None, description="Monto total del comprobante.")
    invoice_type: Optional[str] = Field(default=None, alias="invoiceType", description="Tipo de comprobante (I = Ingreso, E = Egreso, T = Traslado, N = Nómina, P = Pago).")
    status: Optional[int] = Field(default=None, description="Estatus del comprobante (1 = Vigente, 0 = Cancelado).")
    cancellation_date: Optional[datetime] = Field(default=None, alias="cancellationDate", description="Fecha de cancelación del comprobante (si aplica).")
    download_package_id: Optional[str] = Field(default=None, alias="downloadPackageId", description="ID del paquete de descarga.")
    download_request_id: Optional[str] = Field(default=None, alias="downloadRequestId", description="ID de la solicitud de descarga.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            Decimal: str
        }
    )
    
    
class XmlGlobalInformation(BaseDto):
    """Información global del CFDI (para CFDI globales)."""
    
    periodicity: Optional[str] = Field(default=None, description="Periodicidad del CFDI global.")
    month: Optional[str] = Field(default=None, description="Mes del CFDI global.")
    year: Optional[int] = Field(default=None, description="Año del CFDI global.")

    model_config = ConfigDict(populate_by_name=True)


class XmlIssuer(BaseDto):
    """Información del emisor del CFDI."""
    
    tin: Optional[str] = Field(default=None, description="RFC del emisor.")
    legal_name: Optional[str] = Field(default=None, alias="legalName", description="Razón social del emisor.")
    tax_regime: Optional[str] = Field(default=None, alias="taxRegime", description="Régimen fiscal del emisor.")

    model_config = ConfigDict(populate_by_name=True)


class XmlRecipient(BaseDto):
    """Información del receptor del CFDI."""
    
    tin: Optional[str] = Field(default=None, description="RFC del receptor.")
    legal_name: Optional[str] = Field(default=None, alias="legalName", description="Razón social del receptor.")
    zip_code: Optional[str] = Field(default=None, alias="zipCode", description="Código postal del receptor.")
    tax_regime: Optional[str] = Field(default=None, alias="taxRegime", description="Régimen fiscal del receptor.")
    cfdi_use: Optional[str] = Field(default=None, alias="cfdiUse", description="Uso del CFDI.")
    foreign_tax_id: Optional[str] = Field(default=None, alias="foreignTaxId", description="ID fiscal extranjero.")
    fiscal_residence: Optional[str] = Field(default=None, alias="fiscalResidence", description="Residencia fiscal.")

    model_config = ConfigDict(populate_by_name=True)


class XmlRelated(BaseDto):
    """Información sobre facturas relacionadas del CFDI (CFDI relacionados)."""
    
    xml_id: Optional[str] = Field(default=None, alias="xmlId", description="ID del XML.")
    relationship_type: Optional[str] = Field(default=None, alias="relationshipType", description="Tipo de relación.")
    cfdi_uuid: Optional[str] = Field(default=None, alias="cfdiUuid", description="UUID del CFDI relacionado.")

    model_config = ConfigDict(populate_by_name=True)


class XmlTax(BaseDto):
    """Información de los impuestos del CFDI."""
    
    base: Optional[Decimal] = Field(default=None, description="Base del impuesto.")
    tax: Optional[str] = Field(default=None, description="Impuesto.")
    tax_type: Optional[str] = Field(default=None, alias="taxType", description="Tipo de impuesto.")
    rate: Optional[Decimal] = Field(default=None, description="Tasa del impuesto.")
    amount: Optional[Decimal] = Field(default=None, description="Monto del impuesto.")
    tax_flag: Optional[str] = Field(default=None, alias="taxFlag", description="Bandera del impuesto.")
    xml_id: Optional[str] = Field(default=None, alias="xmlId", description="ID del XML.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )


class XmlItemCustomsInformation(BaseDto):
    """Información aduanera de los conceptos del CFDI."""
    
    xml_item_id: Optional[str] = Field(default=None, alias="xmlItemId", description="ID del concepto XML.")
    customs_document_number: Optional[str] = Field(default=None, alias="customsDocumentNumber", description="Número de documento aduanero.")

    model_config = ConfigDict(populate_by_name=True)


class XmlItemPropertyAccount(BaseDto):
    """Cuenta predial de los conceptos del CFDI."""
    
    xml_item_id: Optional[str] = Field(default=None, alias="xmlItemId", description="ID del concepto XML.")
    property_account_number: Optional[str] = Field(default=None, alias="propertyAccountNumber", description="Número de cuenta predial.")

    model_config = ConfigDict(populate_by_name=True)


class XmlItemTax(BaseDto):
    """Impuestos de los conceptos del CFDI."""
    
    base: Optional[Decimal] = Field(default=None, description="Base del impuesto.")
    tax: Optional[str] = Field(default=None, description="Impuesto.")
    tax_type: Optional[str] = Field(default=None, alias="taxType", description="Tipo de impuesto.")
    rate: Optional[Decimal] = Field(default=None, description="Tasa del impuesto.")
    amount: Optional[Decimal] = Field(default=None, description="Monto del impuesto.")
    tax_flag: Optional[str] = Field(default=None, alias="taxFlag", description="Bandera del impuesto.")
    xml_item_id: Optional[str] = Field(default=None, alias="xmlItemId", description="ID del concepto XML.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )


class XmlItem(BaseDto):
    """Información de los conceptos del CFDI."""
    
    xml_id: Optional[str] = Field(default=None, alias="xmlId", description="ID del XML.")
    item_code: Optional[str] = Field(default=None, alias="itemCode", description="Código del producto/servicio.")
    sku: Optional[str] = Field(default=None, description="SKU del producto.")
    quantity: Optional[Decimal] = Field(default=None, description="Cantidad.")
    unit_measurement: Optional[str] = Field(default=None, alias="unitMeasurement", description="Unidad de medida.")
    description: Optional[str] = Field(default=None, description="Descripción del concepto.")
    unit_price: Optional[Decimal] = Field(default=None, alias="unitPrice", description="Precio unitario.")
    amount: Optional[Decimal] = Field(default=None, description="Importe.")
    discount: Optional[Decimal] = Field(default=None, description="Descuento.")
    tax_object: Optional[str] = Field(default=None, alias="taxObject", description="Objeto de impuesto.")
    third_party_account: Optional[str] = Field(default=None, alias="thirdPartyAccount", description="Cuenta de terceros.")
    
    xml_item_customs_information: Optional[list[XmlItemCustomsInformation]] = Field(
        default_factory=list, 
        alias="xmlItemCustomsInformation", 
        description="Información aduanera del concepto."
    )
    xml_item_property_accounts: Optional[list[XmlItemPropertyAccount]] = Field(
        default_factory=list, 
        alias="xmlItemPropertyAccounts", 
        description="Cuentas prediales del concepto."
    )
    taxes: Optional[list[XmlItemTax]] = Field(default_factory=list, description="Impuestos del concepto.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={Decimal: str}
    )


class XmlComplement(BaseDto):
    """Información de los complementos del CFDI."""
    
    complement_name: Optional[str] = Field(default=None, alias="complementName", description="Nombre del complemento.")
    base64_complement_value: Optional[str] = Field(default=None, alias="base64ComplementValue", description="Valor del complemento en base64.")
    xml_id: Optional[str] = Field(default=None, alias="xmlId", description="ID del XML.")

    model_config = ConfigDict(populate_by_name=True)


class Xml(BaseDto):
    """Representa el XML de un CFDI (Comprobante Fiscal Digital por Internet) descargado desde el SAT."""
    
    # Regla de descarga
    download_request_id: Optional[str] = Field(default=None, alias="downloadRequestId", description="ID de la solicitud de descarga.")
    
    # Version del CFDI
    version: Optional[str] = Field(default=None, description="Versión del CFDI.")
    
    # Serie
    series: Optional[str] = Field(default=None, description="Serie del CFDI.")
    
    # Folio
    number: Optional[str] = Field(default=None, description="Folio del CFDI.")
    
    # Fecha de emisión del CFDI
    date: Optional[datetime] = Field(default=None, description="Fecha de emisión del CFDI.")
    
    # Codigo de la forma de pago
    payment_form: Optional[str] = Field(default=None, alias="paymentForm", description="Código de la forma de pago.")
    
    # Codigo del método de pago
    payment_method: Optional[str] = Field(default=None, alias="paymentMethod", description="Código del método de pago.")
    
    # Numero de certificado del emisor
    certificate_number: Optional[str] = Field(default=None, alias="certificateNumber", description="Número de certificado del emisor.")
    
    # Condiciones de pago
    payment_conditions: Optional[str] = Field(default=None, alias="paymentConditions", description="Condiciones de pago.")
    
    # Subtotal del CFDI
    sub_total: Optional[Decimal] = Field(default=None, alias="subTotal", description="Subtotal del CFDI.")
    
    # Descuento aplicado al CFDI
    discount: Optional[Decimal] = Field(default=None, description="Descuento aplicado al CFDI.")
    
    # Codigo de la moneda del CFDI
    currency: Optional[str] = Field(default=None, description="Código de la moneda del CFDI.")
    
    # Tipo de cambio del CFDI (si aplica)
    exchange_rate: Optional[Decimal] = Field(default=None, alias="exchangeRate", description="Tipo de cambio del CFDI (si aplica).")
    
    # Total del CFDI
    total: Optional[Decimal] = Field(default=None, description="Total del CFDI.")
    
    # Tipo de comprobante (I = Ingreso, E = Egreso, T = Traslado, N = Nómina, P = Pago)
    invoice_type: Optional[str] = Field(default=None, alias="invoiceType", description="Tipo de comprobante (I = Ingreso, E = Egreso, T = Traslado, N = Nómina, P = Pago).")
    
    # Codigo de exportación (si aplica)
    export: Optional[str] = Field(default=None, description="Código de exportación (si aplica).")
    
    # Lugar de expedición del CFDI
    expedition_zip_code: Optional[str] = Field(default=None, alias="expeditionZipCode", description="Lugar de expedición del CFDI.")
    
    # Confirmacion si aplica
    confirmation: Optional[str] = Field(default=None, description="Confirmación si aplica.")
    
    # Total impuestos retenidos
    total_withheld_taxes: Optional[Decimal] = Field(default=None, alias="totalWithheldTaxes", description="Total impuestos retenidos.")
    
    # Total impuestos trasladados
    total_transferred_taxes: Optional[Decimal] = Field(default=None, alias="totalTransferredTaxes", description="Total impuestos trasladados.")
    
    # Información global del CFDI (para CFDI globales)
    xml_global_information: Optional[XmlGlobalInformation] = Field(default=None, alias="xmlGlobalInformation", description="Información global del CFDI (para CFDI globales).")
    
    # Información de impuestos del CFDI
    taxes: Optional[list[XmlTax]] = Field(default_factory=list, description="Información de impuestos del CFDI.")
    
    # Información sobre facturas relacionada del CFDI (CFDI relacionados)
    xml_related: Optional[list[XmlRelated]] = Field(default_factory=list, alias="xmlRelated", description="Información sobre facturas relacionadas del CFDI (CFDI relacionados).")
    
    # Información del emisor del CFDI
    xml_issuer: Optional[XmlIssuer] = Field(default=None, alias="xmlIssuer", description="Información del emisor del CFDI.")
    
    # Información del receptor del CFDI
    xml_recipient: Optional[XmlRecipient] = Field(default=None, alias="xmlRecipient", description="Información del receptor del CFDI.")
    
    # Información de los conceptos del CFDI
    xml_items: Optional[list[XmlItem]] = Field(default_factory=list, alias="xmlItems", description="Información de los conceptos del CFDI.")
    
    # Información de los complementos del CFDI
    xml_complements: Optional[list[XmlComplement]] = Field(default_factory=list, alias="xmlComplements", description="Información de los complementos del CFDI.")
    
    # Xml crudo en base64
    base64_content: Optional[str] = Field(default=None, alias="base64Content", description="XML crudo en base64.")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            Decimal: str
        }
    )