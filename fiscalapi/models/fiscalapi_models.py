from decimal import Decimal
from pydantic import ConfigDict, Field
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
