#!/bin/bash
# Script de configuración inicial del proyecto

echo "🚀 Configurando proyecto Odoo API..."

# Crear entorno virtual si no existe
if [ ! -d "odooAPI" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv odooAPI
fi

# Activar entorno virtual
source odooAPI/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo de configuración..."
    cp .env.example .env
    echo "✏️ Edita el archivo .env con tus credenciales"
fi

# Crear directorios de datos
mkdir -p data/{dumps,exports,imports}
mkdir -p logs

echo "✅ Configuración completada!"
echo "💡 Próximos pasos:"
echo "   1. Edita .env con tus credenciales de Odoo"
echo "   2. Ejecuta: python examples/basic_connection.py"
