"""
Simple test to verify that the module factory can be imported.
"""

import sys

print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    print("Attempting to import ModuleFactory...")
    from src.core.module_factory import ModuleFactory

    print("Successfully imported ModuleFactory")
except Exception as e:
    print(f"Error importing ModuleFactory: {str(e)}")
    import traceback

    traceback.print_exc()
