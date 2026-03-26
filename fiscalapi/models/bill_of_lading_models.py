"""Modelos de Carta Porte (Bill of Lading) para complemento de factura CFDI 4.0."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ===== Domicilio =====

class Domicilio(BaseModel):
    """Domicilio asociado a una ubicación o figura de transporte."""
    calle: Optional[str] = Field(default=None, alias="calle")
    numero_exterior: Optional[str] = Field(default=None, alias="numeroExterior")
    numero_interior: Optional[str] = Field(default=None, alias="numeroInterior")
    colonia_id: Optional[str] = Field(default=None, alias="coloniaId")
    localidad_id: Optional[str] = Field(default=None, alias="localidadId")
    referencia: Optional[str] = Field(default=None, alias="referencia")
    municipio_id: Optional[str] = Field(default=None, alias="municipioId")
    estado_id: Optional[str] = Field(default=None, alias="estadoId")
    pais_id: Optional[str] = Field(default=None, alias="paisId")
    codigo_postal_id: Optional[str] = Field(default=None, alias="codigoPostalId")

    model_config = ConfigDict(populate_by_name=True)


# ===== Regimen Aduanero =====

class RegimenAduanero(BaseModel):
    """Régimen aduanero aplicable al transporte internacional."""
    regimen_aduanero_id: Optional[str] = Field(default=None, alias="regimenAduaneroId")

    model_config = ConfigDict(populate_by_name=True)


# ===== Ubicacion =====

class Ubicacion(BaseModel):
    """Ubicación de origen o destino de la mercancía."""
    tipo_ubicacion: Optional[str] = Field(default=None, alias="tipoUbicacion")
    id_ubicacion: Optional[str] = Field(default=None, alias="idUbicacion")
    rfc_remitente_destinatario: Optional[str] = Field(default=None, alias="rfcRemitenteDestinatario")
    num_reg_id_trib: Optional[str] = Field(default=None, alias="numRegIdTrib")
    residencia_fiscal_id: Optional[str] = Field(default=None, alias="residenciaFiscalId")
    nombre_remitente_destinatario: Optional[str] = Field(default=None, alias="nombreRemitenteDestinatario")
    num_estacion_id: Optional[str] = Field(default=None, alias="numEstacionId")
    nombre_estacion: Optional[str] = Field(default=None, alias="nombreEstacion")
    navegacion_trafico_id: Optional[str] = Field(default=None, alias="navegacionTraficoId")
    tipo_estacion_id: Optional[str] = Field(default=None, alias="tipoEstacionId")
    fecha_hora_salida_llegada: Optional[str] = Field(default=None, alias="fechaHoraSalidaLlegada")
    distancia_recorrida: Optional[Decimal] = Field(default=None, alias="distanciaRecorrida")
    domicilio: Optional[Domicilio] = Field(default=None, alias="domicilio")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


# ===== Mercancia =====

class DocumentoAduanero(BaseModel):
    """Documento aduanero asociado a una mercancía."""
    tipo_documento_id: Optional[str] = Field(default=None, alias="tipoDocumentoId")
    num_pedimento: Optional[str] = Field(default=None, alias="numPedimento")
    rfc_impo: Optional[str] = Field(default=None, alias="rfcImpo")

    model_config = ConfigDict(populate_by_name=True)


class CantidadTransporta(BaseModel):
    """Cantidad transportada entre ubicaciones."""
    cantidad: Decimal = Field(default=..., alias="cantidad")
    id_origen: Optional[str] = Field(default=None, alias="idOrigen")
    id_destino: Optional[str] = Field(default=None, alias="idDestino")
    cves_transporte_id: Optional[str] = Field(default=None, alias="cvesTransporteId")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class DetalleMercancia(BaseModel):
    """Detalle adicional de la mercancía transportada."""
    unidad_peso_merc_id: Optional[str] = Field(default=None, alias="unidadPesoMercId")
    peso_bruto: Decimal = Field(default=..., alias="pesoBruto")
    peso_neto: Decimal = Field(default=..., alias="pesoNeto")
    peso_tara: Decimal = Field(default=..., alias="pesoTara")
    num_piezas: Optional[int] = Field(default=None, alias="numPiezas")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class Mercancia(BaseModel):
    """Mercancía transportada en la carta porte."""
    bienes_transp_id: Optional[str] = Field(default=None, alias="bienesTranspId")
    descripcion: Optional[str] = Field(default=None, alias="descripcion")
    cantidad: Decimal = Field(default=..., alias="cantidad")
    clave_unidad_id: Optional[str] = Field(default=None, alias="claveUnidadId")
    material_peligroso_id: Optional[str] = Field(default=None, alias="materialPeligrosoId")
    denominacion_generica_prod: Optional[str] = Field(default=None, alias="denominacionGenericaProd")
    denominacion_distintiva_prod: Optional[str] = Field(default=None, alias="denominacionDistintivaProd")
    fabricante: Optional[str] = Field(default=None, alias="fabricante")
    fecha_caducidad: Optional[str] = Field(default=None, alias="fechaCaducidad")
    lote_medicamento: Optional[str] = Field(default=None, alias="loteMedicamento")
    forma_farmaceutica_id: Optional[str] = Field(default=None, alias="formaFarmaceuticaId")
    condiciones_esp_transp_id: Optional[str] = Field(default=None, alias="condicionesEspTranspId")
    registro_sanitario_folio_autorizacion: Optional[str] = Field(default=None, alias="registroSanitarioFolioAutorizacion")
    peso_en_kg: Decimal = Field(default=..., alias="pesoEnKg")
    fraccion_arancelaria_id: Optional[str] = Field(default=None, alias="fraccionArancelariaId")
    tipo_materia_id: Optional[str] = Field(default=None, alias="tipoMateriaId")
    descripcion_materia: Optional[str] = Field(default=None, alias="descripcionMateria")
    valor_mercancia: Optional[Decimal] = Field(default=None, alias="valorMercancia")
    moneda_id: Optional[str] = Field(default=None, alias="monedaId")
    documentacion_aduanera: Optional[list[DocumentoAduanero]] = Field(default=None, alias="documentacionAduanera")
    cantidad_transporta: Optional[list[CantidadTransporta]] = Field(default=None, alias="cantidadTransporta")
    detalle_mercancia: Optional[DetalleMercancia] = Field(default=None, alias="detalleMercancia")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


# ===== Autotransporte =====

class Remolque(BaseModel):
    """Remolque del autotransporte."""
    sub_tipo_rem_id: Optional[str] = Field(default=None, alias="subTipoRemId")
    placa: Optional[str] = Field(default=None, alias="placa")

    model_config = ConfigDict(populate_by_name=True)


class Autotransporte(BaseModel):
    """Datos del autotransporte federal."""
    perm_sct_id: Optional[str] = Field(default=None, alias="permSCTId")
    num_permiso_sct: Optional[str] = Field(default=None, alias="numPermisoSCT")
    config_vehicular_id: Optional[str] = Field(default=None, alias="configVehicularId")
    peso_bruto_vehicular: Decimal = Field(default=..., alias="pesoBrutoVehicular")
    placa_vm: Optional[str] = Field(default=None, alias="placaVM")
    anio_modelo_vm: int = Field(default=..., alias="anioModeloVM")
    asegura_resp_civil: Optional[str] = Field(default=None, alias="aseguraRespCivil")
    poliza_resp_civil: Optional[str] = Field(default=None, alias="polizaRespCivil")
    remolques: Optional[list[Remolque]] = Field(default=None, alias="remolques")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


# ===== Transporte Maritimo =====

class RemolqueCCP(BaseModel):
    """Remolque del contenedor marítimo."""
    sub_tipo_rem_ccp_id: Optional[str] = Field(default=None, alias="subTipoRemCCPId")
    placa_ccp: Optional[str] = Field(default=None, alias="placaCCP")

    model_config = ConfigDict(populate_by_name=True)


class ContenedorMaritimo(BaseModel):
    """Contenedor para transporte marítimo."""
    matricula_contenedor: Optional[str] = Field(default=None, alias="matriculaContenedor")
    tipo_contenedor_id: Optional[str] = Field(default=None, alias="tipoContenedorId")
    num_precinto: Optional[str] = Field(default=None, alias="numPrecinto")
    peso_contenedor_vacio: Optional[Decimal] = Field(default=None, alias="pesoContenedorVacio")
    peso_neto_mercancia: Optional[Decimal] = Field(default=None, alias="pesoNetoMercancia")
    id_ccp_relacionado: Optional[str] = Field(default=None, alias="idCCPRelacionado")
    placa_vm_ccp: Optional[str] = Field(default=None, alias="placaVMCCP")
    fecha_certificacion_ccp: Optional[str] = Field(default=None, alias="fechaCertificacionCCP")
    remolques_ccp: Optional[list[RemolqueCCP]] = Field(default=None, alias="remolquesCCP")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class TransporteMaritimo(BaseModel):
    """Datos del transporte marítimo."""
    perm_sct_id: Optional[str] = Field(default=None, alias="permSCTId")
    num_permiso_sct: Optional[str] = Field(default=None, alias="numPermisoSCT")
    config_maritima_id: Optional[str] = Field(default=None, alias="configMaritimaId")
    nombre_aseg: Optional[str] = Field(default=None, alias="nombreAseg")
    num_poliza_seguro: Optional[str] = Field(default=None, alias="numPolizaSeguro")
    tipo_embarcacion_id: Optional[str] = Field(default=None, alias="tipoEmbarcacionId")
    matricula: Optional[str] = Field(default=None, alias="matricula")
    numero_omi: Optional[str] = Field(default=None, alias="numeroOMI")
    anio_embarcacion: Optional[int] = Field(default=None, alias="anioEmbarcacion")
    nombre_embarc: Optional[str] = Field(default=None, alias="nombreEmbarc")
    nacionalidad_embarc_id: Optional[str] = Field(default=None, alias="nacionalidadEmbarcId")
    unidades_de_arq_bruto: Optional[Decimal] = Field(default=None, alias="unidadesDeArqBruto")
    tipo_carga_id: Optional[str] = Field(default=None, alias="tipoCargaId")
    eslora: Optional[Decimal] = Field(default=None, alias="eslora")
    manga: Optional[Decimal] = Field(default=None, alias="manga")
    calado: Optional[Decimal] = Field(default=None, alias="calado")
    puntal: Optional[Decimal] = Field(default=None, alias="puntal")
    linea_naviera: Optional[str] = Field(default=None, alias="lineaNaviera")
    nombre_agente_naviero: Optional[str] = Field(default=None, alias="nombreAgenteNaviero")
    num_cert_itc: Optional[str] = Field(default=None, alias="numCertITC")
    nombre_embar_cargador: Optional[str] = Field(default=None, alias="nombreEmbarCargador")
    nombre_agente: Optional[str] = Field(default=None, alias="nombreAgente")
    num_autorizacion_naviero_id: Optional[str] = Field(default=None, alias="numAutorizacionNavieroId")
    num_viaje: Optional[str] = Field(default=None, alias="numViaje")
    num_conoc_embarc: Optional[str] = Field(default=None, alias="numConocEmbarc")
    permiso_temp_navegacion: Optional[str] = Field(default=None, alias="permisoTempNavegacion")
    contenedores: Optional[list[ContenedorMaritimo]] = Field(default=None, alias="contenedores")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


# ===== Transporte Aereo =====

class TransporteAereo(BaseModel):
    """Datos del transporte aéreo."""
    perm_sct_id: Optional[str] = Field(default=None, alias="permSCTId")
    num_permiso_sct: Optional[str] = Field(default=None, alias="numPermisoSCT")
    matricula_aeronave: Optional[str] = Field(default=None, alias="matriculaAeronave")
    nombre_aseg: Optional[str] = Field(default=None, alias="nombreAseg")
    num_poliza_seguro: Optional[str] = Field(default=None, alias="numPolizaSeguro")
    numero_guia: Optional[str] = Field(default=None, alias="numeroGuia")
    lugar_contrato: Optional[str] = Field(default=None, alias="lugarContrato")
    codigo_transportista_id: Optional[str] = Field(default=None, alias="codigoTransportistaId")
    rfc_embarcador: Optional[str] = Field(default=None, alias="rfcEmbarcador")
    nombre_embarcador: Optional[str] = Field(default=None, alias="nombreEmbarcador")
    rfc_transportista: Optional[str] = Field(default=None, alias="rfcTransportista")

    model_config = ConfigDict(populate_by_name=True)


# ===== Transporte Ferroviario =====

class DerechoDePaso(BaseModel):
    """Derecho de paso del transporte ferroviario."""
    tipo_derecho_de_paso_id: Optional[str] = Field(default=None, alias="tipoDerechoDePasoId")
    kilometraje_pagado: Decimal = Field(default=..., alias="kilometrajePagado")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class ContenedorFerroviario(BaseModel):
    """Contenedor para transporte ferroviario."""
    tipo_contenedor_id: Optional[str] = Field(default=None, alias="tipoContenedorId")
    peso_contenedor_vacio: Optional[Decimal] = Field(default=None, alias="pesoContenedorVacio")
    peso_neto_mercancia: Optional[Decimal] = Field(default=None, alias="pesoNetoMercancia")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class Carro(BaseModel):
    """Carro del transporte ferroviario."""
    tipo_carro_id: Optional[str] = Field(default=None, alias="tipoCarroId")
    matricula_carro: Optional[str] = Field(default=None, alias="matriculaCarro")
    guia_carro: Optional[str] = Field(default=None, alias="guiaCarro")
    toneladas_netas_carro: Decimal = Field(default=..., alias="toneladasNetasCarro")
    contenedores: Optional[list[ContenedorFerroviario]] = Field(default=None, alias="contenedores")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class TransporteFerroviario(BaseModel):
    """Datos del transporte ferroviario."""
    tipo_de_servicio_id: Optional[str] = Field(default=None, alias="tipoDeServicioId")
    tipo_de_trafico_id: Optional[str] = Field(default=None, alias="tipoDeTraficoId")
    nombre_aseg: Optional[str] = Field(default=None, alias="nombreAseg")
    num_poliza_seguro: Optional[str] = Field(default=None, alias="numPolizaSeguro")
    derechos_de_paso: Optional[list[DerechoDePaso]] = Field(default=None, alias="derechosDePaso")
    carros: Optional[list[Carro]] = Field(default=None, alias="carros")

    model_config = ConfigDict(populate_by_name=True)


# ===== Tipo Figura =====

class ParteTransporte(BaseModel):
    """Parte de transporte asociada a una figura."""
    parte_transporte_id: Optional[str] = Field(default=None, alias="parteTransporteId")

    model_config = ConfigDict(populate_by_name=True)


class TipoFigura(BaseModel):
    """Figura de transporte (operador, propietario, arrendatario, notificado)."""
    tipo_figura_id: Optional[str] = Field(default=None, alias="tipoFiguraId")
    rfc_figura: Optional[str] = Field(default=None, alias="rfcFigura")
    num_licencia: Optional[str] = Field(default=None, alias="numLicencia")
    nombre_figura: Optional[str] = Field(default=None, alias="nombreFigura")
    partes_transporte: Optional[list[ParteTransporte]] = Field(default=None, alias="partesTransporte")
    domicilio: Optional[Domicilio] = Field(default=None, alias="domicilio")

    model_config = ConfigDict(populate_by_name=True)


# ===== Carta Porte =====

class LadingComplement(BaseModel):
    """Complemento Carta Porte para transporte de mercancías."""
    transp_internac_id: Optional[str] = Field(default=None, alias="transpInternacId")
    entrada_salida_merc_id: Optional[str] = Field(default=None, alias="entradaSalidaMercId")
    pais_origen_destino_id: Optional[str] = Field(default=None, alias="paisOrigenDestinoId")
    via_entrada_salida_id: Optional[str] = Field(default=None, alias="viaEntradaSalidaId")
    total_dist_rec: Optional[Decimal] = Field(default=None, alias="totalDistRec")
    peso_neto_total: Optional[Decimal] = Field(default=None, alias="pesoNetoTotal")
    registro_istmo_id: Optional[str] = Field(default=None, alias="registroISTMOId")
    ubicacion_polo_origen_id: Optional[str] = Field(default=None, alias="ubicacionPoloOrigenId")
    ubicacion_polo_destino_id: Optional[str] = Field(default=None, alias="ubicacionPoloDestinoId")
    unidad_peso_id: Optional[str] = Field(default=None, alias="unidadPesoId")
    logistica_inversa_recoleccion_devolucion_id: Optional[str] = Field(default=None, alias="logisticaInversaRecoleccionDevolucionId")
    regimen_aduaneros: Optional[list[RegimenAduanero]] = Field(default=None, alias="regimenAduaneros")
    ubicaciones: Optional[list[Ubicacion]] = Field(default=None, alias="ubicaciones")
    mercancias: Optional[list[Mercancia]] = Field(default=None, alias="mercancias")
    autotransporte: Optional[Autotransporte] = Field(default=None, alias="autotransporte")
    transporte_maritimo: Optional[TransporteMaritimo] = Field(default=None, alias="transporteMaritimo")
    transporte_aereo: Optional[TransporteAereo] = Field(default=None, alias="transporteAereo")
    transporte_ferroviario: Optional[TransporteFerroviario] = Field(default=None, alias="transporteFerroviario")
    tipos_figura: Optional[list[TipoFigura]] = Field(default=None, alias="tiposFigura")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})
