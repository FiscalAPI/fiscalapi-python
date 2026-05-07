"""Modelos de Carta Porte (Bill of Lading) para complemento de factura CFDI 4.0."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ===== Domicilio =====

class UbicacionDomicilio(BaseModel):
    """Domicilio de una ubicación de origen o destino."""
    calle: Optional[str] = Field(default=None, alias="calle")
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


class TipoFiguraDomicilio(BaseModel):
    """Domicilio de una figura de transporte."""
    calle: Optional[str] = Field(default=None, alias="calle")
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


# ===== Regimen Aduanero =====

class RegimenAduanero(BaseModel):
    """Régimen aduanero aplicable al transporte internacional."""
    regimen_aduanero_id: str = Field(default=..., alias="regimenAduaneroId")

    model_config = ConfigDict(populate_by_name=True)


# ===== Ubicacion =====

class Ubicacion(BaseModel):
    """Ubicación de origen o destino de la mercancía."""
    tipo_ubicacion: str = Field(default=..., alias="tipoUbicacion")
    id_ubicacion: Optional[str] = Field(default=None, alias="idUbicacion")
    rfc_remitente_destinatario: str = Field(default=..., alias="rfcRemitenteDestinatario")
    num_reg_id_trib: Optional[str] = Field(default=None, alias="numRegIdTrib")
    residencia_fiscal_id: Optional[str] = Field(default=None, alias="residenciaFiscalId")
    nombre_remitente_destinatario: Optional[str] = Field(default=None, alias="nombreRemitenteDestinatario")
    num_estacion_id: Optional[str] = Field(default=None, alias="numEstacionId")
    nombre_estacion: Optional[str] = Field(default=None, alias="nombreEstacion")
    navegacion_trafico_id: Optional[str] = Field(default=None, alias="navegacionTraficoId")
    tipo_estacion_id: Optional[str] = Field(default=None, alias="tipoEstacionId")
    fecha_hora_salida_llegada: datetime = Field(default=..., alias="fechaHoraSalidaLlegada")
    distancia_recorrida: Optional[Decimal] = Field(default=None, alias="distanciaRecorrida")
    domicilio: Optional[UbicacionDomicilio] = Field(default=None, alias="domicilio")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str, datetime: lambda v: v.isoformat()})


# ===== Mercancia =====

class DocumentoAduanero(BaseModel):
    """Documento aduanero asociado a una mercancía."""
    tipo_documento_id: str = Field(default=..., alias="tipoDocumentoId")
    num_pedimento: Optional[str] = Field(default=None, alias="numPedimento")
    ident_doc_aduanero: Optional[str] = Field(default=None, alias="identDocAduanero")
    rfc_impo: Optional[str] = Field(default=None, alias="rfcImpo")

    model_config = ConfigDict(populate_by_name=True)


class GuiaIdentificacion(BaseModel):
    """Guía de identificación asociada a una mercancía."""
    numero_guia_identificacion: str = Field(default=..., alias="numeroGuiaIdentificacion")
    descrip_guia_identificacion: str = Field(default=..., alias="descripGuiaIdentificacion")
    peso_guia_identificacion: Decimal = Field(default=..., alias="pesoGuiaIdentificacion")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class CantidadTransporta(BaseModel):
    """Cantidad transportada entre ubicaciones."""
    cantidad: Decimal = Field(default=..., alias="cantidad")
    id_origen: str = Field(default=..., alias="idOrigen")
    id_destino: str = Field(default=..., alias="idDestino")
    cves_transporte_id: Optional[str] = Field(default=None, alias="cvesTransporteId")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class DetalleMercancia(BaseModel):
    """Detalle adicional de la mercancía transportada."""
    unidad_peso_merc_id: str = Field(default=..., alias="unidadPesoMercId")
    peso_bruto: Decimal = Field(default=..., alias="pesoBruto")
    peso_neto: Decimal = Field(default=..., alias="pesoNeto")
    peso_tara: Decimal = Field(default=..., alias="pesoTara")
    num_piezas: Optional[int] = Field(default=None, alias="numPiezas")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class Mercancia(BaseModel):
    """Mercancía transportada en la carta porte."""
    bienes_transp_id: str = Field(default=..., alias="bienesTranspId")
    clave_stcc_id: Optional[str] = Field(default=None, alias="claveSTCCId")
    descripcion: str = Field(default=..., alias="descripcion")
    cantidad: Decimal = Field(default=..., alias="cantidad")
    clave_unidad_id: str = Field(default=..., alias="claveUnidadId")
    unidad: Optional[str] = Field(default=None, alias="unidad")
    dimensiones: Optional[str] = Field(default=None, alias="dimensiones")
    material_peligroso_id: Optional[str] = Field(default=None, alias="materialPeligrosoId")
    cve_material_peligroso_id: Optional[str] = Field(default=None, alias="cveMaterialPeligrosoId")
    embalaje_id: Optional[str] = Field(default=None, alias="embalajeId")
    descrip_embalaje: Optional[str] = Field(default=None, alias="descripEmbalaje")
    sector_cofepris_id: Optional[str] = Field(default=None, alias="sectorCOFEPRISId")
    nombre_ingrediente_activo: Optional[str] = Field(default=None, alias="nombreIngredienteActivo")
    nom_quimico: Optional[str] = Field(default=None, alias="nomQuimico")
    denominacion_generica_prod: Optional[str] = Field(default=None, alias="denominacionGenericaProd")
    denominacion_distintiva_prod: Optional[str] = Field(default=None, alias="denominacionDistintivaProd")
    fabricante: Optional[str] = Field(default=None, alias="fabricante")
    fecha_caducidad: Optional[datetime] = Field(default=None, alias="fechaCaducidad")
    lote_medicamento: Optional[str] = Field(default=None, alias="loteMedicamento")
    forma_farmaceutica_id: Optional[str] = Field(default=None, alias="formaFarmaceuticaId")
    condiciones_esp_transp_id: Optional[str] = Field(default=None, alias="condicionesEspTranspId")
    registro_sanitario_folio_autorizacion: Optional[str] = Field(default=None, alias="registroSanitarioFolioAutorizacion")
    permiso_importacion: Optional[str] = Field(default=None, alias="permisoImportacion")
    folio_impo_vucem: Optional[str] = Field(default=None, alias="folioImpoVUCEM")
    num_cas: Optional[str] = Field(default=None, alias="numCAS")
    razon_social_emp_imp: Optional[str] = Field(default=None, alias="razonSocialEmpImp")
    num_reg_san_plag_cofepris: Optional[str] = Field(default=None, alias="numRegSanPlagCOFEPRIS")
    datos_fabricante: Optional[str] = Field(default=None, alias="datosFabricante")
    datos_formulador: Optional[str] = Field(default=None, alias="datosFormulador")
    datos_maquilador: Optional[str] = Field(default=None, alias="datosMaquilador")
    uso_autorizado: Optional[str] = Field(default=None, alias="usoAutorizado")
    peso_en_kg: Decimal = Field(default=..., alias="pesoEnKg")
    valor_mercancia: Optional[Decimal] = Field(default=None, alias="valorMercancia")
    moneda_id: Optional[str] = Field(default=None, alias="monedaId")
    fraccion_arancelaria_id: Optional[str] = Field(default=None, alias="fraccionArancelariaId")
    uuid_comercio_ext: Optional[str] = Field(default=None, alias="uuidComercioExt")
    tipo_materia_id: Optional[str] = Field(default=None, alias="tipoMateriaId")
    descripcion_materia: Optional[str] = Field(default=None, alias="descripcionMateria")
    documentacion_aduanera: Optional[list[DocumentoAduanero]] = Field(default=None, alias="documentacionAduanera")
    guias_identificacion: Optional[list[GuiaIdentificacion]] = Field(default=None, alias="guiasIdentificacion")
    cantidad_transporta: Optional[list[CantidadTransporta]] = Field(default=None, alias="cantidadTransporta")
    detalle_mercancia: Optional[DetalleMercancia] = Field(default=None, alias="detalleMercancia")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str, datetime: lambda v: v.isoformat()})


# ===== Autotransporte =====

class Remolque(BaseModel):
    """Remolque del autotransporte."""
    sub_tipo_rem_id: str = Field(default=..., alias="subTipoRemId")
    placa: str = Field(default=..., alias="placa")

    model_config = ConfigDict(populate_by_name=True)


class Autotransporte(BaseModel):
    """Datos del autotransporte federal."""
    perm_sct_id: str = Field(default=..., alias="permSCTId")
    num_permiso_sct: str = Field(default=..., alias="numPermisoSCT")
    config_vehicular_id: str = Field(default=..., alias="configVehicularId")
    peso_bruto_vehicular: Decimal = Field(default=..., alias="pesoBrutoVehicular")
    placa_vm: str = Field(default=..., alias="placaVM")
    anio_modelo_vm: int = Field(default=..., alias="anioModeloVM")
    asegura_resp_civil: str = Field(default=..., alias="aseguraRespCivil")
    poliza_resp_civil: str = Field(default=..., alias="polizaRespCivil")
    asegura_med_ambiente: Optional[str] = Field(default=None, alias="aseguraMedAmbiente")
    poliza_med_ambiente: Optional[str] = Field(default=None, alias="polizaMedAmbiente")
    asegura_carga: Optional[str] = Field(default=None, alias="aseguraCarga")
    poliza_carga: Optional[str] = Field(default=None, alias="polizaCarga")
    prima_seguro: Optional[Decimal] = Field(default=None, alias="primaSeguro")
    remolques: Optional[list[Remolque]] = Field(default=None, alias="remolques")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


# ===== Transporte Maritimo =====

class RemolqueCCP(BaseModel):
    """Remolque del contenedor marítimo."""
    sub_tipo_rem_ccp_id: str = Field(default=..., alias="subTipoRemCCPId")
    placa_ccp: str = Field(default=..., alias="placaCCP")

    model_config = ConfigDict(populate_by_name=True)


class ContenedorMaritimo(BaseModel):
    """Contenedor para transporte marítimo."""
    tipo_contenedor_id: str = Field(default=..., alias="tipoContenedorId")
    matricula_contenedor: Optional[str] = Field(default=None, alias="matriculaContenedor")
    num_precinto: Optional[str] = Field(default=None, alias="numPrecinto")
    id_ccp_relacionado: Optional[str] = Field(default=None, alias="idCCPRelacionado")
    placa_vm_ccp: Optional[str] = Field(default=None, alias="placaVMCCP")
    fecha_certificacion_ccp: Optional[datetime] = Field(default=None, alias="fechaCertificacionCCP")
    remolques_ccp: Optional[list[RemolqueCCP]] = Field(default=None, alias="remolquesCCP")

    model_config = ConfigDict(populate_by_name=True, json_encoders={datetime: lambda v: v.isoformat()})


class TransporteMaritimo(BaseModel):
    """Datos del transporte marítimo."""
    perm_sct_id: Optional[str] = Field(default=None, alias="permSCTId")
    num_permiso_sct: Optional[str] = Field(default=None, alias="numPermisoSCT")
    nombre_aseg: Optional[str] = Field(default=None, alias="nombreAseg")
    num_poliza_seguro: Optional[str] = Field(default=None, alias="numPolizaSeguro")
    tipo_embarcacion_id: str = Field(default=..., alias="tipoEmbarcacionId")
    matricula: str = Field(default=..., alias="matricula")
    numero_omi: str = Field(default=..., alias="numeroOMI")
    anio_embarcacion: Optional[int] = Field(default=None, alias="anioEmbarcacion")
    nombre_embarc: Optional[str] = Field(default=None, alias="nombreEmbarc")
    nacionalidad_embarc_id: str = Field(default=..., alias="nacionalidadEmbarcId")
    unidades_de_arq_bruto: Decimal = Field(default=..., alias="unidadesDeArqBruto")
    tipo_carga_id: str = Field(default=..., alias="tipoCargaId")
    eslora: Optional[Decimal] = Field(default=None, alias="eslora")
    manga: Optional[Decimal] = Field(default=None, alias="manga")
    calado: Optional[Decimal] = Field(default=None, alias="calado")
    puntal: Optional[Decimal] = Field(default=None, alias="puntal")
    linea_naviera: Optional[str] = Field(default=None, alias="lineaNaviera")
    nombre_agente_naviero: str = Field(default=..., alias="nombreAgenteNaviero")
    num_autorizacion_naviero_id: str = Field(default=..., alias="numAutorizacionNavieroId")
    num_viaje: Optional[str] = Field(default=None, alias="numViaje")
    num_conoc_embarc: Optional[str] = Field(default=None, alias="numConocEmbarc")
    permiso_temp_navegacion: Optional[str] = Field(default=None, alias="permisoTempNavegacion")
    contenedores: Optional[list[ContenedorMaritimo]] = Field(default=None, alias="contenedores")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


# ===== Transporte Aereo =====

class TransporteAereo(BaseModel):
    """Datos del transporte aéreo."""
    perm_sct_id: str = Field(default=..., alias="permSCTId")
    num_permiso_sct: str = Field(default=..., alias="numPermisoSCT")
    matricula_aeronave: Optional[str] = Field(default=None, alias="matriculaAeronave")
    nombre_aseg: Optional[str] = Field(default=None, alias="nombreAseg")
    num_poliza_seguro: Optional[str] = Field(default=None, alias="numPolizaSeguro")
    numero_guia: str = Field(default=..., alias="numeroGuia")
    lugar_contrato: Optional[str] = Field(default=None, alias="lugarContrato")
    codigo_transportista_id: str = Field(default=..., alias="codigoTransportistaId")
    rfc_embarcador: Optional[str] = Field(default=None, alias="rfcEmbarcador")
    num_reg_id_trib_embarc: Optional[str] = Field(default=None, alias="numRegIdTribEmbarc")
    residencia_fiscal_embarc_id: Optional[str] = Field(default=None, alias="residenciaFiscalEmbarcId")
    nombre_embarcador: Optional[str] = Field(default=None, alias="nombreEmbarcador")

    model_config = ConfigDict(populate_by_name=True)


# ===== Transporte Ferroviario =====

class DerechoDePaso(BaseModel):
    """Derecho de paso del transporte ferroviario."""
    tipo_derecho_de_paso_id: str = Field(default=..., alias="tipoDerechoDePasoId")
    kilometraje_pagado: Decimal = Field(default=..., alias="kilometrajePagado")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class CarroContenedor(BaseModel):
    """Contenedor para transporte ferroviario."""
    tipo_contenedor_id: str = Field(default=..., alias="tipoContenedorId")
    peso_contenedor_vacio: Decimal = Field(default=..., alias="pesoContenedorVacio")
    peso_neto_mercancia: Decimal = Field(default=..., alias="pesoNetoMercancia")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class Carro(BaseModel):
    """Carro del transporte ferroviario."""
    tipo_carro_id: str = Field(default=..., alias="tipoCarroId")
    matricula_carro: str = Field(default=..., alias="matriculaCarro")
    guia_carro: str = Field(default=..., alias="guiaCarro")
    toneladas_netas_carro: Decimal = Field(default=..., alias="toneladasNetasCarro")
    contenedores: Optional[list[CarroContenedor]] = Field(default=None, alias="contenedores")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})


class TransporteFerroviario(BaseModel):
    """Datos del transporte ferroviario."""
    tipo_de_servicio_id: str = Field(default=..., alias="tipoDeServicioId")
    tipo_de_trafico_id: str = Field(default=..., alias="tipoDeTraficoId")
    nombre_aseg: Optional[str] = Field(default=None, alias="nombreAseg")
    num_poliza_seguro: Optional[str] = Field(default=None, alias="numPolizaSeguro")
    derechos_de_paso: Optional[list[DerechoDePaso]] = Field(default=None, alias="derechosDePaso")
    carros: list[Carro] = Field(default_factory=list, alias="carros")

    model_config = ConfigDict(populate_by_name=True)


# ===== Tipo Figura =====

class ParteTransporte(BaseModel):
    """Parte de transporte asociada a una figura."""
    parte_transporte_id: str = Field(default=..., alias="parteTransporteId")

    model_config = ConfigDict(populate_by_name=True)


class TipoFigura(BaseModel):
    """Figura de transporte (operador, propietario, arrendatario, notificado)."""
    tipo_figura_id: str = Field(default=..., alias="tipoFiguraId")
    rfc_figura: Optional[str] = Field(default=None, alias="rfcFigura")
    num_licencia: Optional[str] = Field(default=None, alias="numLicencia")
    nombre_figura: str = Field(default=..., alias="nombreFigura")
    num_reg_id_trib_figura: Optional[str] = Field(default=None, alias="numRegIdTribFigura")
    residencia_fiscal_figura_id: Optional[str] = Field(default=None, alias="residenciaFiscalFiguraId")
    partes_transporte: Optional[list[ParteTransporte]] = Field(default=None, alias="partesTransporte")
    domicilio: Optional[TipoFiguraDomicilio] = Field(default=None, alias="domicilio")

    model_config = ConfigDict(populate_by_name=True)


# ===== Carta Porte =====

class CartaPorteComplement(BaseModel):
    """Complemento Carta Porte para transporte de mercancías."""
    transp_internac_id: str = Field(default=..., alias="transpInternacId")
    entrada_salida_merc_id: Optional[str] = Field(default=None, alias="entradaSalidaMercId")
    pais_origen_destino_id: Optional[str] = Field(default=None, alias="paisOrigenDestinoId")
    via_entrada_salida_id: Optional[str] = Field(default=None, alias="viaEntradaSalidaId")
    total_dist_rec: Optional[Decimal] = Field(default=None, alias="totalDistRec")
    peso_neto_total: Optional[Decimal] = Field(default=None, alias="pesoNetoTotal")
    cargo_por_tasacion: Optional[Decimal] = Field(default=None, alias="cargoPorTasacion")
    registro_istmo_id: Optional[str] = Field(default=None, alias="registroISTMOId")
    ubicacion_polo_origen_id: Optional[str] = Field(default=None, alias="ubicacionPoloOrigenId")
    ubicacion_polo_destino_id: Optional[str] = Field(default=None, alias="ubicacionPoloDestinoId")
    unidad_peso_id: str = Field(default=..., alias="unidadPesoId")
    logistica_inversa_recoleccion_devolucion_id: Optional[str] = Field(default=None, alias="logisticaInversaRecoleccionDevolucionId")
    regimen_aduaneros: Optional[list[RegimenAduanero]] = Field(default=None, alias="regimenAduaneros")
    ubicaciones: list[Ubicacion] = Field(default_factory=list, alias="ubicaciones")
    mercancias: list[Mercancia] = Field(default_factory=list, alias="mercancias")
    autotransporte: Optional[Autotransporte] = Field(default=None, alias="autotransporte")
    transporte_maritimo: Optional[TransporteMaritimo] = Field(default=None, alias="transporteMaritimo")
    transporte_aereo: Optional[TransporteAereo] = Field(default=None, alias="transporteAereo")
    transporte_ferroviario: Optional[TransporteFerroviario] = Field(default=None, alias="transporteFerroviario")
    tipos_figura: Optional[list[TipoFigura]] = Field(default=None, alias="tiposFigura")

    model_config = ConfigDict(populate_by_name=True, json_encoders={Decimal: str})
