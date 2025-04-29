"""
Local AI Provider implementation.

This module provides a local mock implementation of the AI provider interface
for testing and development purposes.
"""

import json
import logging
import random
import time
from typing import Any, Dict, List, Optional

from src.modules.script_generator.ai_providers.base_provider import BaseAIProvider

# Configure logging
logger = logging.getLogger(__name__)


class LocalProvider(BaseAIProvider):
    """Local mock implementation of AI provider for testing."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the local provider.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__("Local", config)
        self._delay = config.get("delay", 0.5)  # Simulation delay in seconds

    def analyze_image_content(self, image_data: bytes) -> Dict[str, Any]:
        """
        Mock image content analysis.

        Args:
            image_data: Binary image data to analyze

        Returns:
            Dictionary containing mock analysis results
        """
        # Simulate processing delay
        time.sleep(self._delay)

        # Generate mock objects
        objects = []
        num_objects = random.randint(2, 5)
        possible_objects = [
            {
                "name": "laptop",
                "position": {"x": 0.5, "y": 0.5},
                "size": {"width": 0.4, "height": 0.3},
                "confidence": 0.92,
            },
            {
                "name": "person",
                "position": {"x": 0.3, "y": 0.4},
                "size": {"width": 0.2, "height": 0.5},
                "confidence": 0.88,
            },
            {
                "name": "coffee cup",
                "position": {"x": 0.7, "y": 0.6},
                "size": {"width": 0.1, "height": 0.1},
                "confidence": 0.85,
            },
            {
                "name": "keyboard",
                "position": {"x": 0.5, "y": 0.7},
                "size": {"width": 0.3, "height": 0.1},
                "confidence": 0.9,
            },
            {
                "name": "monitor",
                "position": {"x": 0.5, "y": 0.3},
                "size": {"width": 0.4, "height": 0.3},
                "confidence": 0.95,
            },
            {
                "name": "smartphone",
                "position": {"x": 0.8, "y": 0.5},
                "size": {"width": 0.1, "height": 0.2},
                "confidence": 0.87,
            },
            {
                "name": "desk",
                "position": {"x": 0.5, "y": 0.8},
                "size": {"width": 0.9, "height": 0.2},
                "confidence": 0.93,
            },
        ]

        # Select random objects
        selected_indices = random.sample(
            range(len(possible_objects)), min(num_objects, len(possible_objects))
        )
        for idx in selected_indices:
            objects.append(possible_objects[idx])

        # Generate mock text content
        possible_texts = [
            "DemoMaker Pro",
            "Welcome to the demonstration",
            "AI-powered script generation",
            "Create engaging videos",
            "Automated video creation",
            "",  # Empty text
        ]
        text = random.choice(possible_texts)

        # Generate mock colors
        colors = {
            "blue": f"{random.randint(5, 30)}%",
            "white": f"{random.randint(20, 50)}%",
            "gray": f"{random.randint(10, 30)}%",
            "black": f"{random.randint(5, 20)}%",
        }

        # Generate mock composition
        compositions = [
            "Centered composition with main elements in focus",
            "Split screen layout with content on both sides",
            "Minimal design with ample white space",
            "Dense information display with multiple elements",
            "Header-content-footer structure",
        ]
        composition = random.choice(compositions)

        # Generate mock quality assessment
        qualities = [
            "High resolution image with excellent clarity",
            "Good quality image with clear details",
            "Medium quality with some compression artifacts",
            "High contrast with vibrant colors",
            "Well-lit scene with good exposure",
        ]
        quality = random.choice(qualities)

        # Return mock analysis
        return {
            "objects": objects,
            "text": text,
            "colors": colors,
            "composition": composition,
            "quality": quality,
        }

    def generate_script_from_images(
        self, image_analyses: List[Dict[str, Any]], description: str
    ) -> Dict[str, Any]:
        """
        Generate a mock script from a set of analyzed images.

        Args:
            image_analyses: List of image analysis results
            description: Description of the content for script generation

        Returns:
            Dictionary containing the generated script
        """
        # Simulate processing delay
        time.sleep(self._delay * len(image_analyses))

        # Create script segments based on analyses
        segments = []
        total_duration = 0

        for idx, analysis in enumerate(image_analyses):
            # Extract objects for narration
            objects = analysis.get("objects", [])
            object_names = [obj.get("name", "") for obj in objects]
            object_text = ", ".join(object_names) if object_names else "the interface"

            # Extract text for narration
            text = analysis.get("text", "")

            # Generate segment duration (5-15 seconds)
            duration = random.randint(8, 12)
            total_duration += duration

            # Generate narration text
            if idx == 0:
                # First segment - introduction
                narration = (
                    f"Welcome to this demonstration about {description}. "
                    f"Here we can see {object_text}."
                )
                if text:
                    narration += f" The text '{text}' highlights the key functionality."

            elif idx == len(image_analyses) - 1:
                # Last segment - conclusion
                narration = (
                    f"Finally, we can see {object_text}, which shows "
                    f"the finished result. This completes our demonstration of {description}."
                )
                if text:
                    narration += f" Remember that '{text}' is the core benefit."

            else:
                # Middle segments
                transitions = [
                    "Next, we have",
                    "Moving on to",
                    "Here we can see",
                    "This screen shows",
                    "Now let's look at",
                ]
                transition = random.choice(transitions)
                narration = f"{transition} {object_text}."

                if text:
                    narration += f" The text indicates '{text}'."

                features = [
                    "This feature streamlines the workflow.",
                    "Users can easily accomplish their tasks here.",
                    "This provides significant time savings.",
                    "The intuitive design makes this easy to use.",
                    "This demonstrates the power of the system.",
                ]
                narration += f" {random.choice(features)}"

            # Add segment to script
            segments.append(
                {
                    "id": f"segment-{idx+1}",
                    "image_index": idx,
                    "duration": duration,
                    "narration": narration,
                }
            )

        # Create full script
        script = {
            "title": f"Demo of {description}",
            "total_duration": total_duration,
            "segments": segments,
        }

        return script

    def is_available(self) -> bool:
        """
        Check if the local provider is available.

        Always returns True as the local provider is always available.
        """
        return True

    def initialize(self, api_key: Optional[str] = None, **kwargs) -> bool:
        """
        Initialize the local provider.

        Args:
            api_key: Not used for local provider
            kwargs: Additional configuration options

        Returns:
            Always returns True
        """
        # Set delay if provided
        if "delay" in kwargs:
            self._delay = kwargs["delay"]

        logger.info("Local AI provider initialized")
        return True
