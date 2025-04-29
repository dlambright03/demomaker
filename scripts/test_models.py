"""
Test script generator with different AI models.

This script tests the script generator with different AI models to compare
their performance and output quality.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from src.modules.script_generator import ScriptGenerator


def get_api_key_from_env(provider_name):
    """Get API key from environment variables."""
    env_var_name = f"{provider_name.upper()}_API_KEY"
    return os.environ.get(env_var_name)


def test_model(model_name, images, description, output_dir):
    """Test a specific AI model with the script generator."""
    logger.info(f"\n=== Testing model: {model_name} ===")

    # Get API key if needed
    api_key = None
    if "gpt" in model_name or "openai" in model_name:
        api_key = get_api_key_from_env("openai")
        if not api_key:
            logger.warning("No OpenAI API key found in environment variables")

    # Create script generator with model
    generator = ScriptGenerator(
        {
            "model": model_name,
            "api_key": api_key,
        }
    )

    # Start timer
    start_time = time.time()

    try:
        # Generate script
        script = generator.generate_script(
            images=images,
            description=description,
            title=f"Test with {model_name}",
        )

        # End timer
        elapsed_time = time.time() - start_time

        # Print summary
        logger.info(f"Generation completed in {elapsed_time:.2f} seconds")
        logger.info(f"Generated {len(script.get('segments', []))} segments")
        logger.info(f"Total duration: {script.get('total_duration')} seconds")

        # Save script to file
        output_file = output_dir / f"script_{model_name.replace('-', '_')}.json"
        with open(output_file, "w") as f:
            json.dump(script, f, indent=2)

        logger.info(f"Script saved to: {output_file}")

        # Print first segment
        if script.get("segments"):
            logger.info(
                f"First segment narration: {script['segments'][0]['narration'][:100]}..."
            )

        return True

    except Exception as e:
        logger.error(f"Error testing model {model_name}: {str(e)}")
        return False


def main():
    """Test script generator with different AI models."""
    # Get test images
    data_dir = Path(__file__).parent.parent / "data" / "test_images"
    if not data_dir.exists():
        logger.error(f"Test images directory not found: {data_dir}")
        return 1

    images = list(data_dir.glob("*.png"))
    if not images:
        logger.error("No test images found")
        return 1

    logger.info(f"Found {len(images)} test images")

    # Create output directory
    output_dir = Path(__file__).parent.parent / "output" / "model_tests"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Description for script generation
    description = (
        "DemoMaker: an AI-powered tool for creating engaging demo videos from images "
        "with automated script generation, narration, and video assembly"
    )

    # Get available models
    generator = ScriptGenerator()
    available_models = generator.get_available_models()
    logger.info(f"Available models: {', '.join(available_models)}")

    # Test all models or just the local one if no API keys
    models_to_test = ["local-model"]
    if get_api_key_from_env("openai"):
        models_to_test.append("gpt-3.5-turbo")

    # Run tests
    results = {}
    for model in models_to_test:
        success = test_model(model, images, description, output_dir)
        results[model] = "Success" if success else "Failed"

    # Print summary
    logger.info("\n=== Test Results ===")
    for model, result in results.items():
        logger.info(f"{model}: {result}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
