# Documentación del Proyecto Odoo API

## 📚 Guías Disponibles

- [Instalación](installation.md)
- [Configuración](configuration.md)
- [Uso de la API](api_usage.md)
- [Restauración de BD](database_restore.md)
- [Ejemplos](examples.md)
- [Solución de Problemas](troubleshooting.md)

## 🏗️ Arquitectura del Proyecto

```
src/
├── odoo_api/          # Módulos de conexión a Odoo
├── database/          # Herramientas de base de datos
└── utils/             # Utilidades generales

config/                # Archivos de configuración
examples/              # Ejemplos de uso
tests/                 # Pruebas unitarias
notebooks/             # Jupyter notebooks
```

## 🚀 Inicio Rápido

1. Instalar dependencias: `pip install -r requirements.txt`
2. Configurar credenciales: `cp .env.example .env`
3. Ejecutar ejemplo: `python examples/basic_connection.py`
