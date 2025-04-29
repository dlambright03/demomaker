"""
Simple test script for the script generator module.

This script tests the basic functionality of the script generator module.
"""

import logging
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.modules.script_generator import ScriptGenerator


def test_script_generator():
    """Simple test of script generator functionality."""
    # Initialize script generator
    generator = ScriptGenerator()

    # Get test images
    data_dir = Path(__file__).parent.parent / "data" / "test_images"
    if not data_dir.exists():
        logger.error(f"Test images directory not found: {data_dir}")
        return 1

    # Get all PNG images
    image_paths = list(data_dir.glob("*.png"))
    if not image_paths:
        logger.error("No test images found")
        return 1

    logger.info(f"Found {len(image_paths)} test images")

    # Generate script
    try:
        script = generator.generate_script(
            images=image_paths,
            description="Simple test of script generation",
            title="Test Script",
        )

        # Display script information
        logger.info(f"Generated script with {len(script['segments'])} segments")
        logger.info(f"Total duration: {script['total_duration']} seconds")

        # Display first segment
        if script["segments"]:
            first_segment = script["segments"][0]
            logger.info(f"First segment narration: {first_segment['narration']}")

        return 0

    except Exception as e:
        logger.error(f"Error testing script generator: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(test_script_generator())
