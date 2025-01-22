from fiscalapi.models.common_models import ApiResponse
from fiscalapi.models.fiscalapi_models import Product
from fiscalapi.services.common_services import BaseService


class ProductService(BaseService):
    def get_by_id(self, product_id: int) -> ApiResponse[Product]:
        endpoint = f"products/{product_id}"
        return self.send_request("GET", endpoint, Product)
