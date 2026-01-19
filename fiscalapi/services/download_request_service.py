from datetime import datetime
from fiscalapi.models.common_models import ApiResponse, PagedList
from fiscalapi.models.fiscalapi_models import DownloadRequest, MetadataItem, Xml, FileResponse
from fiscalapi.services.base_service import BaseService


class DownloadRequestService(BaseService):
    """Servicio para gestionar solicitudes de descarga de CFDI."""
    
    def get_list(self, page_number: int, page_size: int) -> ApiResponse[PagedList[DownloadRequest]]:
        """
        Obtiene una lista paginada de solicitudes de descarga.
        
        Args:
            page_number (int): Número de página
            page_size (int): Tamaño de página
        
        Returns:
            ApiResponse[PagedList[DownloadRequest]]: Lista paginada de solicitudes de descarga
        """
        endpoint = f"download-requests?pageNumber={page_number}&pageSize={page_size}"
        return self.send_request("GET", endpoint, PagedList[DownloadRequest])
    
    def get_by_id(self, request_id: str, details: bool = False) -> ApiResponse[DownloadRequest]:
        """
        Obtiene una solicitud de descarga por su ID.
        
        Args:
            request_id (str): ID de la solicitud de descarga
            details (bool): Si incluir detalles adicionales
        
        Returns:
            ApiResponse[DownloadRequest]: Solicitud de descarga encontrada
        """
        endpoint = f"download-requests/{request_id}"
        return self.send_request("GET", endpoint, DownloadRequest, details=details)
    
    def create(self, download_request: DownloadRequest) -> ApiResponse[DownloadRequest]:
        """
        Crea una nueva solicitud de descarga.
        
        Args:
            download_request (DownloadRequest): Solicitud de descarga a crear
        
        Returns:
            ApiResponse[DownloadRequest]: Solicitud de descarga creada
        
        Raises:
            ValueError: Si download_request es None
        """
        if download_request is None:
            raise ValueError("download_request no puede ser nulo")
        
        endpoint = "download-requests"
        return self.send_request("POST", endpoint, DownloadRequest, payload=download_request)
    
    def update(self, request_id: str, download_request: DownloadRequest) -> ApiResponse[DownloadRequest]:
        """
        Actualiza una solicitud de descarga existente.
        
        Args:
            request_id (str): ID de la solicitud de descarga
            download_request (DownloadRequest): Datos actualizados de la solicitud
        
        Returns:
            ApiResponse[DownloadRequest]: Solicitud de descarga actualizada
        
        Raises:
            ValueError: Si request_id o download_request son None
        """
        if not request_id:
            raise ValueError("request_id no puede ser nulo o vacío")
        if download_request is None:
            raise ValueError("download_request no puede ser nulo")
        
        endpoint = f"download-requests/{request_id}"
        return self.send_request("PUT", endpoint, DownloadRequest, payload=download_request)
    
    def delete(self, request_id: str) -> ApiResponse[bool]:
        """
        Elimina una solicitud de descarga.
        
        Args:
            request_id (str): ID de la solicitud de descarga a eliminar
        
        Returns:
            ApiResponse[bool]: True si se eliminó correctamente
        
        Raises:
            ValueError: Si request_id es None o vacío
        """
        if not request_id:
            raise ValueError("request_id no puede ser nulo o vacío")
        
        endpoint = f"download-requests/{request_id}"
        return self.send_request("DELETE", endpoint, bool)
    
    def get_xmls(self, request_id: str) -> ApiResponse[PagedList[Xml]]:
        """
        Obtiene los XMLs asociados a una solicitud de descarga.
        
        Args:
            request_id (str): ID de la solicitud de descarga
        
        Returns:
            ApiResponse[PagedList[Xml]]: Lista paginada de XMLs
        
        Raises:
            ValueError: Si request_id es None o vacío
        """
        if not request_id:
            raise ValueError("request_id no puede ser nulo o vacío")
        
        endpoint = f"download-requests/{request_id}/xmls"
        return self.send_request("GET", endpoint, PagedList[Xml])
    
    def get_metadata_items(self, request_id: str) -> ApiResponse[PagedList[MetadataItem]]:
        """
        Obtiene los elementos de metadatos asociados a una solicitud de descarga.
        
        Args:
            request_id (str): ID de la solicitud de descarga
        
        Returns:
            ApiResponse[PagedList[MetadataItem]]: Lista paginada de elementos de metadatos
        
        Raises:
            ValueError: Si request_id es None o vacío
        """
        if not request_id:
            raise ValueError("request_id no puede ser nulo o vacío")
        
        endpoint = f"download-requests/{request_id}/meta-items"
        return self.send_request("GET", endpoint, PagedList[MetadataItem])
    
    def download_package(self, request_id: str) -> ApiResponse[list[FileResponse]]:
        """
        Descarga el paquete de archivos asociado a una solicitud de descarga.
        
        Args:
            request_id (str): ID de la solicitud de descarga
        
        Returns:
            ApiResponse[list[FileResponse]]: Lista de archivos del paquete
        
        Raises:
            ValueError: Si request_id es None o vacío
        """
        if not request_id:
            raise ValueError("request_id no puede ser nulo o vacío")
        
        endpoint = f"download-requests/{request_id}/package"
        return self.send_request("GET", endpoint, list[FileResponse])
    
    def download_sat_request(self, request_id: str) -> ApiResponse[FileResponse]:
        """
        Descarga la solicitud cruda enviada al SAT.
        
        Args:
            request_id (str): ID de la solicitud de descarga
        
        Returns:
            ApiResponse[FileResponse]: Archivo de la solicitud SAT
        
        Raises:
            ValueError: Si request_id es None o vacío
        """
        if not request_id:
            raise ValueError("request_id no puede ser nulo o vacío")
        
        endpoint = f"download-requests/{request_id}/raw-request"
        return self.send_request("GET", endpoint, FileResponse)
    
    def download_sat_response(self, request_id: str) -> ApiResponse[FileResponse]:
        """
        Descarga la respuesta cruda recibida del SAT.
        
        Args:
            request_id (str): ID de la solicitud de descarga
        
        Returns:
            ApiResponse[FileResponse]: Archivo de la respuesta SAT
        
        Raises:
            ValueError: Si request_id es None o vacío
        """
        if not request_id:
            raise ValueError("request_id no puede ser nulo o vacío")
        
        endpoint = f"download-requests/{request_id}/raw-response"
        return self.send_request("GET", endpoint, FileResponse)
    
    def search(self, created_at: datetime) -> ApiResponse[list[DownloadRequest]]:
        """
        Busca solicitudes de descarga por fecha de creación.
        
        Args:
            created_at (datetime): Fecha de creación para buscar
        
        Returns:
            ApiResponse[list[DownloadRequest]]: Lista de solicitudes encontradas
        
        Raises:
            ValueError: Si created_at es None
        """
        if created_at is None:
            raise ValueError("created_at no puede ser nulo")
        
        created_at_str = created_at.strftime("%Y-%m-%d")
        endpoint = f"download-requests/search?createdAt={created_at_str}"
        print(endpoint)
        return self.send_request("GET", endpoint, list[DownloadRequest])