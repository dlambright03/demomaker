"""
Interface for the Storage Manager Module.

This module is responsible for managing file-based storage of all inputs,
intermediate assets, and outputs for the DemoMaker application.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, BinaryIO, Union


class StorageManagerInterface(ABC):
    """Interface for the Storage Manager Module."""
    
    @abstractmethod
    def initialize_project(self, project_name: str) -> str:
        """
        Initialize a new project with the given name.
        
        Args:
            project_name: Name of the project
            
        Returns:
            A unique project ID
            
        Raises:
            StorageError: If project initialization fails
        """
        pass
    
    @abstractmethod
    def store_input_images(self, project_id: str, images: List[Path]) -> List[Path]:
        """
        Store input images for a project.
        
        Args:
            project_id: Unique project ID
            images: List of image Path objects
            
        Returns:
            List of paths to the stored images
            
        Raises:
            StorageError: If storing images fails
        """
        pass
    
    @abstractmethod
    def store_script(self, project_id: str, script: Dict[str, Any]) -> Path:
        """
        Store a generated script for a project.
        
        Args:
            project_id: Unique project ID
            script: Dictionary containing the structured script
            
        Returns:
            Path to the stored script file
            
        Raises:
            StorageError: If storing the script fails
        """
        pass
    
    @abstractmethod
    def store_narration(self, project_id: str, narration_path: Path) -> Path:
        """
        Store a generated narration audio file for a project.
        
        Args:
            project_id: Unique project ID
            narration_path: Path to the narration audio file
            
        Returns:
            Path to the stored narration file
            
        Raises:
            StorageError: If storing the narration fails
        """
        pass
    
    @abstractmethod
    def store_output_video(self, project_id: str, video_path: Path) -> Path:
        """
        Store an output video file for a project.
        
        Args:
            project_id: Unique project ID
            video_path: Path to the output video file
            
        Returns:
            Path to the stored video file
            
        Raises:
            StorageError: If storing the video fails
        """
        pass
    
    @abstractmethod
    def get_project_metadata(self, project_id: str) -> Dict[str, Any]:
        """
        Get metadata for a project.
        
        Args:
            project_id: Unique project ID
            
        Returns:
            Dictionary containing project metadata
            
        Raises:
            StorageError: If retrieving the metadata fails
            ValueError: If the project ID is invalid
        """
        pass
    
    @abstractmethod
    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all available projects.
        
        Returns:
            List of dictionaries containing project metadata
        """
        pass
    
    @abstractmethod
    def get_input_images(self, project_id: str) -> List[Path]:
        """
        Get input images for a project.
        
        Args:
            project_id: Unique project ID
            
        Returns:
            List of paths to the project's input images
            
        Raises:
            StorageError: If retrieving the images fails
            ValueError: If the project ID is invalid
        """
        pass
    
    @abstractmethod
    def get_script(self, project_id: str) -> Dict[str, Any]:
        """
        Get the generated script for a project.
        
        Args:
            project_id: Unique project ID
            
        Returns:
            Dictionary containing the structured script
            
        Raises:
            StorageError: If retrieving the script fails
            ValueError: If the project ID is invalid
        """
        pass
    
    @abstractmethod
    def get_narration(self, project_id: str) -> Path:
        """
        Get the generated narration audio file for a project.
        
        Args:
            project_id: Unique project ID
            
        Returns:
            Path to the project's narration audio file
            
        Raises:
            StorageError: If retrieving the narration fails
            ValueError: If the project ID is invalid
        """
        pass
    
    @abstractmethod
    def get_output_video(self, project_id: str) -> Path:
        """
        Get the output video file for a project.
        
        Args:
            project_id: Unique project ID
            
        Returns:
            Path to the project's output video file
            
        Raises:
            StorageError: If retrieving the video fails
            ValueError: If the project ID is invalid
        """
        pass
    
    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project and all its associated assets.
        
        Args:
            project_id: Unique project ID
            
        Returns:
            True if deletion was successful, False otherwise
            
        Raises:
            ValueError: If the project ID is invalid
        """
        pass
    
    @abstractmethod
    def create_temp_directory(self) -> Path:
        """
        Create a temporary directory for processing.
        
        Returns:
            Path to the temporary directory
            
        Raises:
            StorageError: If creating the temporary directory fails
        """
        pass
    
    @abstractmethod
    def cleanup_temp_files(self) -> bool:
        """
        Clean up temporary files created during processing.
        
        Returns:
            True if cleanup was successful, False otherwise
        """
        pass
