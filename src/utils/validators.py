"""
Validadores para el proyecto
"""
import re
from typing import Dict, List, Any
from urllib.parse import urlparse

def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida configuración completa del proyecto
    
    Args:
        config: Configuración a validar
        
    Returns:
        Dict: Resultado de la validación
    """
    errors = []
    warnings = []
    
    # Validar configuración de Odoo
    if 'odoo' in config:
        odoo_result = validate_odoo_config(config['odoo'])
        errors.extend(odoo_result.get('errors', []))
        warnings.extend(odoo_result.get('warnings', []))
    
    # Validar configuración de PostgreSQL
    if 'postgres' in config:
        pg_result = validate_postgres_config(config['postgres'])
        errors.extend(pg_result.get('errors', []))
        warnings.extend(pg_result.get('warnings', []))
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def validate_odoo_config(config: Dict[str, str]) -> Dict[str, Any]:
    """
    Valida configuración específica de Odoo
    
    Args:
        config: Configuración de Odoo
        
    Returns:
        Dict: Resultado de la validación
    """
    errors = []
    warnings = []
    
    # Validar URL
    url = config.get('url', '')
    if not url:
        errors.append("URL de Odoo no configurada")
    else:
        parsed = urlparse(url)
        if not parsed.scheme in ['http', 'https']:
            errors.append("URL debe comenzar con http:// o https://")
        if not parsed.netloc:
            errors.append("URL no tiene dominio válido")
        if parsed.scheme == 'http':
            warnings.append("Se recomienda usar HTTPS en producción")
    
    # Validar base de datos
    db = config.get('db', '')
    if not db:
        errors.append("Nombre de base de datos no configurado")
    elif len(db) < 3:
        warnings.append("Nombre de base de datos muy corto")
    
    # Validar usuario
    user = config.get('user', '')
    if not user:
        errors.append("Usuario no configurado")
    elif '@' not in user:
        errors.append("Usuario debe ser un email válido")
    elif not validate_email(user):
        warnings.append("Formato de email del usuario puede ser inválido")
    
    # Validar API Key
    api_key = config.get('api_key', '')
    if not api_key:
        errors.append("API Key no configurada")
    elif api_key.startswith('tu_'):
        errors.append("API Key no ha sido actualizada desde el template")
    elif len(api_key) < 20:
        warnings.append("API Key parece demasiado corta")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def validate_postgres_config(config: Dict[str, str]) -> Dict[str, Any]:
    """
    Valida configuración de PostgreSQL
    
    Args:
        config: Configuración de PostgreSQL
        
    Returns:
        Dict: Resultado de la validación
    """
    errors = []
    warnings = []
    
    # Validar host
    host = config.get('host', '')
    if not host:
        errors.append("Host de PostgreSQL no configurado")
    
    # Validar puerto
    port = config.get('port', '')
    if not port:
        warnings.append("Puerto no configurado, usando 5432 por defecto")
    else:
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                errors.append("Puerto debe estar entre 1 y 65535")
        except ValueError:
            errors.append("Puerto debe ser un número")
    
    # Validar usuario
    user = config.get('user', '')
    if not user:
        errors.append("Usuario de PostgreSQL no configurado")
    
    # Validar contraseña
    password = config.get('password', '')
    if not password:
        warnings.append("Contraseña de PostgreSQL no configurada")
    elif len(password) < 4:
        warnings.append("Contraseña muy corta, se recomienda al menos 4 caracteres")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def validate_email(email: str) -> bool:
    """
    Valida formato básico de email
    
    Args:
        email: Email a validar
        
    Returns:
        bool: True si es válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_url(url: str) -> bool:
    """
    Valida formato de URL
    
    Args:
        url: URL a validar
        
    Returns:
        bool: True si es válida
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except:
        return False

def validate_domain(domain: List) -> bool:
    """
    Valida formato de dominio de Odoo
    
    Args:
        domain: Dominio a validar
        
    Returns:
        bool: True si es válido
    """
    if not isinstance(domain, list):
        return False
    
    for condition in domain:
        if not isinstance(condition, list) or len(condition) != 3:
            return False
        
        field, operator, value = condition
        if not isinstance(field, str):
            return False
        
        valid_operators = ['=', '!=', '>', '<', '>=', '<=', 'like', 'ilike', 'in', 'not in']
        if operator not in valid_operators:
            return False
    
    return True
