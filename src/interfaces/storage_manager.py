"""
Storage Manager Interface for the DemoMaker application.

This module defines the interface for the Storage Manager, which is
responsible for handling file-based storage of all inputs, intermediate
assets, and outputs for the DemoMaker application.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class StorageError(Exception):
    """Base exception for all storage-related errors."""

    pass


class StorageAccessError(StorageError):
    """Exception raised when storage access is denied or fails."""

    pass


class ProjectNotFoundError(StorageError):
    """Exception raised when a project cannot be found."""

    pass


class AssetNotFoundError(StorageError):
    """Exception raised when an asset cannot be found."""

    pass


class AssetTypeError(StorageError):
    """Exception raised when an invalid asset type is specified."""

    pass


class DiskSpaceError(StorageError):
    """Exception raised when there's insufficient disk space."""

    pass


class InvalidProjectArchiveError(StorageError):
    """Exception raised when a project archive is invalid or corrupted."""

    pass


class StorageManagerInterface(ABC):
    """Interface for the Storage Manager module."""

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
            ProjectNotFoundError: If the project does not exist
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
            ProjectNotFoundError: If the project does not exist
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
            ProjectNotFoundError: If the project does not exist
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
            ProjectNotFoundError: If the project does not exist
        """
        pass

    @abstractmethod
    def get_project_metadata(self, project_id: str) -> Dict[str, Any]:
        """
        Get metadata for a specific project.

        Args:
            project_id: Unique project ID

        Returns:
            Dictionary containing project metadata

        Raises:
            StorageError: If retrieving metadata fails
            ProjectNotFoundError: If the project does not exist
        """
        pass

    @abstractmethod
    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all available projects.

        Returns:
            List of dictionaries containing metadata for each project

        Raises:
            StorageError: If listing projects fails
        """
        pass

    @abstractmethod
    def get_project_assets(
        self, project_id: str, asset_type: Optional[str] = None
    ) -> List[Path]:
        """
        Get all assets for a specific project, optionally filtered by type.

        Args:
            project_id: Unique project ID
            asset_type: Optional asset type filter ('images', 'script', 'narration', 'video')

        Returns:
            List of paths to project assets

        Raises:
            StorageError: If retrieving assets fails
            ProjectNotFoundError: If the project does not exist
            AssetTypeError: If an invalid asset type is specified
        """
        pass

    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project and all its assets.

        Args:
            project_id: Unique project ID

        Returns:
            True if deletion was successful, False otherwise

        Raises:
            StorageError: If project deletion fails
            ProjectNotFoundError: If the project does not exist
        """
        pass

    @abstractmethod
    def export_project(self, project_id: str, export_path: Path) -> Path:
        """
        Export a project as a zip archive.

        Args:
            project_id: Unique project ID
            export_path: Path to save the exported project

        Returns:
            Path to the exported project file

        Raises:
            StorageError: If project export fails
            ProjectNotFoundError: If the project does not exist
        """
        pass

    @abstractmethod
    def import_project(self, import_path: Path) -> str:
        """
        Import a project from a zip archive.

        Args:
            import_path: Path to the project archive

        Returns:
            Project ID of the imported project

        Raises:
            StorageError: If project import fails
            InvalidProjectArchiveError: If the archive is not a valid project
        """
        pass

    @abstractmethod
    def get_asset_path(self, project_id: str, asset_id: str) -> Path:
        """
        Get the path to a specific asset.

        Args:
            project_id: Unique project ID
            asset_id: Asset identifier

        Returns:
            Path to the requested asset

        Raises:
            StorageError: If retrieving the asset path fails
            ProjectNotFoundError: If the project does not exist
            AssetNotFoundError: If the asset does not exist
            AssetTypeError: If an invalid asset type is specified
        """
        pass
