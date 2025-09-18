"""
Gestor de configuración del proyecto
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class ConfigManager:
    """Gestiona la configuración del proyecto"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Inicializar gestor de configuración
        
        Args:
            env_file: Ruta al archivo .env (opcional)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            # Buscar .env en el directorio raíz del proyecto
            project_root = Path(__file__).parent.parent.parent
            env_path = project_root / '.env'
            if env_path.exists():
                load_dotenv(env_path)
    
    def get_odoo_config(self) -> Dict[str, str]:
        """
        Obtiene configuración de Odoo desde variables de entorno
        
        Returns:
            Dict: Configuración de Odoo
        """
        return {
            'url': os.getenv('ODOO_URL', ''),
            'db': os.getenv('ODOO_DB', ''),
            'user': os.getenv('ODOO_USER', ''),
            'api_key': os.getenv('ODOO_API_KEY', '')
        }
    
    def get_postgres_config(self) -> Dict[str, str]:
        """
        Obtiene configuración de PostgreSQL
        
        Returns:
            Dict: Configuración de PostgreSQL
        """
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'root')
        }
    
    def validate_odoo_config(self) -> bool:
        """
        Valida que la configuración de Odoo esté completa
        
        Returns:
            bool: True si la configuración es válida
        """
        config = self.get_odoo_config()
        
        for key, value in config.items():
            if not value or value.startswith('tu_'):
                print(f"❌ Falta configurar: ODOO_{key.upper()}")
                return False
        
        return True
    
    def get_config_summary(self) -> Dict[str, Any]:
        """
        Obtiene resumen de la configuración
        
        Returns:
            Dict: Resumen de configuración
        """
        odoo_config = self.get_odoo_config()
        postgres_config = self.get_postgres_config()
        
        # Ocultar información sensible
        safe_config = {
            'odoo': {
                'url': odoo_config['url'],
                'db': odoo_config['db'],
                'user': odoo_config['user'],
                'api_key': f"{odoo_config['api_key'][:10]}..." if odoo_config['api_key'] else ''
            },
            'postgres': {
                'host': postgres_config['host'],
                'port': postgres_config['port'],
                'user': postgres_config['user'],
                'password': '***' if postgres_config['password'] else ''
            }
        }
        
        return safe_config
