"""
Unit tests for the CommandLineProcessor class.
"""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.modules.input_processor import CommandLineProcessor


class TestCommandLineProcessor:
    """Tests for the CommandLineProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CommandLineProcessor()

    def test_get_help(self):
        """Test the get_help method."""
        help_text = self.cli.get_help()
        assert "DemoMaker - Create professional demo videos" in help_text
        assert "commands:" in help_text
        assert "create" in help_text
        assert "list" in help_text
        assert "info" in help_text

    def test_parse_args_create_command(self):
        """Test parsing arguments for the create command."""
        args = self.cli.parse_args(
            [
                "create",
                "--images",
                "test_images/",
                "--output",
                "test_output/",
                "--description",
                "Test demo",
                "--title",
                "Test Title",
            ]
        )

        assert args.command == "create"
        assert args.images == "test_images/"
        assert args.output == "test_output/"
        assert args.description == "Test demo"
        assert args.title == "Test Title"
        assert args.duration is None
        assert args.config is None

    def test_parse_args_list_command(self):
        """Test parsing arguments for the list command."""
        args = self.cli.parse_args(["list"])

        assert args.command == "list"

    def test_parse_args_info_command(self):
        """Test parsing arguments for the info command."""
        args = self.cli.parse_args(["info", "demo_12345"])

        assert args.command == "info"
        assert args.demo_id == "demo_12345"

    @patch("os.access")
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.is_file")
    @patch("pathlib.Path.glob")
    def test_validate_images_directory(
        self, mock_glob, mock_is_file, mock_is_dir, mock_mkdir, mock_access
    ):
        """Test validating images from a directory."""
        # Set up mocks
        mock_is_dir.return_value = True
        mock_is_file.return_value = False

        # Create mock image files
        test_dir = Path("/test_images")
        image_files = [
            test_dir / "image1.jpg",
            test_dir / "image2.png",
            test_dir / "image3.gif",
        ]

        # Configure glob to return our mock image files
        def glob_side_effect(pattern):
            ext = pattern[1:]  # Remove the * from the pattern
            return [f for f in image_files if f.suffix == ext]

        mock_glob.side_effect = glob_side_effect

        # Call the method
        result = self.cli.validate_images("/test_images")

        # Verify results
        assert len(result) == 3
        assert all(isinstance(path, Path) for path in result)
        mock_is_dir.assert_called_once_with()

    @patch("pathlib.Path.is_file")
    def test_validate_images_list(self, mock_is_file):
        """Test validating a list of image paths."""
        # Set up mocks
        mock_is_file.return_value = True

        # Call the method
        result = self.cli.validate_images(
            [
                "/test_images/image1.jpg",
                "/test_images/image2.png",
                "/test_images/image3.gif",
            ]
        )

        # Verify results
        assert len(result) == 3
        assert all(isinstance(path, Path) for path in result)
        assert mock_is_file.call_count == 3

    @patch("pathlib.Path.is_file")
    def test_validate_images_unsupported_format(self, mock_is_file):
        """Test validating an image with an unsupported format."""
        # Set up mocks
        mock_is_file.return_value = True

        # Call the method and check exception
        with pytest.raises(ValueError, match="Unsupported image format"):
            self.cli.validate_images(["/test_images/image.txt"])

    @patch("os.access")
    @patch("pathlib.Path.mkdir")
    def test_validate_output_directory(self, mock_mkdir, mock_access):
        """Test validating an output directory."""
        # Set up mocks
        mock_access.return_value = True

        # Call the method
        result = self.cli.validate_output_directory("/test_output")

        # Verify results
        assert isinstance(result, Path)
        assert str(result) == "/test_output"
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_access.assert_called_once()

    @patch("os.access")
    @patch("pathlib.Path.mkdir")
    def test_validate_output_directory_not_writable(self, mock_mkdir, mock_access):
        """Test validating an output directory that is not writable."""
        # Set up mocks
        mock_access.return_value = False

        # Call the method and check exception
        with pytest.raises(ValueError, match="Output directory is not writable"):
            self.cli.validate_output_directory("/test_output")

    @patch("builtins.open")
    @patch("json.load")
    @patch("pathlib.Path.is_file")
    def test_load_config(self, mock_is_file, mock_json_load, mock_open):
        """Test loading a configuration file."""
        # Set up mocks
        mock_is_file.return_value = True
        mock_json_load.return_value = {"key": "value"}

        # Call the method
        result = self.cli.load_config("/test_config.json")

        # Verify results
        assert result == {"key": "value"}
        mock_is_file.assert_called_once_with()
        mock_open.assert_called_once()
        mock_json_load.assert_called_once()

    @patch("pathlib.Path.is_file")
    def test_load_config_file_not_found(self, mock_is_file):
        """Test loading a configuration file that doesn't exist."""
        # Set up mocks
        mock_is_file.return_value = False

        # Call the method and check exception
        with pytest.raises(ValueError, match="Configuration file not found"):
            self.cli.load_config("/test_config.json")

    def test_process_create_command(self):
        """Test processing the create command."""
        # Create a mock for validate_images, validate_output_directory, and _extract_image_metadata
        with (
            patch.object(self.cli, "validate_images") as mock_validate_images,
            patch.object(self.cli, "validate_output_directory") as mock_validate_output,
            patch.object(self.cli, "_extract_image_metadata") as mock_extract_metadata,
            patch.object(self.cli, "_save_demo_project") as mock_save_project,
        ):

            # Set up mocks
            image_paths = [
                Path("/test_images/image1.jpg"),
                Path("/test_images/image2.png"),
            ]
            mock_validate_images.return_value = image_paths
            mock_validate_output.return_value = Path("/test_output")
            mock_extract_metadata.return_value = [
                {
                    "path": str(p),
                    "filename": p.name,
                    "size_bytes": 1000,
                    "format": p.suffix.lower().lstrip("."),
                    "width": 1920,
                    "height": 1080,
                    "aspect_ratio": "16:9",
                    "color_mode": "RGB",
                }
                for p in image_paths
            ]

            # Call the method
            result = self.cli.process_create_command(
                images="/test_images",
                output="/test_output",
                description="Test demo description",
                title="Test Title",
            )

            # Verify results
            assert "id" in result
            assert result["title"] == "Test Title"
            assert result["description"] == "Test demo description"
            assert result["images"] == [str(p) for p in image_paths]
            assert result["output_directory"] == "/test_output"
            assert "timestamp" in result

            # Verify mocks
            mock_validate_images.assert_called_once_with("/test_images")
            mock_validate_output.assert_called_once_with("/test_output")
            mock_extract_metadata.assert_called_once_with(image_paths)
            mock_save_project.assert_called_once()

    def test_process_list_command(self):
        """Test processing the list command."""
        result = self.cli.process_list_command()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all("id" in demo and "title" in demo for demo in result)

    def test_process_info_command(self):
        """Test processing the info command."""
        result = self.cli.process_info_command("demo_12345")

        assert result["id"] == "demo_12345"
        assert "title" in result
        assert "description" in result
        assert "images" in result
        assert "output_directory" in result
        assert "timestamp" in result

    def test_process_info_command_not_found(self):
        """Test processing the info command for a demo that doesn't exist."""
        with pytest.raises(ValueError, match="Demo with ID .* not found"):
            self.cli.process_info_command("non_existent_demo")
