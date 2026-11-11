from datetime import datetime
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    succeeded: bool = Field(default=..., alias="succeeded")
    message: Optional[str] = Field(default=None, alias="message")
    details: Optional[str] = Field(default=None, alias="details")
    data: Optional[T] = Field(default=None, alias="data")
    http_status_code: Optional[int] = Field(default=None, alias="httpStatusCode")
    trace_identifier: Optional[str] = Field(default=None, alias="traceIdentifier", description="Identificador de la petición en los registros de FiscalAPI. Viene en los errores (por ejemplo, un 500 o un 502): inclúyalo al escribir a soporte@fiscalapi.com.")
    error_data: Optional[Any] = Field(default=None, alias="errorData", description="El data crudo de una respuesta de error (dict o lista tal cual), por ejemplo existingTicketId en el 409 de tickets.create o expectedTotal y computedTotal en su 422. None en las respuestas exitosas y en los errores sin data; data no cambia (en un error sigue en None).")

    model_config = ConfigDict(populate_by_name=True)


class PagedList(BaseModel, Generic[T]):
    """Modelo para la estructura de la lista paginada."""
    items: list[T] = Field(default_factory=list, alias="items", description="Lista de elementos paginados")
    page_number: int = Field(default=..., alias="pageNumber", description="Número de página actual")
    total_pages: int = Field(default=..., alias="totalPages", description="Cantidad total de páginas")
    total_count: int = Field(default=..., alias="totalCount", description="Cantidad total de elementos")
    has_previous_page: bool = Field(default=..., alias="hasPreviousPage", description="Indica si hay una página anterior")
    has_next_page: bool = Field(default=..., alias="hasNextPage", description="Indica si hay una página siguiente")

    model_config = ConfigDict(populate_by_name=True)


class PagedListFilters(BaseModel):
    """Página de una lista (``get_list`` de facturas, personas y productos) y base de sus filtros. Cada filtro aplica solo
    si se asigna; los que quedan en None no se envían."""

    page_number: Optional[int] = Field(default=None, alias="pageNumber", description="Página, desde 1. Sin ella, el API devuelve la primera.")
    page_size: Optional[int] = Field(default=None, alias="pageSize", description="Tamaño de página (1 a 50). Sin él, el API usa su tamaño por omisión.")

    model_config = ConfigDict(populate_by_name=True)

    def to_query_params(self) -> list[tuple[str, str]]:
        """Los filtros asignados como pares de la query string, con los nombres camelCase del API y la página al final,
        en el orden del contrato."""
        filters = self.model_dump(mode="json", by_alias=True, exclude={"page_number", "page_size"})
        page = {"pageNumber": self.page_number, "pageSize": self.page_size}
        return [(key, str(value)) for key, value in [*filters.items(), *page.items()] if value is not None]


class ValidationFailure(BaseModel):
    """Modelo para errores de validación."""
    property_name: str = Field(alias="propertyName")
    error_message: str = Field(alias="errorMessage")
    attempted_value: Optional[Any] = Field(default=None, alias="attemptedValue", description="Valor recibido. El de un secreto (contraseñas, códigos, tokens, archivos y contraseñas de CSD/FIEL) llega como \"[masked: n]\", o \"[masked]\" si es un objeto o lista que lo contiene.")

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