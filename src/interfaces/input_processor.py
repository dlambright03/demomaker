"""
Interface for the Input Processor Module.

This module is responsible for handling command-line arguments,
validating user inputs, and processing user-provided images.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Union, Any


class InputProcessorInterface(ABC):
    """Interface for the Input Processor Module."""
    
    @abstractmethod
    def validate_images(self, image_paths: Union[str, List[str]]) -> List[Path]:
        """
        Validate that the provided image paths exist and are of supported formats.
        
        Args:
            image_paths: A directory containing images or a list of image paths
            
        Returns:
            A list of validated image Path objects
            
        Raises:
            ValueError: If any image path is invalid or of an unsupported format
        """
        pass
    
    @abstractmethod
    def extract_image_metadata(self, image_paths: List[Path]) -> List[Dict[str, Any]]:
        """
        Extract metadata from the provided images.
        
        Args:
            image_paths: A list of validated image Path objects
            
        Returns:
            A list of dictionaries containing metadata for each image
            (resolution, aspect ratio, etc.)
        """
        pass
    
    @abstractmethod
    def process_create_command(self, 
                             images: Union[str, List[str]], 
                             output: str, 
                             description: str, 
                             title: Optional[str] = None,
                             duration: Optional[int] = None,
                             config: Optional[str] = None) -> Dict[str, Any]:
        """
        Process the 'create' command inputs and prepare data for the pipeline.
        
        Args:
            images: Directory containing images or a list of image paths
            output: Output directory for the generated video
            description: Text description of the demo content
            title: Title of the demo (optional)
            duration: Target duration in seconds (optional)
            config: Path to a custom configuration file (optional)
            
        Returns:
            A dictionary containing all processed inputs ready for the pipeline
            
        Raises:
            ValueError: If any input is invalid
        """
        pass
    
    @abstractmethod
    def process_list_command(self) -> List[Dict[str, Any]]:
        """
        Process the 'list' command and retrieve all available demos.
        
        Returns:
            A list of dictionaries containing information about each demo
        """
        pass
    
    @abstractmethod
    def process_info_command(self, demo_id: str) -> Dict[str, Any]:
        """
        Process the 'info' command and retrieve information about a specific demo.
        
        Args:
            demo_id: The ID of the demo to get information about
            
        Returns:
            A dictionary containing detailed information about the demo
            
        Raises:
            ValueError: If the demo ID is invalid
        """
        pass
    
    @abstractmethod
    def get_help(self, command: Optional[str] = None) -> str:
        """
        Get help information for the CLI.
        
        Args:
            command: The specific command to get help for (optional)
            
        Returns:
            A string containing help information
        """
        pass
