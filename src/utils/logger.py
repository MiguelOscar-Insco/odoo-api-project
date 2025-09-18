"""
Configuración de logging para el proyecto
"""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

def setup_logging(level: str = 'INFO', log_file: str = None) -> logging.Logger:
    """
    Configura el sistema de logging
    
    Args:
        level: Nivel de logging ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        log_file: Ruta al archivo de log (opcional)
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear logger principal
    logger = logging.getLogger('odoo_api')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formato de logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (si se especifica)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger hijo
    
    Args:
        name: Nombre del logger
        
    Returns:
        logging.Logger: Logger hijo
    """
    return logging.getLogger(f'odoo_api.{name}')
