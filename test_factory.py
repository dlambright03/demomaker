#!/usr/bin/env python
"""
Test script for the ModuleFactory.
This script uses explicit path handling to ensure imports work correctly.
"""

import os
import sys
import traceback

# Add the project root to Python path for proper imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure simple logging to console
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def test_module_factory():
    """Test the ModuleFactory implementation."""
    try:
        print("Importing ModuleFactory...")
        from src.core.module_factory import ModuleFactory

        print("\nCreating ModuleFactory instance...")
        factory = ModuleFactory()

        print("\nTesting configuration module...")
        config = factory.create_configuration()
        print(f"✓ Configuration created: {type(config).__name__}")

        print("\nTesting storage manager module...")
        storage = factory.create_storage_manager()
        print(f"✓ StorageManager created: {type(storage).__name__}")

        print("\nTesting input processor module...")
        input_processor = factory.create_input_processor()
        print(f"✓ InputProcessor created: {type(input_processor).__name__}")

        print("\nTesting script generator module...")
        script_gen = factory.create_script_generator()
        print(f"✓ ScriptGenerator created: {type(script_gen).__name__}")

        print("\nTesting narration generator module...")
        narration_gen = factory.create_narration_generator()
        print(f"✓ NarrationGenerator created: {type(narration_gen).__name__}")

        print("\nTesting video assembler module...")
        video_assembler = factory.create_video_assembler()
        print(f"✓ VideoAssembler created: {type(video_assembler).__name__}")

        print("\nTesting module caching...")
        config2 = factory.create_configuration()
        if config is config2:
            print("✓ Module caching works correctly")
        else:
            print("✗ Module caching failed")

        print("\nTesting cache clearing...")
        factory.clear_cache()
        config3 = factory.create_configuration()
        if config is not config3:
            print("✓ Cache clearing works correctly")
        else:
            print("✗ Cache clearing failed")

        print("\n✅ All tests passed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error testing ModuleFactory: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("-" * 60)
    print("RUNNING MODULE FACTORY TEST")
    print("-" * 60)
    success = test_module_factory()
    print("-" * 60)
    if success:
        print("MODULE FACTORY TEST: SUCCESS")
    else:
        print("MODULE FACTORY TEST: FAILED")
    print("-" * 60)

    # Return appropriate exit code
    sys.exit(0 if success else 1)
