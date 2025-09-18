"""
Módulo principal para conexión con API de Odoo
"""

from .connection import OdooConnection
from .auth import OdooAuth
from .models import OdooModel, Partner, Product, SaleOrder
from .utils import OdooUtils

__all__ = [
    'OdooConnection', 
    'OdooAuth', 
    'OdooModel', 
    'Partner', 
    'Product', 
    'SaleOrder',
    'OdooUtils'
]
