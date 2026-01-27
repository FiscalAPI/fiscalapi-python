from datetime import datetime
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    succeeded: bool = Field(default=..., alias="succeeded")
    message: Optional[str] = Field(default=None, alias="message")
    details: Optional[str] = Field(default=None, alias="details")
    data: Optional[T] = Field(default=None, alias="data")
    http_status_code: Optional[int] = Field(default=None, alias="httpStatusCode")

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_snake
    )


class PagedList(BaseModel, Generic[T]):
    """Modelo para la estructura de la lista paginada."""
    items: list[T] = Field(default_factory=list, alias="items", description="Lista de elementos paginados")
    page_number: int = Field(default=..., alias="pageNumber", description="Número de página actual")
    total_pages: int = Field(default=..., alias="totalPages", description="Cantidad total de páginas")
    total_count: int = Field(default=..., alias="totalCount", description="Cantidad total de elementos")
    has_previous_page: bool = Field(default=..., alias="hasPreviousPage", description="Indica si hay una página anterior")
    has_next_page: bool = Field(default=..., alias="hasNextPage", description="Indica si hay una página siguiente")

    model_config = ConfigDict(populate_by_name=True)


class ValidationFailure(BaseModel):
    """Modelo para errores de validación."""
    property_name: str = Field(alias="propertyName")
    error_message: str = Field(alias="errorMessage")
    attempted_value: Optional[Any] = Field(default=None, alias="attemptedValue")

    model_config = ConfigDict(populate_by_name=True)


class BaseDto(BaseModel):
    """Modelo base para DTOs."""
    id: Optional[str] = Field(default=None, alias="id")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")
    
    model_config = ConfigDict(populate_by_name=True)

class CatalogDto(BaseDto):
    """Modelo para catálogos."""
    description: str = Field(default=..., alias="description")


class FiscalApiSettings(BaseModel):
    """
    Objeto que contiene la configuración necesaria para interactuar con Fiscalapi.
    """
    api_url: str = Field(default=..., description="URL base de la api.")
    api_key: str = Field(default=..., description="Api Key")
    tenant: str = Field(default=..., description="Tenant Key.")
    api_version: str = Field(default="v4", description="Versión de la api.")
    time_zone: str = Field(default="America/Mexico_City", description="Zona horaria ")
    debug: bool = Field(default=False, description="Indica si se debe imprimir el payload request y response.")

    model_config = ConfigDict(
        title="FiscalApi Settings",
        json_schema_extra={"description": "Configuración para Fiscalapi"}
    )