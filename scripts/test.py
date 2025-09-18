#!/usr/bin/env python3
"""
Script para ejecutar pruebas del proyecto
"""

import sys
import unittest
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def run_tests():
    """Ejecuta todas las pruebas"""
    # Descobrir y ejecutar pruebas
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent.parent / 'tests'
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
