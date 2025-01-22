from decimal import Decimal
from typing import  Optional
from pydantic import ConfigDict, Field
from fiscalapi.models.common_models import BaseDto, CatalogDto


class ProductTax(BaseDto):
    """Modelo para impuestos de productos."""
    product_id: str = Field(alias="productId")
    tax: Optional[dict] = Field(alias="tax")
    rate: Decimal = Field( ge=0, le=1, alias="rate")
    tax_flag: Optional[dict] = Field(alias="taxFlag")
    tax_type: Optional[dict] = Field(alias="taxType")
    
    model_config = ConfigDict(populate_by_name=True)

class Product(BaseDto):
    """Modelo para productos."""
    description: str = Field(alias="description")
    unit_price: Decimal = Field(alias="unitPrice")
    sat_unit_measurement: CatalogDto = Field(alias="satUnitMeasurement")
    sat_tax_object: CatalogDto = Field(alias="satTaxObject")
    sat_product_code: CatalogDto = Field(alias="satProductCode")
    product_taxes: list[ProductTax] = Field(alias="productTaxes")
    
    model_config = ConfigDict(populate_by_name=True)
