"""
Script Generator Module.

This module provides the implementation of the script generator interface
for automatically generating coherent and engaging scripts from images.
"""

import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from PIL import Image

from src.interfaces.script_generator import (
    ImageAnalysisError,
    InvalidInputError,
    ModelNotAvailableError,
    ScriptGenerationError,
    ScriptGenerationTimeoutError,
    ScriptGeneratorInterface,
)
from src.modules.script_generator.ai_providers.factory import AIProviderFactory

# Configure logging
logger = logging.getLogger(__name__)


class ScriptGenerator(ScriptGeneratorInterface):
    """
    Script Generator implementation.

    Generates coherent and engaging scripts based on provided images and descriptions
    by leveraging AI models.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the script generator.

        Args:
            config: Optional configuration dictionary
        """
        self._config = config or {}
        self._model_name = self._config.get("model", "local-model")
        self._api_key = self._config.get("api_key")
        self._default_target_duration = self._config.get("default_target_duration", 60)
        self._provider = None
        self._cancel_requested = False
        self._generation_thread = None

        # Initialize the AI provider
        self._initialize_provider()

    def _initialize_provider(self) -> None:
        """Initialize the AI provider with the selected model."""
        try:
            self._provider = AIProviderFactory.create_provider(
                self._model_name,
                {"api_key": self._api_key},
            )
            logger.info(f"Initialized script generator with model: {self._model_name}")
        except Exception as e:
            logger.error(f"Error initializing provider: {str(e)}")
            # Fall back to local provider
            self._model_name = "local-model"
            self._provider = AIProviderFactory.create_provider(self._model_name)
            logger.info("Falling back to local provider")

    def generate_script(
        self,
        images: List[Union[str, Path, bytes]],
        description: str,
        title: Optional[str] = None,
        target_duration: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate a script based on provided images and description.

        Args:
            images: List of images (file paths, Path objects, or raw bytes)
            description: Description of the content for script generation
            title: Optional title for the script
            target_duration: Optional target duration in seconds for the script

        Returns:
            Dictionary containing the generated script with segments, timing, etc.

        Raises:
            InvalidInputError: If the input is invalid
            ImageAnalysisError: If image analysis fails
            ScriptGenerationError: If script generation fails
            ScriptGenerationTimeoutError: If script generation times out
        """
        if not images:
            raise InvalidInputError("No images provided")

        if not description:
            raise InvalidInputError("No description provided")

        if not self._provider:
            self._initialize_provider()

        if not self._provider.is_available():
            raise ModelNotAvailableError(f"Model {self._model_name} is not available")

        # Reset cancel flag
        self._cancel_requested = False

        try:
            # Analyze images
            image_analyses = self.analyze_images(images)

            # Generate script from analyses
            script = self._provider.generate_script_from_images(
                image_analyses, description
            )

            # Add title if provided
            if title:
                script["title"] = title

            # Adjust timing if target duration is specified
            if target_duration:
                script = self._adjust_timing(script, target_duration)

            return script

        except Exception as e:
            raise ScriptGenerationError(f"Script generation failed: {str(e)}") from e

    def analyze_images(
        self, images: List[Union[str, Path, bytes]]
    ) -> List[Dict[str, Any]]:
        """
        Analyze images to extract content information.

        Args:
            images: List of images (file paths, Path objects, or raw bytes)

        Returns:
            List of dictionaries containing analysis results for each image

        Raises:
            InvalidInputError: If input is invalid
            ImageAnalysisError: If image analysis fails
        """
        if not images:
            raise InvalidInputError("No images provided")

        if not self._provider:
            self._initialize_provider()

        if not self._provider.is_available():
            raise ModelNotAvailableError(f"Model {self._model_name} is not available")

        image_analyses = []

        try:
            for image in images:
                # Load image data
                image_data = self._load_image(image)

                # Analyze image content
                analysis = self._provider.analyze_image_content(image_data)
                image_analyses.append(analysis)

                # Check for cancellation
                if self._cancel_requested:
                    raise ScriptGenerationError("Image analysis cancelled")

            return image_analyses

        except Exception as e:
            raise ImageAnalysisError(f"Image analysis failed: {str(e)}") from e

    def _load_image(self, image: Union[str, Path, bytes]) -> bytes:
        """
        Load image data from various input types.

        Args:
            image: Image source (file path, Path object, or raw bytes)

        Returns:
            Raw image data as bytes

        Raises:
            InvalidInputError: If image cannot be loaded
        """
        try:
            # If image is already bytes, return it directly
            if isinstance(image, bytes):
                return image

            # If image is a string or Path, load it from file
            if isinstance(image, (str, Path)):
                image_path = Path(image)
                if not image_path.exists():
                    raise InvalidInputError(f"Image file not found: {image_path}")

                with open(image_path, "rb") as f:
                    return f.read()

            # Unknown input type
            raise InvalidInputError(f"Unsupported image type: {type(image)}")

        except Exception as e:
            raise InvalidInputError(f"Failed to load image: {str(e)}") from e

    def _adjust_timing(
        self, script: Dict[str, Any], target_duration: int
    ) -> Dict[str, Any]:
        """
        Adjust timing of script segments to match the target duration.

        Args:
            script: Generated script with segments
            target_duration: Target duration in seconds

        Returns:
            Adjusted script with updated timing
        """
        segments = script.get("segments", [])
        if not segments:
            return script

        # Calculate current total duration
        current_duration = script.get("total_duration", 0)
        if current_duration == 0:
            # Calculate from segments
            current_duration = sum(segment.get("duration", 0) for segment in segments)

        # Skip if target matches current
        if current_duration == target_duration:
            return script

        # Calculate adjustment factor
        adjustment_factor = target_duration / current_duration

        # Adjust each segment
        adjusted_segments = []
        adjusted_total = 0

        for segment in segments:
            original_duration = segment.get("duration", 0)
            adjusted_duration = round(original_duration * adjustment_factor)

            # Ensure at least 3 seconds per segment
            adjusted_duration = max(3, adjusted_duration)

            # Create adjusted segment
            adjusted_segment = segment.copy()
            adjusted_segment["duration"] = adjusted_duration
            adjusted_segments.append(adjusted_segment)

            adjusted_total += adjusted_duration

        # Update script with adjusted segments and total
        adjusted_script = script.copy()
        adjusted_script["segments"] = adjusted_segments
        adjusted_script["total_duration"] = adjusted_total

        return adjusted_script

    def set_ai_model(self, model_name: str) -> bool:
        """
        Set the AI model to use for script generation.

        Args:
            model_name: Name of the model

        Returns:
            True if model was set successfully, False otherwise

        Raises:
            ModelNotAvailableError: If the model is not available
        """
        if model_name == self._model_name and self._provider:
            return True

        try:
            # Check if model is available
            available_models = self.get_available_models()
            if model_name not in available_models:
                raise ModelNotAvailableError(f"Model {model_name} is not available")

            # Set model and reinitialize provider
            self._model_name = model_name
            self._initialize_provider()

            return self._provider.is_available()

        except Exception as e:
            logger.error(f"Error setting AI model: {str(e)}")
            raise ModelNotAvailableError(f"Failed to set model {model_name}") from e

    def get_available_models(self) -> List[str]:
        """
        Get a list of available AI models.

        Returns:
            List of available model names
        """
        return AIProviderFactory.get_available_models()

    def estimate_generation_time(
        self, num_images: int, description_length: int
    ) -> float:
        """
        Estimate the time required for script generation.

        Args:
            num_images: Number of images
            description_length: Length of the description text

        Returns:
            Estimated time in seconds
        """
        # Base time for processing
        base_time = 2.0

        # Time per image
        image_time = 1.5 * num_images

        # Time based on description length
        desc_time = description_length / 200.0

        # Model-specific multiplier
        model_multiplier = 1.0
        if "gpt-4" in self._model_name:
            model_multiplier = 3.0
        elif "gpt-3.5" in self._model_name:
            model_multiplier = 2.0
        elif "local" in self._model_name:
            model_multiplier = 0.5

        # Calculate total estimated time
        estimated_time = (base_time + image_time + desc_time) * model_multiplier

        return round(estimated_time, 1)

    def cancel_generation(self) -> bool:
        """
        Cancel an in-progress script generation.

        Returns:
            True if cancellation was successful, False otherwise
        """
        if self._generation_thread and self._generation_thread.is_alive():
            self._cancel_requested = True
            return True

        return False
