import pandas as pd
from sqlalchemy import create_engine

# Conexión a PostgreSQL con SQLAlchemy
db_name = "odoo_backup_restored"
db_user = "postgres"
db_password = "root"
db_host = "localhost"

# Crear motor de conexión
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}")

# Ejemplo: leer clientes/proveedores de Odoo
query = "SELECT id, name, email FROM res_partner LIMIT 10;"
df = pd.read_sql(query, engine)

print(df)
