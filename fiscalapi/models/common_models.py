import datetime
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake

T = TypeVar('T', bound=BaseModel)

class ApiResponse(BaseModel, Generic[T]):
    succeeded: bool = Field(alias="succeeded")
    message: str = Field(alias="message")
    details: str = Field(alias="details")
    data: Optional[T] = Field(None, alias="data")

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_snake
    )

      

class BaseDto(BaseModel):
    """Modelo base para DTOs."""
    id: str = Field(alias="id")
    created_at: Optional[datetime.datetime] = Field(alias="createdAt")
    updated_at: Optional[datetime.datetime] = Field(alias="updatedAt")
    
    model_config = ConfigDict(populate_by_name=True)

class CatalogDto(BaseDto):
    """Modelo para catálogos."""
    description: str = Field(alias="description")

    model_config = ConfigDict(populate_by_name=True)


class FiscalApiSettings(BaseModel):
    """
    Configuración para la API Fiscal.
    """
    api_url: str = Field(..., description="URL base de Fiscalapi")
    api_key: str = Field(..., description="Api Key")
    tenant: str = Field(..., description="Tenant Key.")
    api_version: str = Field("v4", description="Versión de la API Fiscal.")
    time_zone: str = Field("America/Mexico_City", description="Zona horaria para las operaciones.")

    class Config:
        title = "Fiscal API Settings"
        description = "Configuración para Fiscalapi"