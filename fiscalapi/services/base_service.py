from typing import Type, TypeVar
from pydantic import BaseModel
import requests
from fiscalapi.models.common_models import ApiResponse, FiscalApiSettings, ValidationFailure

#T = TypeVar('T', bound=BaseModel)

T = TypeVar('T')


class BaseService:
    def __init__(self, settings: FiscalApiSettings):
        self.settings = settings
        self.api_version = settings.api_version
        self.base_url = settings.api_url
        self.api_key = settings.api_key

    def _get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "X-TENANT-KEY": self.settings.tenant,
            "X-API-KEY": self.settings.api_key,
            "X-TIME-ZONE": self.settings.time_zone,
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"
        headers = self._get_headers()

        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        # Disable certificate validation (for development only!)
        kwargs.setdefault("verify", False)


        # print payload request
        print("***Payload Request:", kwargs.get("json"))
        
        # print line breaks 
        print("\n\n")
        
        
        # Send request
        response = requests.request(method=method, url=url, headers=headers, **kwargs)
        
        # print payload response
        print("***Payload Response:", response.text)
         
        # print line breaks 
        print("\n\n")

        return response

    def _process_response(self, response: requests.Response, response_model: Type[T]) -> ApiResponse[T]:
        status_code = response.status_code
        raw_content = response.text

        try:
            response_data = response.json()
        except ValueError:
            return ApiResponse[T](
                succeeded=False,
                http_status_code=status_code,
                message="Error processing server response",
                details=raw_content,
                data=None
            )

        if 200 <= status_code < 300:
            
            if issubclass(response_model, BaseModel) and isinstance(response_data["data"], dict):
                response_data["data"] = response_model.model_validate(response_data["data"])
                
            return ApiResponse[T].model_validate(response_data)

        try:
            generic_error = ApiResponse[object].model_validate(response_data)
        except Exception:
            return ApiResponse[T](
                succeeded=False,
                http_status_code=status_code,
                message="Error processing server error response",
                details=raw_content,
                data=None
            )

        if status_code == 400 and isinstance(response_data.get("data"), list):
            try:
                failures = [ValidationFailure.model_validate(item) for item in response_data["data"]]
                if failures:
                    details_str = "; ".join(f"{f.propertyName}: {f.errorMessage}" for f in failures)
                    return ApiResponse[T](
                        succeeded=False,
                        http_status_code=400,
                        message=generic_error.message,
                        details=details_str,
                        data=None
                    )
            except Exception:
                pass

        return ApiResponse[T](
            succeeded=False,
            http_status_code=status_code,
            message=generic_error.message or f"HTTP Error {status_code}",
            details=generic_error.details or raw_content,
            data=None
        )

    def send_request(self, method: str, endpoint: str, response_model: Type[T], **kwargs) -> ApiResponse[T]:
        payload = kwargs.pop("payload", None)
        if payload is not None and isinstance(payload, BaseModel):
            # Excluir propiedades con valor None
            kwargs["json"] = payload.model_dump(mode="json", by_alias=True, exclude_none=True)

        response = self._request(method, endpoint, **kwargs)
        return self._process_response(response, response_model)