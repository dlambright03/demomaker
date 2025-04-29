"""
Generate script from images.

This script generates a script from a set of images using the Script Generator module.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.modules.script_generator import ScriptGenerator


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a script from images using AI"
    )

    parser.add_argument(
        "--images",
        "-i",
        type=str,
        nargs="+",
        help="Paths to image files to use for script generation",
    )

    parser.add_argument(
        "--description",
        "-d",
        type=str,
        required=True,
        help="Description of the content for script generation",
    )

    parser.add_argument(
        "--title", "-t", type=str, help="Title for the generated script"
    )

    parser.add_argument(
        "--duration",
        "-dur",
        type=int,
        help="Target duration in seconds for the generated script",
    )

    parser.add_argument(
        "--model", "-m", type=str, help="AI model to use for script generation"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="script.json",
        help="Output file path for the generated script (default: script.json)",
    )

    parser.add_argument(
        "--test-images",
        action="store_true",
        help="Use test images from data/test_images directory",
    )

    return parser.parse_args()


def main():
    """Generate a script from images."""
    args = parse_arguments()

    # Initialize script generator
    generator = ScriptGenerator()

    # Set AI model if specified
    if args.model:
        try:
            generator.set_ai_model(args.model)
            logger.info(f"Using AI model: {args.model}")
        except Exception as e:
            logger.error(f"Error setting AI model: {str(e)}")
            logger.info(
                f"Available models: {', '.join(generator.get_available_models())}"
            )
            return 1

    # Get image paths
    image_paths = []

    if args.test_images:
        # Use test images
        test_dir = Path(__file__).parent.parent / "data" / "test_images"
        if not test_dir.exists():
            logger.error(f"Test images directory not found: {test_dir}")
            return 1

        image_paths = list(test_dir.glob("*.png"))
        if not image_paths:
            logger.error("No test images found")
            return 1

        logger.info(f"Using {len(image_paths)} test images")

    elif args.images:
        # Use specified images
        for img_path in args.images:
            path = Path(img_path)
            if not path.exists():
                logger.error(f"Image not found: {path}")
                return 1

            image_paths.append(path)

        logger.info(f"Using {len(image_paths)} specified images")

    else:
        logger.error("No images specified. Use --images or --test-images")
        return 1

    # Generate script
    try:
        # Estimate generation time
        est_time = generator.estimate_generation_time(
            len(image_paths), len(args.description)
        )
        logger.info(f"Estimated generation time: {est_time} seconds")

        # Generate script
        logger.info("Generating script...")
        script = generator.generate_script(
            images=image_paths,
            description=args.description,
            title=args.title,
            target_duration=args.duration,
        )

        # Save script to file
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(script, f, indent=2)

        logger.info(f"Script saved to: {output_path}")

        # Print summary
        logger.info(f"Generated script with {len(script.get('segments', []))} segments")
        logger.info(f"Total duration: {script.get('total_duration')} seconds")

        # Print first segment narration
        if script.get("segments"):
            first_segment = script["segments"][0]
            logger.info(
                f"First segment narration: {first_segment.get('narration', '')[:100]}..."
            )

        return 0

    except Exception as e:
        logger.error(f"Error generating script: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
