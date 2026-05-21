from fiscalapi.models.common_models import ApiResponse
from fiscalapi.models.manifest_models import SignManifestRequest, SignManifestResponse
from fiscalapi.services.base_service import BaseService


class ManifestService(BaseService):
    """Servicio para firmar cartas manifiesto con la FIEL del contribuyente."""

    def sign(self, request: SignManifestRequest) -> ApiResponse[SignManifestResponse]:
        endpoint = "manifests"
        return self.send_request("POST", endpoint, SignManifestResponse, payload=request)
