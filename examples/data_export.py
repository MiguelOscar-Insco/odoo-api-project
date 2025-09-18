#!/usr/bin/env python3
"""
Ejemplo de exportación de datos desde Odoo
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from odoo_api.connection import OdooConnection
from utils.config_manager import ConfigManager

def export_partners(connection: OdooConnection, output_file: Path):
    """Exporta contactos a archivo JSON"""
    print("📤 Exportando contactos...")
    
    partners = connection.search_read(
        'res.partner',
        [['is_company', '=', True]],  # Solo empresas
        ['name', 'email', 'phone', 'website', 'country_id'],
        limit=100
    )
    
    # Agregar timestamp
    export_data = {
        'export_date': datetime.now().isoformat(),
        'total_records': len(partners),
        'data': partners
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(partners)} contactos exportados a {output_file}")

def main():
    """Función principal"""
    print("📊 Ejemplo de Exportación de Datos")
    print("=" * 40)
    
    # Configuración
    config = ConfigManager()
    if not config.validate_odoo_config():
        print("❌ Configuración inválida")
        return
    
    # Conexión
    odoo_config = config.get_odoo_config()
    connection = OdooConnection(**odoo_config)
    
    if not connection.authenticate():
        print("❌ Error de autenticación")
        return
    
    print("✅ Conexión establecida")
    
    # Exportar datos
    output_dir = Path(__file__).parent.parent / 'data' / 'exports'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'partners_export_{timestamp}.json'
    
    export_partners(connection, output_file)

if __name__ == "__main__":
    main()
