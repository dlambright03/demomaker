#!/usr/bin/env python3
"""
Test script to verify Configuration imports.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print(f"Python path: {sys.path}")

try:
    # Try direct import from module
    from src.modules.configuration.config_manager import Configuration

    print("Direct import successful!")

    # Create an instance to verify it works
    config = Configuration()
    print(f"Environment: {config.get_environment()}")

    # Reset the import cache to ensure clean import
    import importlib

    if "src.modules.configuration" in sys.modules:
        del sys.modules["src.modules.configuration"]

    # Try import via __init__.py
    from src.modules.configuration import Configuration

    print("Package import successful!")
except Exception as e:
    print(f"Import error: {e}")
    import traceback

    traceback.print_exc()
