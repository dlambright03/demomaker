#!/usr/bin/env python3
"""
Simple test for the Script Generator module.
"""

import json
import logging
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.modules.script_generator import ScriptGenerator


def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("test_script")

    # Define test images
    image_dir = Path(__file__).parent.parent / "data" / "test_images"
    images = list(image_dir.glob("*.png"))

    if not images:
        logger.error("No test images found")
        return 1

    logger.info(f"Found {len(images)} test images: {[img.name for img in images]}")

    # Create script generator
    generator = ScriptGenerator({"model": "local-model"})

    # Generate script
    script = generator.generate_script(
        images=images,
        description="This is a simple test of the Script Generator module",
    )

    # Save script to file
    output_path = Path(__file__).parent.parent / "data" / "test_script.json"
    with open(output_path, "w") as f:
        json.dump(script, f, indent=2)

    logger.info(f"Script saved to {output_path}")

    # Print summary
    print("\nGenerated script summary:")
    print(f"Title: {script['title']}")
    print(f"Duration: {script['total_duration']} seconds")
    print(f"Segments: {len(script['segments'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
