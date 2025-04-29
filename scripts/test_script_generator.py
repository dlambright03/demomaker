#!/usr/bin/env python3
"""
Test script for the Script Generator module.

This script demonstrates the basic functionality of the Script Generator module
and tests it with different model settings and inputs.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.modules.script_generator import ScriptGenerator


def setup_logging(level=logging.INFO):
    """Set up logging configuration."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test the Script Generator module")
    parser.add_argument(
        "--images",
        "-i",
        type=str,
        nargs="+",
        default=None,
        help="Paths to images to include in the script (default: use test images)",
    )
    parser.add_argument(
        "--description",
        "-d",
        type=str,
        default="Test script for a demonstration of the DemoMaker Script Generator",
        help="Description of the demo content",
    )
    parser.add_argument("--title", "-t", type=str, help="Title of the demo (optional)")
    parser.add_argument(
        "--duration", "-D", type=int, help="Target duration in seconds (optional)"
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="local-model",
        help="AI model to use (default: local-model)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="script_output.json",
        help="Output file for the generated script (default: script_output.json)",
    )
    parser.add_argument(
        "--create-test-images",
        action="store_true",
        help="Create test images if none are provided",
    )

    return parser.parse_args()


def create_test_images(count=3, output_dir=None):
    """Create test images for the script generator."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        logging.error(
            "Pillow is required to create test images. Install with: pip install pillow"
        )
        return []

    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data" / "test_images"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    image_paths = []
    for i in range(count):
        # Create a new image
        img = Image.new("RGB", (640, 480), color=(i * 40, 0, 120))
        draw = ImageDraw.Draw(img)

        # Add some text
        text = f"Test Image {i+1}"
        text_pos = (320, 240)
        draw.text(text_pos, text, fill=(255, 255, 255), anchor="mm")

        # Save the image
        img_path = os.path.join(output_dir, f"test_img_{i+1}.png")
        img.save(img_path)
        image_paths.append(Path(img_path))
        logging.info(f"Created test image: {img_path}")

    return image_paths


def test_script_generator(args):
    """Test the ScriptGenerator with given arguments."""
    logger = logging.getLogger("script_generator_test")

    # Create test images if necessary
    if args.images is None or not args.images:
        if args.create_test_images:
            image_paths = create_test_images()
            if not image_paths:
                logger.error("Failed to create test images")
                return 1
        else:
            # Use existing test images
            test_dir = Path(__file__).parent.parent / "data" / "test_images"
            if not test_dir.exists():
                logger.error(f"Test images directory does not exist: {test_dir}")
                logger.error(
                    "Provide images with --images or create test images with --create-test-images"
                )
                return 1

            image_paths = list(test_dir.glob("*.png"))
            if not image_paths:
                logger.error(f"No PNG images found in {test_dir}")
                return 1
    else:
        # Use provided image paths
        image_paths = []
        for img_path in args.images:
            path = Path(img_path)
            if not path.exists():
                logger.error(f"Image path does not exist: {path}")
                return 1
            image_paths.append(path)

    logger.info(f"Using {len(image_paths)} images for script generation")

    # Create script generator
    config = {"model": args.model}
    script_generator = ScriptGenerator(config)

    # List available models
    logger.info(f"Available models: {script_generator.get_available_models()}")
    logger.info(f"Using model: {args.model}")

    # Estimate generation time
    est_time = script_generator.estimate_generation_time(
        len(image_paths), len(args.description)
    )
    logger.info(f"Estimated generation time: {est_time} seconds")

    # Generate script
    try:
        start_time = time.time()
        script = script_generator.generate_script(
            images=image_paths,
            description=args.description,
            title=args.title,
            target_duration=args.duration,
        )
        elapsed = time.time() - start_time

        # Format the script as JSON
        script_json = json.dumps(script, indent=2)

        # Output the script
        output_path = args.output
        with open(output_path, "w") as f:
            f.write(script_json)
        logger.info(
            f"Script generated in {elapsed:.2f} seconds (estimated: {est_time}s)"
        )
        logger.info(f"Script written to: {output_path}")

        # Print summary
        print("\nScript Summary:")
        print(f"Title: {script['title']}")
        print(f"Duration: {script['total_duration']} seconds")
        print(f"Number of segments: {len(script['segments'])}")
        print(f"Model used: {script['metadata']['model']}")

        return 0

    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        return 1


def main():
    """Run the script generator test."""
    # Set up logging
    setup_logging()

    # Parse arguments
    args = parse_arguments()

    # Run the test
    return test_script_generator(args)


if __name__ == "__main__":
    sys.exit(main())
