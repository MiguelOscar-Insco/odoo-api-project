import subprocess
import os

# --- Parámetros de la Base de Datos ---
DB_NAME = "odoo_backup_restored" # Puedes elegir el nombre que quieras para la nueva base de datos
DB_USER = "postgres"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DUMP_FILE_PATH = r"C:\Users\Miguel Oscar\Documents\Odoo Backups\dump.sql"

# --- Configurar variables de entorno para la contraseña ---
# Esto es más seguro que poner la contraseña en la línea de comando
os.environ["PGPASSWORD"] = DB_PASSWORD

try:
    # Paso 1: Crear una nueva base de datos vacía
    print("Creando la nueva base de datos...")
    create_db_command = ["createdb", "-h", DB_HOST, "-U", DB_USER, DB_NAME]
    subprocess.run(create_db_command, check=True)
    print(f"Base de datos '{DB_NAME}' creada exitosamente.")

    # Paso 2: Restaurar el dump en la nueva base de datos
    print(f"Restaurando el archivo '{DUMP_FILE_PATH}'...")
    restore_command = ["psql", "-h", DB_HOST, "-U", DB_USER, "-d", DB_NAME, "-f", DUMP_FILE_PATH]
    subprocess.run(restore_command, check=True)
    print("Restauración completada exitosamente.")

except subprocess.CalledProcessError as e:
    print(f"Ocurrió un error al ejecutar el comando: {e}")
    print("Asegúrate de que la base de datos de destino no exista y que los ejecutables de PostgreSQL estén en tu PATH.")

finally:
    # Eliminar la variable de entorno de la contraseña por seguridad
    del os.environ["PGPASSWORD"]