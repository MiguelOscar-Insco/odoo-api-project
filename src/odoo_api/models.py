"""
Módulo para trabajar con modelos de Odoo
"""
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class OdooModel:
    """Clase base para trabajar con modelos de Odoo"""
    
    def __init__(self, connection, model_name: str):
        """
        Inicializar modelo
        
        Args:
            connection: Instancia de OdooConnection
            model_name: Nombre del modelo de Odoo (ej: 'res.partner')
        """
        self.connection = connection
        self.model_name = model_name
    
    def search(self, domain: List = None, limit: int = None, 
               offset: int = 0, order: str = None) -> List[int]:
        """
        Busca registros que cumplan el dominio
        
        Args:
            domain: Condiciones de búsqueda
            limit: Límite de registros
            offset: Número de registros a omitir
            order: Campo por el cual ordenar
            
        Returns:
            List[int]: IDs de los registros encontrados
        """
        args = [domain or []]
        kwargs = {}
        
        if limit:
            kwargs['limit'] = limit
        if offset:
            kwargs['offset'] = offset
        if order:
            kwargs['order'] = order
            
        return self.connection.execute_kw(self.model_name, 'search', args, kwargs)
    
    def read(self, ids: List[int], fields: List[str] = None) -> List[Dict]:
        """
        Lee los campos de los registros especificados
        
        Args:
            ids: IDs de los registros a leer
            fields: Campos a leer (None para todos)
            
        Returns:
            List[Dict]: Datos de los registros
        """
        args = [ids]
        kwargs = {}
        
        if fields:
            kwargs['fields'] = fields
            
        return self.connection.execute_kw(self.model_name, 'read', args, kwargs)
    
    def search_read(self, domain: List = None, fields: List[str] = None,
                   limit: int = None, offset: int = 0, order: str = None) -> List[Dict]:
        """
        Combina search y read en una sola operación
        
        Args:
            domain: Condiciones de búsqueda
            fields: Campos a leer
            limit: Límite de registros
            offset: Número de registros a omitir
            order: Campo por el cual ordenar
            
        Returns:
            List[Dict]: Datos de los registros encontrados
        """
        args = [domain or []]
        kwargs = {}
        
        if fields:
            kwargs['fields'] = fields
        if limit:
            kwargs['limit'] = limit
        if offset:
            kwargs['offset'] = offset
        if order:
            kwargs['order'] = order
            
        return self.connection.execute_kw(self.model_name, 'search_read', args, kwargs)
    
    def create(self, values: Dict[str, Any]) -> int:
        """
        Crea un nuevo registro
        
        Args:
            values: Valores del nuevo registro
            
        Returns:
            int: ID del registro creado
        """
        return self.connection.execute_kw(self.model_name, 'create', [values])
    
    def write(self, ids: List[int], values: Dict[str, Any]) -> bool:
        """
        Actualiza registros existentes
        
        Args:
            ids: IDs de los registros a actualizar
            values: Nuevos valores
            
        Returns:
            bool: True si la actualización fue exitosa
        """
        return self.connection.execute_kw(self.model_name, 'write', [ids, values])
    
    def unlink(self, ids: List[int]) -> bool:
        """
        Elimina registros
        
        Args:
            ids: IDs de los registros a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa
        """
        return self.connection.execute_kw(self.model_name, 'unlink', [ids])
    
    def count(self, domain: List = None) -> int:
        """
        Cuenta registros que cumplan el dominio
        
        Args:
            domain: Condiciones de búsqueda
            
        Returns:
            int: Número de registros
        """
        return self.connection.execute_kw(self.model_name, 'search_count', [domain or []])
    
    def get_fields(self) -> Dict[str, Dict]:
        """
        Obtiene información sobre los campos del modelo
        
        Returns:
            Dict: Información de los campos
        """
        return self.connection.execute_kw(self.model_name, 'fields_get', [])

# Clases específicas para modelos comunes
class Partner(OdooModel):
    """Modelo para res.partner (Contactos)"""
    
    def __init__(self, connection):
        super().__init__(connection, 'res.partner')
    
    def find_by_email(self, email: str) -> List[Dict]:
        """Busca contacto por email"""
        return self.search_read([['email', '=', email]])
    
    def get_companies(self, limit: int = None) -> List[Dict]:
        """Obtiene empresas (is_company=True)"""
        return self.search_read([['is_company', '=', True]], limit=limit)

class Product(OdooModel):
    """Modelo para product.product (Productos)"""
    
    def __init__(self, connection):
        super().__init__(connection, 'product.product')
    
    def find_by_barcode(self, barcode: str) -> List[Dict]:
        """Busca producto por código de barras"""
        return self.search_read([['barcode', '=', barcode]])
    
    def get_active_products(self, limit: int = None) -> List[Dict]:
        """Obtiene productos activos"""
        return self.search_read([['active', '=', True]], limit=limit)

class SaleOrder(OdooModel):
    """Modelo para sale.order (Órdenes de Venta)"""
    
    def __init__(self, connection):
        super().__init__(connection, 'sale.order')
    
    def get_draft_orders(self, limit: int = None) -> List[Dict]:
        """Obtiene órdenes en borrador"""
        return self.search_read([['state', '=', 'draft']], limit=limit)
    
    def get_confirmed_orders(self, limit: int = None) -> List[Dict]:
        """Obtiene órdenes confirmadas"""
        return self.search_read([['state', '=', 'sale']], limit=limit)
