#!/usr/bin/env python3
"""
Script principal de conexion a Odoo (version actualizada)
Este script usa la nueva estructura de modulos
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent / 'src'))

from odoo_api.connection import OdooConnection
from utils.config_manager import ConfigManager
from utils.logger import setup_logging, get_logger

def main():
    """Funcion principal"""
    # Configurar logging
    logger = setup_logging()
    
    print("🔌 Conexion a Odoo - Version Actualizada")
    print("=" * 50)
    
    # Cargar configuracion
    config_manager = ConfigManager()
    
    if not config_manager.validate_odoo_config():
        print("\n❌ Configuracion invalida. Edita el archivo .env")
        print("💡 Copia .env.example a .env y actualiza con tus credenciales")
        return False
    
    odoo_config = config_manager.get_odoo_config()
    
    print(f"🔗 Conectando a: {odoo_config['url']}")
    print(f"📊 Base de datos: {odoo_config['db']}")
    print(f"👤 Usuario: {odoo_config['user']}")
    
    # Crear conexion
    try:
        connection = OdooConnection(**odoo_config)
        
        # Autenticar
        print("\n🔐 Autenticando...")
        if connection.authenticate():
            print(f"✅ Autenticacion exitosa. UID: {connection.uid}")
            
            # Pruebas basicas
            print("\n📋 Ejecutando pruebas basicas...")
            
            # 1. Informacion del usuario
            try:
                user_info = connection.search_read(
                    'res.users', 
                    [['id', '=', connection.uid]], 
                    ['name', 'login', 'email', 'groups_id']
                )
                
                if user_info:
                    user = user_info[0]
                    print(f"👤 Usuario actual:")
                    print(f"   Nombre: {user.get('name')}")
                    print(f"   Login: {user.get('login')}")
                    print(f"   Email: {user.get('email')}")
                    print(f"   Grupos: {len(user.get('groups_id', []))} grupos asignados")
                
            except Exception as e:
                print(f"⚠️ Error obteniendo info del usuario: {e}")
            
            # 2. Estadisticas basicas
            try:
                print(f"\n📊 Estadisticas del sistema:")
                
                # Contar registros principales
                partners_count = connection.execute_kw('res.partner', 'search_count', [[]])
                products_count = connection.execute_kw('product.product', 'search_count', [[]])
                
                print(f"   👥 Contactos: {partners_count:,}")
                print(f"   📦 Productos: {products_count:,}")
                
                # Intentar contar ordenes de venta si existe el modelo
                try:
                    orders_count = connection.execute_kw('sale.order', 'search_count', [[]])
                    print(f"   🛒 Ordenes de venta: {orders_count:,}")
                except Exception:
                    print(f"   🛒 Ordenes de venta: Modulo no disponible")
                
                # Intentar contar facturas si existe el modelo
                try:
                    invoices_count = connection.execute_kw('account.move', 'search_count', [
                        [['move_type', 'in', ['out_invoice', 'out_refund']]]
                    ])
                    print(f"   🧾 Facturas: {invoices_count:,}")
                except Exception:
                    print(f"   🧾 Facturas: Modulo no disponible")
                    
            except Exception as e:
                print(f"⚠️ Error obteniendo estadisticas: {e}")
            
            # 3. Probar modelos especificos
            print(f"\n🧪 Probando modelos especificos...")
            
            # Importar modelos especificos
            from odoo_api.models import Partner, Product
            
            try:
                # Probar modelo Partner
                partner_model = Partner(connection)
                companies = partner_model.get_companies(limit=5)
                print(f"   🏢 Primeras 5 empresas:")
                for company in companies[:3]:  # Mostrar solo 3 para no saturar
                    print(f"     - {company.get('name', 'Sin nombre')}")
                
            except Exception as e:
                print(f"   ⚠️ Error probando modelo Partner: {e}")
            
            try:
                # Probar modelo Product
                product_model = Product(connection)
                products = product_model.get_active_products(limit=3)
                print(f"   📦 Primeros 3 productos activos:")
                for product in products:
                    name = product.get('name', 'Sin nombre')
                    price = product.get('list_price', 0)
                    print(f"     - {name} (${price})")
                    
            except Exception as e:
                print(f"   ⚠️ Error probando modelo Product: {e}")
            
            print(f"\n🎉 ¡Todas las pruebas completadas exitosamente!")
            print(f"🔧 Tu conexion a Odoo esta funcionando correctamente.")
            return True
            
        else:
            print("❌ Error en la autenticacion")
            print("💡 Verifica:")
            print("   - Tu API Key sea correcta")
            print("   - Tu usuario tenga permisos de API")
            print("   - La URL y base de datos sean correctas")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexion: {e}")
        print("💡 Verifica que la instancia de Odoo este accesible")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
