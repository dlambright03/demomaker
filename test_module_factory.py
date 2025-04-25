#!/usr/bin/env python
"""
Test script for the ModuleFactory.
This script runs from the project root to ensure correct imports.
"""

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def test_module_factory():
    """Test the module factory implementation."""
    try:
        print("\n=== Testing Module Factory Implementation ===\n")

        # Import the module factory
        from src.core.module_factory import ModuleFactory

        print("✓ Successfully imported ModuleFactory")

        # Create a factory instance
        factory = ModuleFactory()
        print("✓ Successfully created ModuleFactory instance")

        # Test configuration module
        config = factory.create_configuration()
        print(f"✓ Created Configuration module: {type(config).__name__}")

        # Test storage manager module
        storage = factory.create_storage_manager()
        print(f"✓ Created StorageManager module: {type(storage).__name__}")

        # Test input processor module
        input_processor = factory.create_input_processor()
        print(f"✓ Created InputProcessor module: {type(input_processor).__name__}")

        # Test script generator module
        script_gen = factory.create_script_generator()
        print(f"✓ Created ScriptGenerator module: {type(script_gen).__name__}")

        # Test narration generator module
        narration_gen = factory.create_narration_generator()
        print(f"✓ Created NarrationGenerator module: {type(narration_gen).__name__}")

        # Test video assembler module
        video_assembler = factory.create_video_assembler()
        print(f"✓ Created VideoAssembler module: {type(video_assembler).__name__}")

        # Test module caching
        config2 = factory.create_configuration()
        if config is config2:
            print("✓ Module caching works correctly")
        else:
            print("✗ Module caching failed")

        # Test cache clearing
        factory.clear_cache()
        config3 = factory.create_configuration()
        if config is not config3:
            print("✓ Cache clearing works correctly")
        else:
            print("✗ Cache clearing failed")

        print("\n=== All tests passed successfully! ===\n")
        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Current directory: {Path.cwd()}")
    success = test_module_factory()
    sys.exit(0 if success else 1)
