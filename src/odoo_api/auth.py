"""
Módulo de autenticación para Odoo
"""
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class OdooAuth:
    """Clase para manejar autenticación con Odoo"""
    
    def __init__(self, url: str, db: str, user: str, api_key: str):
        """
        Inicializar autenticador
        
        Args:
            url: URL de la instancia de Odoo
            db: Nombre de la base de datos
            user: Usuario de Odoo
            api_key: API Key de Odoo
        """
        self.url = url
        self.db = db
        self.user = user
        self.api_key = api_key
        self.uid = None
    
    def authenticate(self, connection) -> bool:
        """
        Autentica el usuario usando la conexión proporcionada
        
        Args:
            connection: Instancia de OdooConnection
            
        Returns:
            bool: True si la autenticación fue exitosa
        """
        try:
            result = connection._jsonrpc_request("common", "authenticate", 
                                               [self.db, self.user, self.api_key, {}])
            self.uid = result
            return bool(self.uid)
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado"""
        return self.uid is not None
    
    def get_uid(self) -> Optional[int]:
        """Retorna el UID del usuario autenticado"""
        return self.uid
    
    def validate_credentials(self) -> Dict[str, Any]:
        """
        Valida las credenciales sin autenticar
        
        Returns:
            Dict con el resultado de la validación
        """
        issues = []
        
        if not self.url:
            issues.append("URL no configurada")
        elif not self.url.startswith(('http://', 'https://')):
            issues.append("URL debe comenzar con http:// o https://")
            
        if not self.db:
            issues.append("Base de datos no configurada")
            
        if not self.user:
            issues.append("Usuario no configurado")
        elif '@' not in self.user:
            issues.append("Usuario debe ser un email válido")
            
        if not self.api_key:
            issues.append("API Key no configurada")
        elif len(self.api_key) < 10:
            issues.append("API Key parece demasiado corta")
            
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
