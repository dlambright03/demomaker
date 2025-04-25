"""
Implementation of the Storage Manager Module.

This module manages file-based storage of all inputs, intermediate
assets, and outputs for the DemoMaker application.
"""

import json
import logging
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Union

from src.interfaces.storage_manager import (
    AssetNotFoundError,
    AssetTypeError,
    DiskSpaceError,
    InvalidProjectArchiveError,
    ProjectNotFoundError,
    StorageAccessError,
    StorageError,
    StorageManagerInterface,
)

# Configure logging
logger = logging.getLogger(__name__)


class FileStorageManager(StorageManagerInterface):
    """Implementation of the Storage Manager Module using file-based storage."""

    # Asset type constants
    ASSET_TYPE_IMAGES = "images"
    ASSET_TYPE_SCRIPT = "script"
    ASSET_TYPE_NARRATION = "narration"
    ASSET_TYPE_VIDEO = "video"
    ASSET_TYPE_METADATA = "metadata"

    VALID_ASSET_TYPES = [
        ASSET_TYPE_IMAGES,
        ASSET_TYPE_SCRIPT,
        ASSET_TYPE_NARRATION,
        ASSET_TYPE_VIDEO,
        ASSET_TYPE_METADATA,
    ]

    def __init__(self, base_storage_path: Optional[Path] = None):
        """
        Initialize the FileStorageManager.

        Args:
            base_storage_path: Base path for storage (optional)
        """
        # Set default base storage path if not provided
        if base_storage_path is None:
            base_storage_path = Path(os.path.expanduser("~/.demomaker/storage"))

        self.base_storage_path = base_storage_path

        # Create base storage directory if it doesn't exist
        try:
            self.base_storage_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Storage initialized at: {self.base_storage_path}")
        except Exception as e:
            logger.error(f"Failed to initialize storage: {str(e)}")
            raise StorageAccessError(f"Failed to initialize storage: {str(e)}") from e

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
        try:
            # Generate a unique project ID based on name and timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Sanitize project name for use in ID
            sanitized_name = "".join(
                c if c.isalnum() else "_" for c in project_name
            ).lower()
            project_id = f"{sanitized_name}_{timestamp}"

            # Create project directory structure
            project_dir = self.base_storage_path / project_id

            # Check if project directory already exists
            if project_dir.exists():
                logger.warning(f"Project directory already exists: {project_dir}")
                # Add a unique suffix to ensure uniqueness
                import uuid

                project_id = f"{project_id}_{str(uuid.uuid4())[:8]}"
                project_dir = self.base_storage_path / project_id

            # Create project directory and subdirectories
            project_dir.mkdir(parents=True, exist_ok=False)

            # Create subdirectories for different asset types
            for asset_type in self.VALID_ASSET_TYPES:
                (project_dir / asset_type).mkdir(exist_ok=True)

            # Create initial metadata
            metadata = {
                "project_id": project_id,
                "project_name": project_name,
                "created_at": datetime.now().isoformat(),
                "status": "initialized",
            }

            # Store metadata
            metadata_file = project_dir / self.ASSET_TYPE_METADATA / "project.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Project initialized: {project_id}")

            return project_id

        except Exception as e:
            logger.error(f"Failed to initialize project: {str(e)}")
            raise StorageError(f"Failed to initialize project: {str(e)}") from e

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
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Get images directory
            images_dir = project_dir / self.ASSET_TYPE_IMAGES

            # Store each image
            stored_images = []
            for i, image_path in enumerate(images):
                # Create a unique filename for the stored image
                # Preserve the original extension
                original_ext = image_path.suffix
                stored_filename = f"image_{i:03d}{original_ext}"
                stored_path = images_dir / stored_filename

                # Copy the image file
                shutil.copy2(image_path, stored_path)

                # Add to list of stored images
                stored_images.append(stored_path)

            # Update metadata
            self._update_project_metadata(
                project_id,
                {
                    "image_count": len(stored_images),
                    "last_updated": datetime.now().isoformat(),
                },
            )

            logger.info(f"Stored {len(stored_images)} images for project {project_id}")

            return stored_images

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to store images: {str(e)}")
            raise StorageError(f"Failed to store images: {str(e)}") from e

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
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Get script directory
            script_dir = project_dir / self.ASSET_TYPE_SCRIPT

            # Create a timestamped filename for the script
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            script_filename = f"script_{timestamp}.json"
            script_path = script_dir / script_filename

            # Write the script to file
            with open(script_path, "w", encoding="utf-8") as f:
                json.dump(script, f, indent=2)

            # Update metadata
            self._update_project_metadata(
                project_id,
                {
                    "has_script": True,
                    "script_timestamp": timestamp,
                    "last_updated": datetime.now().isoformat(),
                },
            )

            logger.info(f"Stored script for project {project_id}: {script_path}")

            return script_path

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to store script: {str(e)}")
            raise StorageError(f"Failed to store script: {str(e)}") from e

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
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Get narration directory
            narration_dir = project_dir / self.ASSET_TYPE_NARRATION

            # Create a timestamped filename for the narration
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            original_ext = narration_path.suffix
            narration_filename = f"narration_{timestamp}{original_ext}"
            stored_path = narration_dir / narration_filename

            # Copy the narration file
            shutil.copy2(narration_path, stored_path)

            # Update metadata
            self._update_project_metadata(
                project_id,
                {
                    "has_narration": True,
                    "narration_timestamp": timestamp,
                    "last_updated": datetime.now().isoformat(),
                },
            )

            logger.info(f"Stored narration for project {project_id}: {stored_path}")

            return stored_path

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to store narration: {str(e)}")
            raise StorageError(f"Failed to store narration: {str(e)}") from e

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
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Get video directory
            video_dir = project_dir / self.ASSET_TYPE_VIDEO

            # Create a timestamped filename for the video
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            original_ext = video_path.suffix
            video_filename = f"video_{timestamp}{original_ext}"
            stored_path = video_dir / video_filename

            # Copy the video file
            shutil.copy2(video_path, stored_path)

            # Update metadata
            self._update_project_metadata(
                project_id,
                {
                    "has_video": True,
                    "video_timestamp": timestamp,
                    "status": "completed",
                    "last_updated": datetime.now().isoformat(),
                },
            )

            logger.info(f"Stored output video for project {project_id}: {stored_path}")

            return stored_path

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to store output video: {str(e)}")
            raise StorageError(f"Failed to store output video: {str(e)}") from e

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
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Get metadata file
            metadata_file = project_dir / self.ASSET_TYPE_METADATA / "project.json"

            # Check if metadata file exists
            if not metadata_file.exists():
                # Create empty metadata if file doesn't exist
                metadata = {
                    "project_id": project_id,
                    "created_at": datetime.now().isoformat(),
                    "status": "unknown",
                }

                # Save the metadata
                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2)

                return metadata

            # Read metadata from file
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            return metadata

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to get project metadata: {str(e)}")
            raise StorageError(f"Failed to get project metadata: {str(e)}") from e

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all available projects.

        Returns:
            List of dictionaries containing metadata for each project

        Raises:
            StorageError: If listing projects fails
        """
        try:
            projects = []

            # Check if base storage directory exists
            if not self.base_storage_path.exists():
                return projects

            # Get all subdirectories in the base storage directory
            for project_dir in self.base_storage_path.iterdir():
                if project_dir.is_dir():
                    try:
                        # Get project ID from directory name
                        project_id = project_dir.name

                        # Get project metadata
                        metadata = self.get_project_metadata(project_id)

                        # Add to projects list
                        projects.append(metadata)
                    except Exception as e:
                        logger.warning(
                            f"Error reading project {project_dir.name}: {str(e)}"
                        )
                        # Continue with next project
                        continue

            return projects

        except Exception as e:
            logger.error(f"Failed to list projects: {str(e)}")
            raise StorageError(f"Failed to list projects: {str(e)}") from e

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
        """
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            assets = []

            # If asset type is specified, validate it
            if asset_type is not None and asset_type not in self.VALID_ASSET_TYPES:
                raise AssetTypeError(f"Invalid asset type: {asset_type}")

            # Get asset directories to process
            if asset_type is None:
                # Get all asset types
                asset_dirs = [project_dir / t for t in self.VALID_ASSET_TYPES]
            else:
                # Get specific asset type
                asset_dirs = [project_dir / asset_type]

            # Collect assets from each directory
            for asset_dir in asset_dirs:
                if asset_dir.exists() and asset_dir.is_dir():
                    for asset_path in asset_dir.iterdir():
                        if asset_path.is_file():
                            assets.append(asset_path)

            return assets

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except AssetTypeError:
            # Re-raise asset type error
            raise
        except Exception as e:
            logger.error(f"Failed to get project assets: {str(e)}")
            raise StorageError(f"Failed to get project assets: {str(e)}") from e

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
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Delete the project directory and all its contents
            shutil.rmtree(project_dir)

            logger.info(f"Deleted project: {project_id}")

            return True

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to delete project: {str(e)}")
            raise StorageError(f"Failed to delete project: {str(e)}") from e

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
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Create export directory if it doesn't exist
            export_path.parent.mkdir(parents=True, exist_ok=True)

            # If export_path is a directory, create a zip file in it
            if export_path.is_dir():
                export_file = export_path / f"{project_id}.zip"
            else:
                export_file = export_path

            # Create zip archive
            with zipfile.ZipFile(export_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add all files from the project directory to the zip
                for root, _, files in os.walk(project_dir):
                    for file in files:
                        file_path = Path(root) / file
                        # Get relative path from project directory
                        rel_path = file_path.relative_to(project_dir)
                        # Add file to zip
                        zipf.write(file_path, rel_path)

            logger.info(f"Exported project {project_id} to {export_file}")

            return export_file

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to export project: {str(e)}")
            raise StorageError(f"Failed to export project: {str(e)}") from e

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
        try:
            # Validate import path
            if not import_path.exists() or not import_path.is_file():
                raise InvalidProjectArchiveError(
                    f"Import path does not exist or is not a file: {import_path}"
                )

            # Check if the file is a valid zip
            if not zipfile.is_zipfile(import_path):
                raise InvalidProjectArchiveError(f"Not a valid zip file: {import_path}")

            # Create a temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)

                # Extract the zip archive
                with zipfile.ZipFile(import_path, "r") as zipf:
                    zipf.extractall(temp_dir_path)

                # Look for metadata to get project ID
                metadata_files = list(temp_dir_path.glob("**/project.json"))

                if not metadata_files:
                    raise InvalidProjectArchiveError(
                        "Archive does not contain project metadata"
                    )

                # Read the first metadata file found
                with open(metadata_files[0], "r", encoding="utf-8") as f:
                    metadata = json.load(f)

                # Get project ID from metadata
                project_id = metadata.get("project_id")

                if not project_id:
                    raise InvalidProjectArchiveError(
                        "Invalid project metadata: missing project ID"
                    )

                # Check if project already exists
                project_dir = self.base_storage_path / project_id

                if project_dir.exists():
                    # Generate a new project ID with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    project_id = f"{project_id}_{timestamp}"
                    project_dir = self.base_storage_path / project_id

                # Create project directory
                project_dir.mkdir(parents=True)

                # Copy extracted files to project directory
                for item in temp_dir_path.iterdir():
                    if item.is_dir():
                        # Copy directory contents
                        shutil.copytree(item, project_dir, dirs_exist_ok=True)
                    else:
                        # Copy file
                        shutil.copy2(item, project_dir)

                # Update metadata to reflect import
                self._update_project_metadata(
                    project_id,
                    {
                        "imported_at": datetime.now().isoformat(),
                        "original_import_file": str(import_path),
                        "last_updated": datetime.now().isoformat(),
                    },
                )

                logger.info(f"Imported project {project_id} from {import_path}")

                return project_id

        except Exception as e:
            logger.error(f"Failed to import project: {str(e)}")
            if isinstance(e, (InvalidProjectArchiveError, ProjectNotFoundError)):
                # Re-raise specific errors
                raise
            else:
                # Wrap other exceptions
                raise StorageError(f"Failed to import project: {str(e)}") from e

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
            AssetNotFoundError: If the asset does not exist
        """
        try:
            # Get project directory
            project_dir = self.base_storage_path / project_id

            # Validate project exists
            if not project_dir.exists():
                raise ProjectNotFoundError(f"Project not found: {project_id}")

            # Parse asset ID to determine asset type and filename
            parts = asset_id.split("/")

            if len(parts) < 2:
                raise AssetNotFoundError(f"Invalid asset ID format: {asset_id}")

            asset_type = parts[0]
            asset_filename = "/".join(parts[1:])

            # Validate asset type
            if asset_type not in self.VALID_ASSET_TYPES:
                raise AssetTypeError(f"Invalid asset type: {asset_type}")

            # Construct asset path
            asset_path = project_dir / asset_type / asset_filename

            # Check if asset exists
            if not asset_path.exists():
                raise AssetNotFoundError(f"Asset not found: {asset_id}")

            return asset_path

        except (ProjectNotFoundError, AssetNotFoundError, AssetTypeError):
            # Re-raise specific errors
            raise
        except Exception as e:
            logger.error(f"Failed to get asset path: {str(e)}")
            raise StorageError(f"Failed to get asset path: {str(e)}") from e

    def _update_project_metadata(
        self, project_id: str, updates: Dict[str, Any]
    ) -> None:
        """
        Update project metadata with the provided updates.

        Args:
            project_id: Unique project ID
            updates: Dictionary of metadata updates

        Raises:
            ProjectNotFoundError: If the project does not exist
            StorageError: If updating metadata fails
        """
        try:
            # Get current metadata
            metadata = self.get_project_metadata(project_id)

            # Update metadata with new values
            metadata.update(updates)

            # Save updated metadata
            metadata_file = (
                self.base_storage_path
                / project_id
                / self.ASSET_TYPE_METADATA
                / "project.json"
            )

            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

        except ProjectNotFoundError:
            # Re-raise project not found error
            raise
        except Exception as e:
            logger.error(f"Failed to update project metadata: {str(e)}")
            raise StorageError(f"Failed to update project metadata: {str(e)}") from e
