"""
Simple test for the script generator module.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging

from src.modules.script_generator.ai_script_generator import ScriptGenerator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Test images directory
data_dir = Path(__file__).parent.parent / "data" / "test_images"
images = list(data_dir.glob("*.png"))

print(f"Found {len(images)} test images")

# Create script generator
generator = ScriptGenerator()

# Generate a script
try:
    script = generator.generate_script(
        images=images,
        description="DemoMaker AI Script Generator Test",
        title="Test Script",
    )

    print("\nGenerated Script:")
    print(f"- Title: {script.get('title')}")
    print(f"- Duration: {script.get('total_duration')} seconds")
    print(f"- Segments: {len(script.get('segments', []))}")

    # Print the first segment
    if script.get("segments"):
        print("\nFirst Segment:")
        print(f"- Start Time: {script['segments'][0]['start_time']}")
        print(f"- Duration: {script['segments'][0]['duration']}")
        print(f"- Narration: {script['segments'][0]['narration']}")

    print("\nScript generation successful!")

except Exception as e:
    print(f"Error: {str(e)}")
