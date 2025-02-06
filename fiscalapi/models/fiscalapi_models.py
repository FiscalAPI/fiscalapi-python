import datetime
from decimal import Decimal
from pydantic import ConfigDict, EmailStr, Field
from fiscalapi.models.common_models import BaseDto, CatalogDto
from typing import Literal, Optional

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
        valid_from: Optional[datetime.datetime] = Field(default=None, alias="validFrom", description="Fecha de inicio de vigencia del certificado o llave privada.")
        valid_to: Optional[datetime.datetime] = Field(default=None, alias="validTo", description="Fecha de fin de vigencia del certificado o llave privada.")
        sequence: Optional[int] = Field(default=None, alias="sequence", description="Numero de secuencia que identifica el par entre certificado y llave privada.")

        model_config = ConfigDict(
            populate_by_name=True
        )