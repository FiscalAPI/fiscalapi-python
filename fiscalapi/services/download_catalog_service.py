from typing import List
from fiscalapi.models.common_models import ApiResponse, CatalogDto, PagedList
from fiscalapi.services.base_service import BaseService



class DownloadCatalogService(BaseService):
    """Servicio para gestionar catálogos de descarga masiva."""
    
    def get_list(self) -> ApiResponse[List[str]]:
        """
        Obtiene una lista de catálogos disponibles.
        
        Returns:
            ApiResponse[List[str]]: Lista de catálogos disponibles
        """
        endpoint = "download-catalogs"
        return self.send_request("GET", endpoint, List[str])
    
    def list_catalog (self, catalog_name: str) -> ApiResponse[List[CatalogDto]]:
        """
        Obtiene una lista de registros de un catálogo.
        
        Args:
            catalog_name (str): Nombre del catálogo
        Returns:
            ApiResponse[List[CatalogDto]]: Lista de registros de un catálogo
        """
        endpoint = f"download-catalogs/{catalog_name}"
        return self.send_request("GET", endpoint, List[CatalogDto])
    
    