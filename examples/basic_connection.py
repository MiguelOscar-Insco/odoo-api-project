#!/usr/bin/env python3
"""
Ejemplo básico de conexión a Odoo
"""

import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from odoo_api.connection import OdooConnection
from utils.config_manager import ConfigManager

def main():
    """Ejemplo de conexión básica"""
    print("🔌 Ejemplo de Conexión Básica a Odoo")
    print("=" * 40)
    
    # Cargar configuración
    config = ConfigManager()
    odoo_config = config.get_odoo_config()
    
    if not config.validate_odoo_config():
        print("❌ Configuración inválida. Revisa tu archivo .env")
        return
    
    # Crear conexión
    connection = OdooConnection(
        url=odoo_config['url'],
        db=odoo_config['db'],
        user=odoo_config['user'],
        api_key=odoo_config['api_key']
    )
    
    # Autenticar
    print("🔐 Autenticando...")
    if connection.authenticate():
        print(f"✅ Autenticación exitosa. UID: {connection.uid}")
        
        # Ejemplo: Leer información del usuario actual
        print("\n👤 Información del usuario:")
        user_info = connection.search_read(
            'res.users', 
            [['id', '=', connection.uid]], 
            ['name', 'login', 'email']
        )
        
        if user_info:
            user = user_info[0]
            print(f"   Nombre: {user.get('name')}")
            print(f"   Login: {user.get('login')}")
            print(f"   Email: {user.get('email')}")
        
        # Ejemplo: Contar registros
        print("\n📊 Estadísticas:")
        partners_count = len(connection.execute_kw('res.partner', 'search', [[]]))
        products_count = len(connection.execute_kw('product.product', 'search', [[]]))
        
        print(f"   Contactos: {partners_count}")
        print(f"   Productos: {products_count}")
        
    else:
        print("❌ Error en la autenticación")

if __name__ == "__main__":
    main()
