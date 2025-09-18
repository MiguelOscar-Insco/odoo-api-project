import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# URLs a probar
urls_to_test = [
    "https://inscodemexico.odoo.com",
    "https://inscodemexico-insco.odoo.com",
    "https://inscodemexico.odoo.sh",
    "https://inscodemexico-insco.odoo.sh"
]

# Tus credenciales
ODOO_USER = "miguel.almarales@inscomexico.com"
ODOO_API_KEY = os.getenv("ODOO_API_KEY")  # Lee desde .env

def test_url_access(url):
    """Prueba si una URL está accesible"""
    try:
        print(f"\n🔍 Probando: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            if "odoo" in response.text.lower():
                print(f"✅ ¡ÉXITO! {url} es una instancia de Odoo activa")
                return True
            else:
                print(f"⚠️  {url} responde pero no parece ser Odoo")
        else:
            print(f"❌ {url} -> Status: {response.status_code}")
        return False
        
    except requests.RequestException as e:
        print(f"❌ {url} -> Error: {e}")
        return False

def test_jsonrpc(url, db_name):
    """Prueba la conexión JSON-RPC"""
    try:
        jsonrpc_url = f"{url}/jsonrpc"
        print(f"🔍 Probando JSON-RPC: {jsonrpc_url}")
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "version",
                "args": []
            },
            "id": 1
        }
        
        response = requests.post(jsonrpc_url, headers=headers, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            version = result.get("result", {})
            print(f"✅ JSON-RPC funciona! Versión: {version}")
            return True
        else:
            print(f"❌ JSON-RPC falló: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error JSON-RPC: {e}")
        return False

def test_authentication(url, db_name):
    """Prueba autenticación (solo si tienes API key)"""
    if not ODOO_API_KEY:
        print("⚠️  No se puede probar autenticación sin API Key en el archivo .env")
        return False
        
    try:
        jsonrpc_url = f"{url}/jsonrpc"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [db_name, ODOO_USER, ODOO_API_KEY, {}]
            },
            "id": 1
        }
        
        response = requests.post(jsonrpc_url, headers=headers, data=json.dumps(payload))
        result = response.json()
        uid = result.get("result")
        
        if uid:
            print(f"✅ Autenticación exitosa! UID: {uid}")
            return True
        else:
            print("❌ Autenticación falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 BUSCANDO TU INSTANCIA DE ODOO")
    print("=" * 60)
    
    working_urls = []
    
    for url in urls_to_test:
        if test_url_access(url):
            working_urls.append(url)
            
            # Probar JSON-RPC
            db_possible_names = [
                "inscodemexico",
                "inscodemexico-insco", 
                url.replace("https://", "").replace(".odoo.com", "").replace(".odoo.sh", "")
            ]
            
            for db_name in db_possible_names:
                print(f"\n📊 Probando con DB: {db_name}")
                if test_jsonrpc(url, db_name):
                    print(f"\n🎯 CONFIGURACIÓN ENCONTRADA:")
                    print(f"   URL: {url}")
                    print(f"   DB: {db_name}")
                    
                    # Probar autenticación si hay API key
                    test_authentication(url, db_name)
                    
                    print(f"\n📝 ACTUALIZA TU ARCHIVO .env:")
                    print(f"ODOO_URL={url}")
                    print(f"ODOO_DB={db_name}")
                    print(f"ODOO_USER={ODOO_USER}")
                    print(f"ODOO_API_KEY=tu_api_key_aqui")
                    
                    return
        
        print("-" * 40)
    
    if not working_urls:
        print("\n❌ No se encontraron instancias accesibles")
        print("\n🔍 Verifica en tu panel de Odoo.sh:")
        print("   1. Que tu instancia esté activa")
        print("   2. La URL exacta de acceso")

if __name__ == "__main__":
    main()