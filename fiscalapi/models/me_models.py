"""Modelos de la persona de la credencial (``me.get``, GET /api/v4/me)."""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from fiscalapi.models.fiscalapi_models import CreditBalance


class DeniedPermission(BaseModel):
    """Un permiso negado (``PersonFeatures.denied``): los features que le faltan al tenant."""

    missing_features: Optional[list[str]] = Field(default=None, alias="missingFeatures", description="Códigos de los features que le faltan al tenant.")

    model_config = ConfigDict(populate_by_name=True)


class PersonFeature(BaseModel):
    """Un feature habilitado del tenant (``PersonFeatures.features``)."""

    values: Optional[dict[str, int]] = Field(default=None, alias="values", description="Valores del feature por código (por ejemplo, seats); vacío si no tiene.")

    model_config = ConfigDict(populate_by_name=True)


class PersonSubscription(BaseModel):
    """La suscripción que otorga los features del tenant (``PersonFeatures.subscription``)."""

    status: Optional[str] = Field(default=None, alias="status", description="Estado de la suscripción (active, trialing o past_due), o None si ninguna otorga features.")
    is_available: Optional[bool] = Field(default=None, alias="isAvailable", description="False si no se pudieron leer los features del tenant (o la persona no tiene roles).")

    model_config = ConfigDict(populate_by_name=True)


class PersonSeatAssignment(BaseModel):
    """Un asiento de la persona en un feature por persona (``PersonFeatures.seat_assignments``)."""

    feature_code: Optional[str] = Field(default=None, alias="featureCode", description="Código del feature (por ejemplo, descarga_cfdi).")
    units: Optional[int] = Field(default=None, alias="units", description="Unidades que ocupa de la cantidad contratada.")
    status: Optional[str] = Field(default=None, alias="status", description="Active si cabe en la cantidad contratada (la persona usa el feature) o Suspended si no cabe.")

    model_config = ConfigDict(populate_by_name=True)


class PersonFeatures(BaseModel):
    """Lo que la persona puede hacer (``MeInfo.features``). Es informativo: cada endpoint vuelve a evaluar su permiso."""

    is_owner: Optional[bool] = Field(default=None, alias="isOwner", description="True si la persona es el owner del tenant.")
    roles: Optional[list[str]] = Field(default=None, alias="roles", description="Roles de la persona: Owner o Member (más Host para la persona del host).")
    permissions: Optional[list[str]] = Field(default=None, alias="permissions", description="Permisos concedidos, con la forma Área.Acción (por ejemplo, Invoices.Issue).")
    denied: Optional[dict[str, DeniedPermission]] = Field(default=None, alias="denied", description="Permisos que el rol de la persona tiene pero se le niegan porque al tenant le faltan features, por permiso.")
    features: Optional[dict[str, PersonFeature]] = Field(default=None, alias="features", description="Features habilitados del tenant, por código (por ejemplo, emision_cfdi), con sus valores.")
    subscription: Optional[PersonSubscription] = Field(default=None, alias="subscription", description="La suscripción que otorga los features del tenant.")
    seat_assignments: Optional[list[PersonSeatAssignment]] = Field(default=None, alias="seatAssignments", description="Los asientos de la persona en los features por persona; vacío si no tiene ninguno.")

    model_config = ConfigDict(populate_by_name=True)


class MeInfo(BaseModel):
    """La persona de la credencial: quién es, de qué tenant y ambiente, si es el owner, lo que puede hacer y sus saldos.
    Siempre la persona de la API key; no trae secretos."""

    id: Optional[str] = Field(default=None, alias="id", description="Id de la persona.")
    legal_name: Optional[str] = Field(default=None, alias="legalName", description="Nombre o razón social.")
    tin: Optional[str] = Field(default=None, alias="tin", description="RFC.")
    email: Optional[str] = Field(default=None, alias="email", description="Correo.")
    tenant_id: Optional[str] = Field(default=None, alias="tenantId", description="Tenant de la persona (el del header X-TENANT-KEY).")
    environment: Optional[str] = Field(default=None, alias="environment", description="Ambiente que responde: Development, Test o Production.")
    is_owner: Optional[bool] = Field(default=None, alias="isOwner", description="True si la persona es el owner del tenant (el mismo valor que features.is_owner).")
    features: Optional[PersonFeatures] = Field(default=None, alias="features", description="Lo que la persona puede hacer: roles, permisos concedidos y negados, features del tenant y suscripción.")
    balances: Optional[list[CreditBalance]] = Field(default=None, alias="balances", description="Saldos por tipo de crédito, como Person.balances; un tipo ausente tiene saldo 0.")

    model_config = ConfigDict(populate_by_name=True)
