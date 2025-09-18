"""
Módulo de conexión principal a Odoo
"""
import json
import requests
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class OdooConnection:
    """Clase para manejar conexiones a Odoo via JSON-RPC"""
    
    def __init__(self, url: str, db: str, user: str, api_key: str):
        """
        Inicializar conexión a Odoo
        
        Args:
            url: URL de la instancia de Odoo
            db: Nombre de la base de datos
            user: Usuario de Odoo
            api_key: API Key de Odoo
        """
        self.url = url.rstrip('/')
        self.db = db
        self.user = user
        self.api_key = api_key
        self.jsonrpc_url = f"{self.url}/jsonrpc"
        self.uid = None
        
    def authenticate(self) -> bool:
        """Autentica el usuario y obtiene el UID"""
        try:
            result = self._jsonrpc_request("common", "authenticate", 
                                         [self.db, self.user, self.api_key, {}])
            self.uid = result
            return bool(self.uid)
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            return False
    
    def _jsonrpc_request(self, service: str, method: str, args: List) -> Any:
        """Ejecuta request JSON-RPC"""
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": args
            },
            "id": 1
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.jsonrpc_url, 
                               headers=headers, 
                               data=json.dumps(payload))
        response.raise_for_status()
        
        result = response.json()
        if "error" in result:
            raise Exception(f"Odoo Error: {result['error']}")
            
        return result.get("result")
    
    def execute_kw(self, model: str, method: str, args: List, kwargs: Dict = None) -> Any:
        """Ejecuta método en modelo de Odoo"""
        if not self.uid:
            if not self.authenticate():
                raise Exception("No se pudo autenticar")
        
        call_args = [self.db, self.uid, self.api_key, model, method, args]
        if kwargs:
            call_args.append(kwargs)
            
        return self._jsonrpc_request("object", "execute_kw", call_args)
    
    def search_read(self, model: str, domain: List = None, 
                   fields: List = None, limit: int = None) -> List[Dict]:
        """Busca y lee registros de un modelo"""
        args = [domain or []]
        kwargs = {}
        if fields:
            kwargs['fields'] = fields
        if limit:
            kwargs['limit'] = limit
            
        return self.execute_kw(model, 'search_read', args, kwargs)
    
    def create(self, model: str, values: Dict) -> int:
        """Crea un nuevo registro"""
        return self.execute_kw(model, 'create', [values])
    
    def write(self, model: str, ids: List[int], values: Dict) -> bool:
        """Actualiza registros existentes"""
        return self.execute_kw(model, 'write', [ids, values])
    
    def unlink(self, model: str, ids: List[int]) -> bool:
        """Elimina registros"""
        return self.execute_kw(model, 'unlink', [ids])
