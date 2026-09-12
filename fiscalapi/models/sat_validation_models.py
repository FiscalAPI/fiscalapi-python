"""Modelos para validaciones SAT (endpoints /api/v4/sat-validations).

Cada tipo de validación solicitado consume un crédito de validación. El cobro es todo o nada y ocurre
antes de ejecutar: si el saldo no alcanza para todos, no se ejecuta ninguno y la API responde 403.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SatValidationTypeIds(str, Enum):
    """Ids de los tipos de validación SAT, en el orden del catálogo."""

    XML_STRUCTURE = "sat.xml.structure"
    CERTIFICATE_VALIDITY = "sat.certificate.validity"
    CFDI_SELLO = "sat.cfdi.sello"
    TFD_SELLO = "sat.tfd.sello"
    CFDI_STATUS = "sat.cfdi.status"
    BLACKLIST_69B = "sat.blacklist.69b"
    BLACKLIST_69B_BIS = "sat.blacklist.69bbis"


class SatValidationStatusIds(str, Enum):
    """Ids de los estatus de validación SAT.

    Los estatus que puede tomar cada tipo se consultan con ``get_statuses(validation_type_id)``: no todos
    los estatus aplican a todos los tipos.
    """

    VALIDO = "Valido"
    INVALIDO = "Invalido"
    VIGENTE = "Vigente"
    EXPIRADO = "Expirado"
    NO_VIGENTE_AUN = "NoVigenteAun"
    CANCELADO = "Cancelado"
    NO_ENCONTRADO = "NoEncontrado"
    NO_LISTADO = "NoListado"
    PRESUNTO = "Presunto"
    DESVIRTUADO = "Desvirtuado"
    DEFINITIVO = "Definitivo"
    SENTENCIA_FAVORABLE = "SentenciaFavorable"
    NO_DISPONIBLE = "NoDisponible"
    OMITIDO = "Omitido"


class SatValidationRequest(BaseModel):
    """Petición para ejecutar validaciones SAT (POST /api/v4/sat-validations).

    Envía ``xml`` o ``tin``, nunca ambos y nunca ninguno: con ``xml`` puedes solicitar cualquier tipo de
    validación; con ``tin`` únicamente listas negras (``sat.blacklist.69b`` y ``sat.blacklist.69bbis``).
    """

    xml: Optional[str] = Field(default=None, alias="xml", description="CFDI timbrado completo codificado en base64. Excluyente con tin.")
    tin: Optional[str] = Field(default=None, alias="tin", description="RFC a consultar en listas negras. Excluyente con xml.")
    validation_types: list[str] = Field(default=..., alias="validationTypes", description="Ids de los tipos de validación a ejecutar (ver SatValidationTypeIds). Sin vacíos ni duplicados.")

    model_config = ConfigDict(populate_by_name=True)


class SatValidationType(BaseModel):
    """Tipo de validación SAT del catálogo."""

    id: Optional[SatValidationTypeIds] = Field(default=None, alias="id", description="Id del tipo de validación.")
    description: Optional[str] = Field(default=None, alias="description", description="Descripción de lo que verifica el tipo.")

    model_config = ConfigDict(populate_by_name=True)


class SatValidationTypeStatus(BaseModel):
    """Estatus que un tipo de validación puede tomar al ejecutarse."""

    id: Optional[SatValidationStatusIds] = Field(default=None, alias="id", description="Id del estatus.")
    description: Optional[str] = Field(default=None, alias="description", description="Descripción del estatus según el catálogo.")

    model_config = ConfigDict(populate_by_name=True)


class SatValidationStatus(BaseModel):
    """Estatus obtenido al ejecutar una validación SAT."""

    id: Optional[SatValidationStatusIds] = Field(default=None, alias="id", description="Id del estatus obtenido.")
    description: Optional[str] = Field(default=None, alias="description", description="Descripción del estatus según el catálogo.")
    details: Optional[str] = Field(default=None, alias="details", description="Hechos del caso en texto libre (RFC y corte del listado, número de certificado, estado en el SAT). Puede ser nulo.")

    model_config = ConfigDict(populate_by_name=True)


class SatValidationResult(BaseModel):
    """Un tipo de validación ejecutado con el estatus obtenido y su veredicto."""

    type: Optional[SatValidationType] = Field(default=None, alias="type", description="Tipo de validación evaluado.")
    status: Optional[SatValidationStatus] = Field(default=None, alias="status", description="Estatus obtenido.")
    passed: Optional[bool] = Field(default=None, alias="passed", description="Verdadero cuando el estatus se considera aprobado para ese tipo.")

    model_config = ConfigDict(populate_by_name=True)
