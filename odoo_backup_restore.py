import os
import requests
import zipfile
import psycopg2
import subprocess
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

ODOO_USER = os.getenv("ODOO_USER")
ODOO_API_KEY = os.getenv("ODOO_API_KEY")
PROJECT = os.getenv("ODOO_PROJECT")

LOCAL_DB = os.getenv("LOCAL_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")

BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# ---------------------------
# 1. Descargar el dump más reciente
# ---------------------------
def download_backup():
    url = f"https://www.odoo.sh/project/{PROJECT}/branches/inscodemexico-insco-837013/backups"
    print(f"🔄 Descargando backups desde: {url}")

    r = requests.get(url, auth=(ODOO_USER, ODOO_API_KEY))
    r.raise_for_status()

    backups = r.json()
    latest = backups[0]["url"]  # el más reciente
    filename = os.path.join(BACKUP_DIR, backups[0]["filename"])

    print(f"⬇️ Descargando dump: {backups[0]['filename']}")
    with requests.get(latest, auth=(ODOO_USER, ODOO_API_KEY), stream=True) as response:
        response.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"✅ Backup descargado en {filename}")
    return filename

# ---------------------------
# 2. Extraer y restaurar
# ---------------------------
def restore_backup(zip_path):
    print("📦 Extrayendo dump...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(BACKUP_DIR)

    sql_file = None
    for file in os.listdir(BACKUP_DIR):
        if file.endswith(".sql"):
            sql_file = os.path.join(BACKUP_DIR, file)
            break

    if not sql_file:
        raise FileNotFoundError("❌ No se encontró archivo .sql en el backup")

    print(f"🔄 Restaurando en PostgreSQL → {LOCAL_DB}")

    # Crear la BD si no existe
    conn = psycopg2.connect(
        dbname="postgres",
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{LOCAL_DB}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {LOCAL_DB};")
        print(f"✅ Base de datos {LOCAL_DB} creada")
    cur.close()
    conn.close()

    # Restaurar dump
    cmd = [
        "psql",
        "-h", PG_HOST,
        "-p", PG_PORT,
        "-U", PG_USER,
        "-d", LOCAL_DB,
        "-f", sql_file
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = PG_PASSWORD
    subprocess.run(cmd, env=env, check=True)

    print(f"🎉 Restauración completada en {LOCAL_DB}")

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    print("🚀 Iniciando proceso de backup...")
    try:
        backup_file = download_backup()
        restore_backup(backup_file)
        print("✅ Proceso terminado correctamente")
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
