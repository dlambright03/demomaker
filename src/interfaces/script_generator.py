"""
Interface for the Script Generator Module.

This module is responsible for generating a structured script from
user-provided images and descriptions using AI models.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any


class ScriptGeneratorInterface(ABC):
    """Interface for the Script Generator Module."""
    
    @abstractmethod
    def generate_script(self, 
                       images: List[Path], 
                       description: str, 
                       title: Optional[str] = None,
                       target_duration: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate a structured script based on the provided images and description.
        
        Args:
            images: List of validated image Path objects
            description: Text description of the demo content
            title: Title of the demo (optional)
            target_duration: Target duration in seconds (optional)
            
        Returns:
            A dictionary containing the generated script with timing information
            
        Raises:
            ScriptGenerationError: If script generation fails
        """
        pass
    
    @abstractmethod
    def set_ai_model(self, model_name: str) -> None:
        """
        Set the AI model to use for script generation.
        
        Args:
            model_name: The name of the AI model to use
            
        Raises:
            ValueError: If the model name is invalid or unavailable
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get a list of available AI models for script generation.
        
        Returns:
            A list of available model names
        """
        pass
    
    @abstractmethod
    def estimate_generation_time(self, 
                               num_images: int, 
                               description_length: int) -> int:
        """
        Estimate the time required to generate a script.
        
        Args:
            num_images: Number of images in the input
            description_length: Length of the description in characters
            
        Returns:
            Estimated time in seconds
        """
        pass
    
    @abstractmethod
    def cancel_generation(self) -> bool:
        """
        Cancel an ongoing script generation process.
        
        Returns:
            True if cancellation was successful, False otherwise
        """
        pass
