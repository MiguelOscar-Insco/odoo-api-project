#!/usr/bin/env python3
"""
Script para probar que todas las importaciones funcionan
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_imports():
    """Prueba todas las importaciones"""
    print("🧪 Probando importaciones...")
    
    try:
        print("  ✓ Importando config_manager...")
        from utils.config_manager import ConfigManager
        
        print("  ✓ Importando connection...")
        from odoo_api.connection import OdooConnection
        
        print("  ✓ Importando auth...")
        from odoo_api.auth import OdooAuth
        
        print("  ✓ Importando models...")
        from odoo_api.models import OdooModel, Partner, Product
        
        print("  ✓ Importando utils...")
        from odoo_api.utils import OdooUtils
        
        print("  ✓ Importando logger...")
        from utils.logger import setup_logging
        
        print("  ✓ Importando validators...")
        from utils.validators import validate_config
        
        print("\n✅ Todas las importaciones exitosas!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Error de importacion: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

def test_config():
    """Prueba la configuracion"""
    print("\n🔧 Probando configuracion...")
    
    try:
        from utils.config_manager import ConfigManager
        
        config_manager = ConfigManager()
        odoo_config = config_manager.get_odoo_config()
        
        print(f"  URL: {odoo_config['url']}")
        print(f"  DB: {odoo_config['db']}")
        print(f"  User: {odoo_config['user']}")
        print(f"  API Key: {'Configurada' if odoo_config['api_key'] else 'No configurada'}")
        
        if config_manager.validate_odoo_config():
            print("  ✅ Configuracion valida")
            return True
        else:
            print("  ⚠️ Configuracion incompleta")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en configuracion: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de Sistema")
    print("=" * 30)
    
    imports_ok = test_imports()
    config_ok = test_config()
    
    if imports_ok and config_ok:
        print("\n🎉 Sistema listo para usar!")
        print("Ejecuta: python connect_odoo.py")
    else:
        print("\n❌ Hay problemas que resolver")
        if not imports_ok:
            print("  - Revisa los modulos en src/")
        if not config_ok:
            print("  - Configura tu archivo .env")
