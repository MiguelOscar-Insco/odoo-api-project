# Guía de Instalación

## Requisitos del Sistema

- Python 3.8 o superior
- PostgreSQL (opcional, para restauración de BD)
- Acceso a instancia de Odoo con API habilitada

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/odoo-api-project.git
cd odoo-api-project
```

### 2. Crear entorno virtual
```bash
python -m venv odooAPI
source odooAPI/bin/activate  # Linux/Mac
# odooAPI\Scripts\activate    # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## Verificación de Instalación

```bash
python -c "from src.odoo_api import OdooConnection; print('✅ Instalación exitosa')"
```
