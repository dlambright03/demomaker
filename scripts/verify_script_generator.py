"""
Verify Script Generator Module.

This script verifies that the Script Generator module is working correctly with
its required dependencies.
"""

import importlib
import logging
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def check_imports():
    """Check that all required imports are available."""
    required_modules = [
        "src.modules.script_generator",
        "src.interfaces.script_generator",
        "PIL",  # For image handling
    ]

    optional_modules = [
        "openai",  # For OpenAI provider
    ]

    # Check required modules
    logger.info("Checking required modules...")
    all_required_available = True

    for module_name in required_modules:
        try:
            importlib.import_module(module_name)
            logger.info(f"✓ {module_name} is available")
        except ImportError as e:
            logger.error(f"✗ {module_name} is not available: {str(e)}")
            all_required_available = False

    # Check optional modules
    logger.info("\nChecking optional modules...")

    for module_name in optional_modules:
        try:
            importlib.import_module(module_name)
            logger.info(f"✓ {module_name} is available")
        except ImportError:
            logger.warning(f"⚠ {module_name} is not available (optional)")

    return all_required_available


def check_script_generator():
    """Check that the script generator can be instantiated and used."""
    try:
        from src.modules.script_generator import ScriptGenerator

        # Create instance
        generator = ScriptGenerator()
        logger.info("✓ ScriptGenerator instance created")

        # Check methods
        methods = [
            "generate_script",
            "set_ai_model",
            "get_available_models",
            "estimate_generation_time",
            "cancel_generation",
            "analyze_images",
        ]

        for method_name in methods:
            if not hasattr(generator, method_name):
                logger.error(f"✗ ScriptGenerator is missing method: {method_name}")
                return False

        logger.info(f"✓ ScriptGenerator has all required methods")

        # Check models
        models = generator.get_available_models()
        logger.info(f"✓ Available models: {', '.join(models)}")

        return True

    except Exception as e:
        logger.error(f"✗ Error checking ScriptGenerator: {str(e)}")
        return False


def check_test_images():
    """Check that test images are available."""
    data_dir = Path(__file__).parent.parent / "data" / "test_images"

    if not data_dir.exists():
        logger.error(f"✗ Test images directory not found: {data_dir}")
        return False

    # Get all PNG images
    image_paths = list(data_dir.glob("*.png"))

    if not image_paths:
        logger.error("✗ No test images found")
        return False

    logger.info(f"✓ Found {len(image_paths)} test images")
    return True


def main():
    """Verify the script generator module."""
    logger.info("Verifying Script Generator Module...")

    # Check imports
    if not check_imports():
        logger.error("✗ Required imports check failed")
        return False

    # Check script generator
    if not check_script_generator():
        logger.error("✗ Script generator check failed")
        return False

    # Check test images
    if not check_test_images():
        logger.error("✗ Test images check failed")
        return False

    # All checks passed
    logger.info("\n✓ All checks passed. Script Generator module is working correctly.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
