from typing import Optional

from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import Product, ProductListFilters
from fiscalapi.services.base_service import BaseService


class ProductService(BaseService):

    def get_list(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        *,
        filters: Optional[ProductListFilters] = None,
    ) -> ApiResponse[PagedList[Product]]:
        """Obtiene una lista paginada de productos, con la página o con filtros. GET /api/v4/products

        Los filtros en None no se envían; sin página ni filtros, la lista es la de siempre (primera página).

        Args:
            page_number: Página, desde 1.
            page_size: Tamaño de página (1 a 50).
            filters: Búsqueda y página; en lugar de page_number y page_size.

        Returns:
            ApiResponse con la página de productos.

        Raises:
            ValueError: Si se pasan filters junto con page_number o page_size.
        """
        endpoint = self._list_endpoint("products", page_number, page_size, filters)
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
