"""Modelos del complemento Comercio Exterior para CFDI 4.0."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ===== Domicilios =====

class ComercioExteriorEmisorDomicilio(BaseModel):
    """Domicilio del emisor del complemento Comercio Exterior."""
    calle: str = Field(default=..., alias="calle")
    numero_exterior: Optional[str] = Field(default=None, alias="numeroExterior")
    numero_interior: Optional[str] = Field(default=None, alias="numeroInterior")
    colonia_id: Optional[str] = Field(default=None, alias="coloniaId")
    localidad_id: Optional[str] = Field(default=None, alias="localidadId")
    referencia: Optional[str] = Field(default=None, alias="referencia")
    municipio_id: Optional[str] = Field(default=None, alias="municipioId")
    estado_id: str = Field(default=..., alias="estadoId")
    pais_id: str = Field(default=..., alias="paisId")
    codigo_postal_id: str = Field(default=..., alias="codigoPostalId")

    model_config = ConfigDict(populate_by_name=True)


class ComercioExteriorReceptorDomicilio(BaseModel):
    """Domicilio del receptor del complemento Comercio Exterior."""
    calle: str = Field(default=..., alias="calle")
    numero_exterior: Optional[str] = Field(default=None, alias="numeroExterior")
    numero_interior: Optional[str] = Field(default=None, alias="numeroInterior")
    colonia: Optional[str] = Field(default=None, alias="colonia")
    localidad: Optional[str] = Field(default=None, alias="localidad")
    referencia: Optional[str] = Field(default=None, alias="referencia")
    municipio: Optional[str] = Field(default=None, alias="municipio")
    estado: str = Field(default=..., alias="estado")
    pais_id: str = Field(default=..., alias="paisId")
    codigo_postal: str = Field(default=..., alias="codigoPostal")

    model_config = ConfigDict(populate_by_name=True)


class ComercioExteriorDestinatarioDomicilio(BaseModel):
    """Domicilio de un destinatario del complemento Comercio Exterior."""
    calle: str = Field(default=..., alias="calle")
    numero_exterior: Optional[str] = Field(default=None, alias="numeroExterior")
    numero_interior: Optional[str] = Field(default=None, alias="numeroInterior")
    colonia: Optional[str] = Field(default=None, alias="colonia")
    localidad: Optional[str] = Field(default=None, alias="localidad")
    referencia: Optional[str] = Field(default=None, alias="referencia")
    municipio: Optional[str] = Field(default=None, alias="municipio")
    estado: str = Field(default=..., alias="estado")
    pais_id: str = Field(default=..., alias="paisId")
    codigo_postal: str = Field(default=..., alias="codigoPostal")

    model_config = ConfigDict(populate_by_name=True)


# ===== Emisor =====

class ComercioExteriorEmisor(BaseModel):
    """Emisor del complemento Comercio Exterior."""
    curp: Optional[str] = Field(default=None, alias="curp")
    domicilio: ComercioExteriorEmisorDomicilio = Field(default=..., alias="domicilio")

    model_config = ConfigDict(populate_by_name=True)


# ===== Propietario =====

class ComercioExteriorPropietario(BaseModel):
    """Propietario de las mercancías exportadas."""
    num_reg_id_trib: str = Field(default=..., alias="numRegIdTrib")
    residencia_fiscal_id: str = Field(default=..., alias="residenciaFiscalId")

    model_config = ConfigDict(populate_by_name=True)


# ===== Receptor =====

class ComercioExteriorReceptor(BaseModel):
    """Receptor del complemento Comercio Exterior."""
    num_reg_id_trib: Optional[str] = Field(default=None, alias="numRegIdTrib")
    domicilio: Optional[ComercioExteriorReceptorDomicilio] = Field(default=None, alias="domicilio")

    model_config = ConfigDict(populate_by_name=True)


# ===== Destinatario =====

class ComercioExteriorDestinatario(BaseModel):
    """Destinatario de las mercancías exportadas."""
    num_reg_id_trib: Optional[str] = Field(default=None, alias="numRegIdTrib")
    nombre: Optional[str] = Field(default=None, alias="nombre")
    domicilios: list[ComercioExteriorDestinatarioDomicilio] = Field(default_factory=list, alias="domicilios")

    model_config = ConfigDict(populate_by_name=True)


# ===== Mercancías =====

class ComercioExteriorMercanciaDescripcionEspecifica(BaseModel):
    """Descripción específica de una mercancía del complemento Comercio Exterior."""
    marca: str = Field(default=..., alias="marca")
    modelo: Optional[str] = Field(default=None, alias="modelo")
    sub_modelo: Optional[str] = Field(default=None, alias="subModelo")
    numero_serie: Optional[str] = Field(default=None, alias="numeroSerie")

    model_config = ConfigDict(populate_by_name=True)


class ComercioExteriorMercancia(BaseModel):
    """Mercancía del complemento Comercio Exterior."""
    no_identificacion: str = Field(default=..., alias="noIdentificacion")
    fraccion_arancelaria_id: Optional[str] = Field(default=None, alias="fraccionArancelariaId")
    cantidad_aduana: Optional[Decimal] = Field(default=None, alias="cantidadAduana")
    unidad_aduana_id: Optional[str] = Field(default=None, alias="unidadAduanaId")
    valor_unitario_aduana: Optional[Decimal] = Field(default=None, alias="valorUnitarioAduana")
    valor_dolares: Decimal = Field(default=..., alias="valorDolares")
    descripciones_especificas: Optional[list[ComercioExteriorMercanciaDescripcionEspecifica]] = Field(
        default=None, alias="descripcionesEspecificas"
    )

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


# ===== Comercio Exterior =====

class ComercioExteriorComplement(BaseModel):
    """Complemento Comercio Exterior para exportación de mercancías en CFDI 4.0."""
    motivo_traslado_id: Optional[str] = Field(default=None, alias="motivoTrasladoId")
    clave_de_pedimento_id: str = Field(default=..., alias="claveDePedimentoId")
    certificado_origen: int = Field(default=..., alias="certificadoOrigen")
    num_certificado_origen: Optional[str] = Field(default=None, alias="numCertificadoOrigen")
    numero_exportador_confiable: Optional[str] = Field(default=None, alias="numeroExportadorConfiable")
    incoterm_id: Optional[str] = Field(default=None, alias="incotermId")
    observaciones: Optional[str] = Field(default=None, alias="observaciones")
    tipo_cambio_usd: Decimal = Field(default=..., alias="tipoCambioUSD")
    emisor: Optional[ComercioExteriorEmisor] = Field(default=None, alias="emisor")
    receptor: Optional[ComercioExteriorReceptor] = Field(default=None, alias="receptor")
    propietarios: Optional[list[ComercioExteriorPropietario]] = Field(default=None, alias="propietarios")
    destinatarios: Optional[list[ComercioExteriorDestinatario]] = Field(default=None, alias="destinatarios")
    mercancias: list[ComercioExteriorMercancia] = Field(default_factory=list, alias="mercancias")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})
