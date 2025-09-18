"""
Configuración centralizada del proyecto Odoo API
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Odoo
ODOO_CONFIG = {
    'url': os.getenv('ODOO_URL'),
    'db': os.getenv('ODOO_DB'), 
    'user': os.getenv('ODOO_USER'),
    'api_key': os.getenv('ODOO_API_KEY')
}

# Configuración de PostgreSQL
POSTGRES_CONFIG = {
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def validate_config():
    """Valida que la configuración esté completa"""
    missing = []
    
    for key, value in ODOO_CONFIG.items():
        if not value or value.startswith('tu_'):
            missing.append(f'ODOO_{key.upper()}')
    
    if missing:
        print(f"⚠️ Faltan configurar: {', '.join(missing)}")
        print("Edita el archivo .env con tus credenciales reales")
        return False
    
    print("✅ Configuración válida")
    return True

if __name__ == "__main__":
    validate_config()
