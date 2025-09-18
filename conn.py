# Protocolo XML-RPC
import xmlrpc.client

# Datos de conexión
url = "https://inscodemexico.odoo.com/"
db = "inscodemexico-insco-837013"
username = "miguel.almarales@inscomexico.com"
#password = "RegEdit#45/15"
password = "e7ccddd32c36fb8e191b56b0b2c4ee766dc3eb70"

# Autenticación
common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
print(common.version())

uid = common.authenticate(db, username, password, {})
print("UID:", uid)



