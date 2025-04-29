"""
Script Generator Interface.

This module defines the interface for script generators in the DemoMaker system.
"""

import abc
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class ScriptGenerationError(Exception):
    """Base class for script generation errors."""

    pass


class InvalidInputError(ScriptGenerationError):
    """Error raised when input to script generator is invalid."""

    pass


class ImageAnalysisError(ScriptGenerationError):
    """Error raised when image analysis fails."""

    pass


class ModelNotAvailableError(ScriptGenerationError):
    """Error raised when requested AI model is not available."""

    pass


class ScriptGenerationTimeoutError(ScriptGenerationError):
    """Error raised when script generation times out."""

    pass


class ScriptGeneratorInterface(abc.ABC):
    """Interface for script generators."""

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get a list of available AI models.

        Returns:
            List of available model names
        """
        pass

    @abc.abstractmethod
    def estimate_generation_time(
        self, num_images: int, description_length: int
    ) -> float:
        """
        Estimate the time required for script generation.

        Args:
            num_images: Number of images to process
            description_length: Length of the description text

        Returns:
            Estimated time in seconds
        """
        pass

    @abc.abstractmethod
    def cancel_generation(self) -> bool:
        """
        Cancel an in-progress script generation.

        Returns:
            True if cancellation was successful, False otherwise
        """
        pass
