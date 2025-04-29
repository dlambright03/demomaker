"""
Demo of the Script Generator Module.

This script demonstrates the capabilities of the Script Generator module.
"""

import json
import logging
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.modules.script_generator import ScriptGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run the script generator demo."""
    # Get test image paths
    data_dir = Path(__file__).parent.parent / "data" / "test_images"

    # Make sure the test images directory exists
    if not data_dir.exists():
        logger.error(f"Test images directory not found: {data_dir}")
        return

    # Get all PNG images
    image_paths = list(data_dir.glob("*.png"))

    if not image_paths:
        logger.error("No test images found")
        return

    logger.info(f"Found {len(image_paths)} test images")

    # List available models
    script_generator = ScriptGenerator()
    models = script_generator.get_available_models()
    logger.info(f"Available models: {', '.join(models)}")

    # Generate script with default model
    description = "DemoMaker, an AI-powered script generation system"

    try:
        # Start with quick analysis
        logger.info("Analyzing images...")
        analyses = script_generator.analyze_images(image_paths)
        logger.info(f"Analysis complete: {len(analyses)} images analyzed")

        # Sample objects from first image
        if analyses and "objects" in analyses[0]:
            objects = analyses[0].get("objects", [])
            if objects:
                obj_names = [obj.get("name", "") for obj in objects[:3]]
                logger.info(f"First image objects: {', '.join(obj_names)}")

        # Estimate generation time
        num_images = len(image_paths)
        description_length = len(description)
        est_time = script_generator.estimate_generation_time(
            num_images, description_length
        )
        logger.info(f"Estimated generation time: {est_time} seconds")

        # Generate the script
        logger.info(f"Generating script...")
        script = script_generator.generate_script(
            images=image_paths,
            description=description,
            title="DemoMaker Script Generator Demo",
            target_duration=60,  # Target 60 seconds total
        )

        # Display script information
        logger.info("Script generation successful!")
        logger.info(f"Total duration: {script.get('total_duration')} seconds")
        logger.info(f"Number of segments: {len(script.get('segments', []))}")

        # Save the script to a JSON file
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)

        script_file = output_dir / "demo_script.json"
        with open(script_file, "w") as f:
            json.dump(script, f, indent=2)

        logger.info(f"Script saved to: {script_file}")

        # Print sample narration
        if script.get("segments"):
            logger.info("\nSample narrations:")
            for i, segment in enumerate(script["segments"]):
                if i > 0 and i < len(script["segments"]) - 1:
                    continue  # Skip middle segments
                position = "First" if i == 0 else "Last"
                logger.info(f"{position} segment: {segment['narration']}")

    except Exception as e:
        logger.error(f"Script generation failed: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()


def main():
    """Run the script generator demo."""
    # Get test image paths
    data_dir = Path(__file__).parent.parent / "data" / "test_images"

    # Make sure the test images directory exists
    if not data_dir.exists():
        logger.error(f"Test images directory not found: {data_dir}")
        return

    # Get all PNG images
    image_paths = list(data_dir.glob("*.png"))

    if not image_paths:
        logger.error("No test images found")
        return

    logger.info(f"Found {len(image_paths)} test images")

    # List available models
    script_generator = ScriptGenerator()
    models = script_generator.get_available_models()
    logger.info(f"Available models: {', '.join(models)}")

    # Generate script with default model
    description = "DemoMaker, an AI-powered script generation system"

    try:
        # Start with quick analysis
        logger.info("Analyzing images...")
        analyses = script_generator.analyze_images(image_paths)
        logger.info(f"Analysis complete: {len(analyses)} images analyzed")

        # Sample objects from first image
        if analyses and "objects" in analyses[0]:
            objects = analyses[0]["objects"]
            logger.info(
                f"First image objects: {', '.join(obj['name'] for obj in objects[:3])}"
            )

        # Estimate generation time
        num_images = len(image_paths)
        description_length = len(description)
        est_time = script_generator.estimate_generation_time(
            num_images, description_length
        )
        logger.info(f"Estimated generation time: {est_time} seconds")

        # Generate the script
        logger.info(f"Generating script...")
        script = script_generator.generate_script(
            images=image_paths,
            description=description,
            title="DemoMaker Script Generator Demo",
            target_duration=60,  # Target 60 seconds total
        )

        # Display script information
        logger.info("Script generation successful!")
        logger.info(f"Total duration: {script.get('total_duration'):.1f} seconds")
        logger.info(f"Number of segments: {len(script.get('segments', []))}")

        # Save the script to a JSON file
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)

        script_file = output_dir / "demo_script.json"
        with open(script_file, "w") as f:
            json.dump(script, f, indent=2)

        logger.info(f"Script saved to: {script_file}")

        # Print sample narration
        if script.get("segments"):
            logger.info("\nSample narrations:")
            for i, segment in enumerate(script["segments"]):
                if i > 0 and i < len(script["segments"]) - 1:
                    continue  # Skip middle segments
                position = "First" if i == 0 else "Last"
                logger.info(f"{position} segment: {segment['narration']}")

    except Exception as e:
        logger.error(f"Script generation failed: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
