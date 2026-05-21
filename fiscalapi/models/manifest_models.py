"""Modelos para firma de carta manifiesto (endpoint POST /api/v4/manifests)."""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SignManifestRequest(BaseModel):
    """Petición para firmar una carta manifiesto con la FIEL del contribuyente."""

    base64_cer: str = Field(default=..., alias="base64Cer", description="Certificado FIEL (.cer) en base64.")
    base64_key: str = Field(default=..., alias="base64Key", description="Llave privada FIEL (.key) en base64.")
    password: str = Field(default=..., alias="password", description="Contraseña de la llave privada FIEL.")

    model_config = ConfigDict(populate_by_name=True)


class SignManifestResponse(BaseModel):
    """Respuesta con el PDF firmado de la carta manifiesto."""

    base64_file: Optional[str] = Field(default=None, alias="base64File", description="PDF firmado en base64.")
    file_name: Optional[str] = Field(default=None, alias="fileName", description="Nombre sugerido del archivo (RFC.pdf).")
    file_extension: Optional[str] = Field(default=None, alias="fileExtension", description="Extensión del archivo (.pdf).")

    model_config = ConfigDict(populate_by_name=True)
