"""
Unit tests for the File Storage Manager implementation.

This module contains tests that verify the FileStorageManager implementation,
including all CRUD operations, thread safety, and error handling.
"""

import json
import os
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from src.interfaces.storage_manager import (
    AssetNotFoundError,
    AssetTypeError,
    InvalidProjectArchiveError,
    ProjectNotFoundError,
    StorageError,
)
from src.modules.storage_manager.file_storage_manager import FileStorageManager


@pytest.fixture
def temp_storage_path():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def storage_manager(temp_storage_path):
    """Create a FileStorageManager with a temporary storage path."""
    return FileStorageManager(base_storage_path=temp_storage_path)


@pytest.fixture
def test_project(storage_manager):
    """Create a test project for testing."""
    project_id = storage_manager.initialize_project("Test Project")
    yield project_id
    try:
        # Clean up after test
        storage_manager.delete_project(project_id)
    except Exception:
        pass


@pytest.fixture
def test_image():
    """Create a temporary image file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        # Write some dummy image data
        f.write(b"PNG\r\n\x1a\n" + b"\x00" * 100)
        f.flush()
        path = Path(f.name)
    yield path
    # Clean up
    if path.exists():
        os.unlink(path)


class TestFileStorageManager:
    """Tests for the FileStorageManager class."""

    def test_initialize_project(self, storage_manager):
        """Test initializing a new project."""
        project_id = storage_manager.initialize_project("Test Project")
        assert project_id is not None
        assert "test_project_" in project_id.lower()

        # Verify directory structure
        project_dir = storage_manager.base_storage_path / project_id
        assert project_dir.exists()

        # Check for all required subdirectories
        for asset_type in storage_manager.VALID_ASSET_TYPES + ["temp"]:
            assert (project_dir / asset_type).exists()
            assert (project_dir / asset_type).is_dir()

        # Check for metadata file
        metadata_file = project_dir / "metadata" / "project.json"
        assert metadata_file.exists()

        # Verify metadata content
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        assert metadata["project_name"] == "Test Project"
        assert metadata["project_id"] == project_id
        assert "created_at" in metadata
        assert metadata["status"] == "initialized"

    def test_store_and_retrieve_images(self, storage_manager, test_project, test_image):
        """Test storing and retrieving images."""
        # Store image
        stored_images = storage_manager.store_input_images(test_project, [test_image])
        assert len(stored_images) == 1
        assert stored_images[0].exists()

        # Get project assets
        assets = storage_manager.get_project_assets(test_project, "images")
        assert len(assets) == 1
        assert assets[0].exists()
        assert assets[0].name.startswith("image_")

        # Check for metadata file
        metadata_file = assets[0].with_name(assets[0].name + ".meta.json")
        assert metadata_file.exists()

        # Verify metadata content
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        assert metadata["original_filename"] == test_image.name
        assert "hash" in metadata
        assert "size_bytes" in metadata

        # Check that project metadata was updated
        project_metadata = storage_manager.get_project_metadata(test_project)
        assert project_metadata["image_count"] == 1

    def test_store_and_retrieve_script(self, storage_manager, test_project):
        """Test storing and retrieving a script."""
        # Create a test script
        script = {
            "title": "Test Script",
            "slides": [
                {"title": "Slide 1", "content": "Content 1"},
                {"title": "Slide 2", "content": "Content 2"},
            ],
        }

        # Store script
        script_path = storage_manager.store_script(test_project, script)
        assert script_path.exists()
        assert script_path.name.startswith("script_")

        # Check for metadata file
        metadata_file = script_path.with_name(script_path.name + ".meta.json")
        assert metadata_file.exists()

        # Get project assets
        assets = storage_manager.get_project_assets(test_project, "script")
        assert len(assets) == 1
        assert assets[0].exists()
        assert assets[0].name.startswith("script_")

        # Verify script content
        with open(assets[0], "r") as f:
            stored_script = json.load(f)

        assert stored_script["title"] == "Test Script"
        assert len(stored_script["slides"]) == 2

        # Check that project metadata was updated
        project_metadata = storage_manager.get_project_metadata(test_project)
        assert project_metadata["has_script"] == True

    def test_list_projects(self, storage_manager):
        """Test listing projects."""
        # Create multiple projects
        project_ids = []
        for i in range(3):
            project_id = storage_manager.initialize_project(f"Test Project {i}")
            project_ids.append(project_id)

        # List projects
        projects = storage_manager.list_projects()
        assert len(projects) >= 3

        # Verify each project in the list
        for project_id in project_ids:
            project = next((p for p in projects if p["project_id"] == project_id), None)
            assert project is not None
            assert project["project_name"].startswith("Test Project")

        # Clean up
        for project_id in project_ids:
            storage_manager.delete_project(project_id)

    def test_delete_project(self, storage_manager):
        """Test deleting a project."""
        # Create a project
        project_id = storage_manager.initialize_project("Project to Delete")

        # Store some data
        script = {"title": "Test Script"}
        storage_manager.store_script(project_id, script)

        # Verify project exists
        project_dir = storage_manager.base_storage_path / project_id
        assert project_dir.exists()

        # Delete project
        result = storage_manager.delete_project(project_id)
        assert result == True

        # Verify project no longer exists
        assert not project_dir.exists()

        # Verify project is not in list
        projects = storage_manager.list_projects()
        assert not any(p["project_id"] == project_id for p in projects)

    def test_get_project_metadata(self, storage_manager, test_project):
        """Test getting project metadata."""
        # Get initial metadata
        metadata = storage_manager.get_project_metadata(test_project)
        assert metadata["project_id"] == test_project
        assert metadata["status"] == "initialized"

        # Store something to update metadata
        script = {"title": "Test Script"}
        storage_manager.store_script(test_project, script)

        # Get updated metadata
        updated_metadata = storage_manager.get_project_metadata(test_project)
        assert updated_metadata["has_script"] == True
        assert "script_timestamp" in updated_metadata
        assert "asset_counts" in updated_metadata
        assert updated_metadata["asset_counts"]["scripts"] == 1

    def test_export_and_import_project(self, storage_manager, test_project, test_image):
        """Test exporting and importing a project."""
        # Store some data
        storage_manager.store_input_images(test_project, [test_image])
        script = {"title": "Test Script"}
        storage_manager.store_script(test_project, script)

        # Export project
        with tempfile.TemporaryDirectory() as temp_dir:
            export_path = Path(temp_dir) / "exported_project.zip"
            exported_file = storage_manager.export_project(test_project, export_path)
            assert exported_file.exists()
            assert exported_file.suffix == ".zip"

            # Import project
            imported_project_id = storage_manager.import_project(exported_file)
            assert imported_project_id is not None
            assert imported_project_id != test_project  # Should have a different ID

            # Verify imported project
            imported_dir = storage_manager.base_storage_path / imported_project_id
            assert imported_dir.exists()

            # Check imported metadata
            metadata = storage_manager.get_project_metadata(imported_project_id)
            assert "imported_at" in metadata
            assert metadata["has_script"] == True

            # Check imported assets
            assets = storage_manager.get_project_assets(imported_project_id)
            assert len(assets) >= 2  # At least script and image

            # Clean up
            storage_manager.delete_project(imported_project_id)

    def test_thread_safety(self, storage_manager, test_project):
        """Test thread safety by accessing the same project concurrently."""
        # Number of concurrent operations
        n_operations = 10

        # Function to update project metadata
        def update_metadata(index):
            try:
                storage_manager._update_project_metadata(
                    test_project, {f"test_key_{index}": f"test_value_{index}"}
                )
            except Exception as e:
                return str(e)
            return None

        # Create and start threads
        threads = []
        results = [None] * n_operations

        for i in range(n_operations):
            t = threading.Thread(
                target=lambda idx=i: results.__setitem__(idx, update_metadata(idx))
            )
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Check that all operations succeeded
        assert all(result is None for result in results)

        # Verify that all updates were applied
        metadata = storage_manager.get_project_metadata(test_project)

        for i in range(n_operations):
            assert metadata[f"test_key_{i}"] == f"test_value_{i}"

    def test_search_projects(self, storage_manager):
        """Test searching for projects."""
        # Create projects with specific names
        project_ids = []
        project_ids.append(storage_manager.initialize_project("Alpha Project"))
        project_ids.append(storage_manager.initialize_project("Beta Project"))
        project_ids.append(storage_manager.initialize_project("Alpha Beta Project"))

        # Search for Alpha projects
        alpha_projects = storage_manager.search_projects("Alpha")
        assert len(alpha_projects) == 2
        assert all("alpha" in p["project_name"].lower() for p in alpha_projects)

        # Search for Beta projects
        beta_projects = storage_manager.search_projects("Beta")
        assert len(beta_projects) == 2
        assert all("beta" in p["project_name"].lower() for p in beta_projects)

        # Search for a non-existent project
        empty_results = storage_manager.search_projects("NonExistent")
        assert len(empty_results) == 0

        # Clean up
        for project_id in project_ids:
            storage_manager.delete_project(project_id)

    def test_find_asset_by_name(self, storage_manager, test_project):
        """Test finding assets by name pattern."""
        # Create multiple script files
        scripts = [
            {"title": "Alpha Script"},
            {"title": "Beta Script"},
            {"title": "Gamma Script"},
        ]

        # Store each script with a small delay to ensure unique timestamps
        for script in scripts:
            time.sleep(0.1)  # Ensure unique timestamps for each script
            storage_manager.store_script(test_project, script)

        # Find all scripts
        all_scripts = storage_manager.find_asset_by_name(test_project, "script_*.json")
        assert len(all_scripts) == 3

        # Find scripts with specific pattern
        # Sleep to ensure timestamp differentiates files
        time.sleep(0.1)
        delta_script = {"title": "Delta Script"}
        storage_manager.store_script(test_project, delta_script)

        # This should find the newest script first
        newest_script = storage_manager.find_asset_by_name(
            test_project, "script_*.json"
        )
        assert len(newest_script) == 4

        # Verify by checking the content, newest should be first
        with open(newest_script[0], "r") as f:
            content = json.load(f)
            assert content["title"] == "Delta Script"

    def test_error_handling(self, storage_manager):
        """Test error handling for various operations."""
        # Test non-existent project
        with pytest.raises(ProjectNotFoundError):
            storage_manager.get_project_metadata("non_existent_project")

        # Test invalid asset type
        project_id = storage_manager.initialize_project("Error Test Project")
        with pytest.raises(AssetTypeError):
            storage_manager.get_project_assets(project_id, "invalid_asset_type")

        # Test non-existent asset
        with pytest.raises(AssetNotFoundError):
            storage_manager.get_asset_path(project_id, "images/non_existent.png")

        # Test invalid project archive
        with tempfile.NamedTemporaryFile(suffix=".zip") as f:
            f.write(b"not a valid zip file")
            f.flush()
            with pytest.raises(InvalidProjectArchiveError):
                storage_manager.import_project(Path(f.name))

        # Clean up
        storage_manager.delete_project(project_id)

    def test_cleanup_temporary_files(self, storage_manager, test_project):
        """Test cleaning up temporary files."""
        # Create temporary files in the project
        temp_dir = storage_manager.base_storage_path / test_project / "temp"
        temp_files = []

        for i in range(5):
            temp_file = temp_dir / f"test_temp_{i}.txt"
            with open(temp_file, "w") as f:
                f.write(f"Temporary file {i}")
            temp_files.append(temp_file)

        # Verify files exist
        for temp_file in temp_files:
            assert temp_file.exists()

        # Clean up temporary files
        count = storage_manager.cleanup_temporary_files(test_project)
        assert count == 5

        # Verify files were deleted
        for temp_file in temp_files:
            assert not temp_file.exists()

    def test_verify_project_integrity(self, storage_manager, test_project, test_image):
        """Test verifying project integrity."""
        # Store some data
        storage_manager.store_input_images(test_project, [test_image])
        script = {"title": "Test Script"}
        script_path = storage_manager.store_script(test_project, script)

        # Verify project integrity
        results = storage_manager.verify_project_integrity(test_project)
        assert results["project_id"] == test_project
        assert results["structure_valid"] == True
        assert results["metadata_valid"] == True
        assert results["assets_verified"] >= 2  # At least script and image
        assert results["assets_corrupted"] == 0
        assert len(results["issues"]) == 0

        # Corrupt a file to test detection
        # We'll write directly to the file to bypass the storage manager
        with open(script_path, "w") as f:
            f.write("corrupted data")

        # Verify integrity again
        results = storage_manager.verify_project_integrity(test_project)
        assert results["assets_corrupted"] >= 1
        assert len(results["issues"]) >= 1
