"""
Unit tests for the Storage Manager Interface.

This module contains tests that verify the StorageManagerInterface design,
including method signatures and exception classes.
"""

from abc import ABC
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional, Union

import pytest

from src.interfaces.storage_manager import (
    AssetNotFoundError,
    DiskSpaceError,
    InvalidProjectArchiveError,
    ProjectNotFoundError,
    StorageError,
    StorageManagerInterface,
)


class TestStorageManagerInterface:
    """Tests for the StorageManagerInterface class."""

    def test_is_abstract_base_class(self):
        """Test that StorageManagerInterface is an abstract base class."""
        assert issubclass(StorageManagerInterface, ABC)

        # Verify we can't instantiate it directly
        with pytest.raises(TypeError):
            StorageManagerInterface()

    def test_required_methods(self):
        """Test that StorageManagerInterface has all required abstract methods."""
        required_methods = [
            "initialize_project",
            "store_input_images",
            "store_script",
            "store_narration",
            "store_output_video",
            "get_project_metadata",
            "list_projects",
            "get_project_assets",
            "delete_project",
            "export_project",
            "import_project",
            "get_asset_path",
        ]

        for method in required_methods:
            assert hasattr(StorageManagerInterface, method)
            assert getattr(StorageManagerInterface, method).__isabstractmethod__

    def test_method_signatures(self):
        """Test method signatures have the correct parameters and return types."""
        # Sample method signature tests
        initialize_project = StorageManagerInterface.initialize_project
        assert "project_name" in initialize_project.__annotations__
        assert initialize_project.__annotations__["return"] == str

        store_input_images = StorageManagerInterface.store_input_images
        assert "project_id" in store_input_images.__annotations__
        assert "images" in store_input_images.__annotations__
        assert store_input_images.__annotations__["return"] == List[Path]

        # Add more signature tests as needed

    def test_exception_hierarchy(self):
        """Test that the exception hierarchy is properly structured."""
        # StorageError is the base exception
        assert issubclass(StorageError, Exception)

        # Other exceptions inherit from StorageError
        assert issubclass(ProjectNotFoundError, StorageError)
        assert issubclass(AssetNotFoundError, StorageError)
        assert issubclass(InvalidProjectArchiveError, StorageError)
        assert issubclass(DiskSpaceError, StorageError)


# Mock implementation for testing inheritance
class MockStorageManager(StorageManagerInterface):
    """Mock implementation of StorageManagerInterface for testing."""

    def initialize_project(self, project_name: str) -> str:
        return "project-123"

    def store_input_images(self, project_id: str, images: List[Path]) -> List[Path]:
        return [Path(f"projects/{project_id}/images/image1.jpg")]

    def store_script(self, project_id: str, script: Dict[str, Any]) -> Path:
        return Path(f"projects/{project_id}/script.json")

    def store_narration(self, project_id: str, narration_path: Path) -> Path:
        return Path(f"projects/{project_id}/narration.mp3")

    def store_output_video(self, project_id: str, video_path: Path) -> Path:
        return Path(f"projects/{project_id}/output.mp4")

    def get_project_metadata(self, project_id: str) -> Dict[str, Any]:
        return {"id": project_id, "name": "Test Project"}

    def list_projects(self) -> List[Dict[str, Any]]:
        return [{"id": "project-123", "name": "Test Project"}]

    def get_project_assets(
        self, project_id: str, asset_type: Optional[str] = None
    ) -> List[Path]:
        return [Path(f"projects/{project_id}/output.mp4")]

    def delete_project(self, project_id: str) -> bool:
        return True

    def export_project(self, project_id: str, export_path: Path) -> Path:
        return Path(f"{export_path}/project-123.zip")

    def import_project(self, import_path: Path) -> str:
        return "project-123"

    def get_asset_path(self, project_id: str, asset_id: str) -> Path:
        return Path(f"projects/{project_id}/{asset_id}")


class TestMockStorageManager:
    """Tests for a concrete implementation of StorageManagerInterface."""

    def test_can_instantiate_concrete_implementation(self):
        """Test that a concrete implementation can be instantiated."""
        mock = MockStorageManager()
        assert isinstance(mock, StorageManagerInterface)

    def test_concrete_implementation_methods(self):
        """Test that concrete implementation methods work as expected."""
        mock = MockStorageManager()
        assert mock.initialize_project("Test Project") == "project-123"
        assert "project-123" in str(mock.store_script("project-123", {}))
        assert mock.delete_project("project-123") is True
