"""
Utilidades para trabajar con Odoo API
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, date

logger = logging.getLogger(__name__)

class OdooUtils:
    """Utilidades generales para Odoo"""
    
    @staticmethod
    def format_domain(conditions: Dict[str, Any]) -> List:
        """
        Convierte un diccionario en formato de dominio de Odoo
        
        Args:
            conditions: Diccionario con condiciones {campo: valor}
            
        Returns:
            List: Dominio en formato de Odoo
            
        Example:
            format_domain({'name': 'Juan', 'active': True})
            # Retorna: [['name', '=', 'Juan'], ['active', '=', True]]
        """
        domain = []
        for field, value in conditions.items():
            if isinstance(value, (list, tuple)) and len(value) == 2:
                operator, val = value
                domain.append([field, operator, val])
            else:
                domain.append([field, '=', value])
        return domain
    
    @staticmethod
    def batch_process(items: List[Any], batch_size: int = 100):
        """
        Divide una lista en lotes para procesamiento por batch
        
        Args:
            items: Lista de elementos
            batch_size: Tamaño del lote
            
        Yields:
            List: Lote de elementos
        """
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]
    
    @staticmethod
    def clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Limpia datos removiendo campos con valores vacíos o inválidos
        
        Args:
            data: Diccionario con datos
            
        Returns:
            Dict: Datos limpiados
        """
        cleaned = {}
        for key, value in data.items():
            if value is not None and value != '' and value != []:
                # Convertir fechas a string si es necesario
                if isinstance(value, (datetime, date)):
                    cleaned[key] = value.isoformat()
                else:
                    cleaned[key] = value
        return cleaned
    
    @staticmethod
    def parse_many2one(value: Any) -> Optional[int]:
        """
        Parsea un campo many2one de Odoo
        
        Args:
            value: Valor del campo many2one (puede ser False, int, o [int, str])
            
        Returns:
            Optional[int]: ID del registro o None
        """
        if isinstance(value, list) and len(value) >= 2:
            return value[0]  # [id, name]
        elif isinstance(value, int):
            return value
        else:
            return None  # False o None
    
    @staticmethod
    def parse_many2many(value: Any) -> List[int]:
        """
        Parsea un campo many2many de Odoo
        
        Args:
            value: Valor del campo many2many
            
        Returns:
            List[int]: Lista de IDs
        """
        if isinstance(value, list):
            return [v for v in value if isinstance(v, int)]
        else:
            return []
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Valida formato de email básico
        
        Args:
            email: Email a validar
            
        Returns:
            bool: True si el formato es válido
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def generate_external_id(prefix: str, record_id: int) -> str:
        """
        Genera un ID externo para un registro
        
        Args:
            prefix: Prefijo para el ID
            record_id: ID del registro
            
        Returns:
            str: ID externo generado
        """
        return f"{prefix}_{record_id}"
    
    @staticmethod
    def odoo_date_to_python(odoo_date: str) -> Optional[datetime]:
        """
        Convierte fecha de Odoo a objeto Python datetime
        
        Args:
            odoo_date: Fecha en formato de Odoo
            
        Returns:
            Optional[datetime]: Objeto datetime o None si hay error
        """
        if not odoo_date:
            return None
        
        try:
            # Formato típico de Odoo: "2024-01-15 10:30:00"
            return datetime.strptime(odoo_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                # Formato de fecha solamente: "2024-01-15"
                return datetime.strptime(odoo_date, '%Y-%m-%d')
            except ValueError:
                logger.warning(f"No se pudo parsear fecha: {odoo_date}")
                return None
    
    @staticmethod
    def python_date_to_odoo(python_date: datetime) -> str:
        """
        Convierte objeto datetime de Python a formato de Odoo
        
        Args:
            python_date: Objeto datetime
            
        Returns:
            str: Fecha en formato de Odoo
        """
        return python_date.strftime('%Y-%m-%d %H:%M:%S')
