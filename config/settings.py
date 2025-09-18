"""
Configuración centralizada del proyecto
"""
import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent.parent

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': BASE_DIR / 'logs' / 'odoo_api.log'
}

# Configuración de Odoo por defecto
DEFAULT_ODOO_CONFIG = {
    'timeout': 30,
    'retries': 3,
    'batch_size': 1000
}

# Configuración de PostgreSQL por defecto
DEFAULT_PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'timeout': 300
}

# Directorios de datos
DATA_DIRS = {
    'dumps': BASE_DIR / 'data' / 'dumps',
    'exports': BASE_DIR / 'data' / 'exports', 
    'imports': BASE_DIR / 'data' / 'imports',
    'logs': BASE_DIR / 'logs',
    'temp': BASE_DIR / 'temp'
}

# Crear directorios si no existen
for dir_path in DATA_DIRS.values():
    dir_path.mkdir(parents=True, exist_ok=True)
