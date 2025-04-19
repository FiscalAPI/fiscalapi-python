from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake

T = TypeVar('T', bound=BaseModel)

class ApiResponse(BaseModel, Generic[T]):
    succeeded: bool = Field(alias="succeeded")
    message: Optional[str] = Field(alias="message")
    details: Optional[str] = Field(alias="details")
    data: Optional[T] = Field(None, alias="data")

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_snake
    )


class PagedList(BaseModel, Generic[T]):
    """Modelo para la estructura de la lista paginada."""
    items: List[T] = Field(default=[], alias="items", description="Lista de elementos paginados")
    page_number: int = Field(alias="pageNumber", description="Número de página actual")
    total_pages: int = Field(alias="totalPages", description="Cantidad total de páginas")
    total_count: int = Field(alias="totalCount", description="Cantidad total de elementos")
    has_previous_page: bool = Field(alias="hasPreviousPage", description="Indica si hay una página anterior")
    has_next_page: bool = Field(alias="hasNextPage", description="Indica si hay una página siguiente")


class ValidationFailure(BaseModel):
    """Modelo para errores de validación."""
    propertyName: str
    errorMessage: str
    attemptedValue: Optional[Any] = None
    customState: Optional[Any] = None
    severity: Optional[int] = None
    errorCode: Optional[str] = None
    formattedMessagePlaceholderValues: Optional[dict] = None


class BaseDto(BaseModel):
    """Modelo base para DTOs."""
    id: Optional[str] = Field(default=None, alias="id")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")
    
    model_config = ConfigDict(populate_by_name=True)

class CatalogDto(BaseDto):
    """Modelo para catálogos."""
    description: str = Field(alias="description")

    model_config = ConfigDict(populate_by_name=True)


class FiscalApiSettings(BaseModel):
    """
    Objeto que contiene la configuración necesaria para interactuar con Fiscalapi.
    """
    api_url: str = Field(..., description="URL base de la api.")
    api_key: str = Field(..., description="Api Key")
    tenant: str = Field(..., description="Tenant Key.")
    api_version: str = Field("v4", description="Versión de la api.")
    time_zone: str = Field("America/Mexico_City", description="Zona horaria ")
    debug: bool = Field(False, description="Indica si se debe imprimir el payload request y response.")

    class Config:
        title = "FiscalApi Settings"
        description = "Configuración para Fiscalapi"