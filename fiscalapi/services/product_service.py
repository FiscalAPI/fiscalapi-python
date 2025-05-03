from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import Product
from fiscalapi.services.base_service import BaseService


class ProductService(BaseService):
    
    # get paged list of products
    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[Product]]:
        endpoint = f"products?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[Product])
    
    # get product by id
    def get_by_id(self, product_id: str) -> ApiResponse[Product]:
        endpoint = f"products/{product_id}"
        return self.send_request("GET", endpoint, Product)
    
    # create product
    def create(self, product: Product) -> ApiResponse[Product]:
        endpoint = "products"
        return self.send_request("POST", endpoint, Product, payload=product)
    
    # update product
    def update(self, product: Product) -> ApiResponse[Product]:
        endpoint = f"products/{product.id}"
        return self.send_request("PUT", endpoint, Product, payload=product)
    
    # delete product
    def delete(self, product_id: str) -> ApiResponse[bool]:
        endpoint = f"products/{product_id}"
        return self.send_request("DELETE", endpoint, bool)
