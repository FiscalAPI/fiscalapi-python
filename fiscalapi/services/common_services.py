from typing import Type, TypeVar
from pydantic import BaseModel
import requests
from fiscalapi.models.common_models import ApiResponse, FiscalApiSettings

T = TypeVar('T', bound=BaseModel)

class BaseService:
    """
    Clase base que agrupa lógica repetida en los servicios,
    como la construcción de URLs, cabeceras y manejo de responses.
    """

    def __init__(self, settings: FiscalApiSettings):
        self.settings = settings
        self.api_version = settings.api_version
        self.base_url = settings.api_url
        self.api_key = settings.api_key

    def _get_headers(self) -> dict:
        """
        Construye las cabeceras http necesarias.
        """
        return {
            "Content-Type": "application/json",
            "X-TENANT-KEY": self.settings.tenant,
            "X-API-KEY": self.settings.api_key,
            "X-TIME-ZONE": self.settings.time_zone,
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Realiza una llamada HTTP con la librería requests.
        """
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"
        headers = self._get_headers()

        # Unir los headers definidos por el usuario con los headers por defecto.
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            del kwargs["headers"]

        response = requests.request(method=method, url=url, headers=headers, **kwargs)
        response.raise_for_status()  # Levanta excepciones para errores HTTP
        return response

    def _process_response(self, response: requests.Response, response_model: Type[BaseModel]) -> ApiResponse:
        """
        Procesa y valida la respuesta de la API.
        """
        try:
            response_data = response.json()

            # Procesar el campo `data` utilizando los modelos con alias
            if "data" in response_data and response_data["data"] is not None:
                response_data["data"] = response_model.model_validate(response_data["data"])

            return ApiResponse.model_validate(response_data)
        except Exception as e:
            print(f"Error al procesar la respuesta: {e}")
            print(f"Response data: {response.json()}")
            raise



    def send_request(self, method: str, endpoint: str, response_model: Type[T], **kwargs) -> ApiResponse[T]:
        """
        Envía una solicitud HTTP y devuelve la respuesta deserializada en un ApiResponse.
        """
        response = self._request(method, endpoint, **kwargs)
        return self._process_response(response, response_model)