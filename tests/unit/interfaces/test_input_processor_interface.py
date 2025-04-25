"""
Unit tests for the Input Processor Interface.

This module contains tests that verify the InputProcessorInterface design,
including method signatures and exception classes.
"""

from abc import ABC
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pytest

from src.interfaces.input_processor import (
    CommandProcessingError,
    ImageValidationError,
    InputProcessorError,
    InputProcessorInterface,
    InvalidArgumentError,
)


class TestInputProcessorInterface:
    """Tests for the InputProcessorInterface class."""

    def test_is_abstract_base_class(self):
        """Test that InputProcessorInterface is an abstract base class."""
        assert issubclass(InputProcessorInterface, ABC)

        # Verify we can't instantiate it directly
        with pytest.raises(TypeError):
            InputProcessorInterface()

    def test_required_methods(self):
        """Test that InputProcessorInterface has all required abstract methods."""
        required_methods = [
            "validate_images",
            "extract_image_metadata",
            "process_create_command",
            "process_list_command",
            "process_info_command",
            "get_help",
            "handle_cli_arguments",
            "normalize_input_paths",
            "generate_project_id",
        ]

        for method in required_methods:
            assert hasattr(InputProcessorInterface, method)
            assert getattr(InputProcessorInterface, method).__isabstractmethod__

    def test_method_signatures(self):
        """Test method signatures have the correct parameters and return types."""
        # Sample method signature tests
        validate_images = InputProcessorInterface.validate_images
        assert "image_paths" in validate_images.__annotations__
        assert validate_images.__annotations__["return"] == List[Path]

        process_create = InputProcessorInterface.process_create_command
        assert "images" in process_create.__annotations__
        assert "output" in process_create.__annotations__
        assert "description" in process_create.__annotations__
        assert process_create.__annotations__["return"] == Dict[str, Any]

        # Add more signature tests as needed

    def test_exception_hierarchy(self):
        """Test that the exception hierarchy is properly structured."""
        # InputProcessorError is the base exception
        assert issubclass(InputProcessorError, Exception)

        # Other exceptions inherit from InputProcessorError
        assert issubclass(ImageValidationError, InputProcessorError)
        assert issubclass(CommandProcessingError, InputProcessorError)
        assert issubclass(InvalidArgumentError, InputProcessorError)


# Mock implementation for testing inheritance
class MockInputProcessor(InputProcessorInterface):
    """Mock implementation of InputProcessorInterface for testing."""

    def validate_images(self, image_paths: Union[str, List[str]]) -> List[Path]:
        return [Path("test.jpg")]

    def extract_image_metadata(self, image_paths: List[Path]) -> List[Dict[str, Any]]:
        return [{"size": "100kb", "dimensions": "800x600"}]

    def process_create_command(
        self,
        images: Union[str, List[str]],
        output: str,
        description: str,
        title: Optional[str] = None,
        duration: Optional[int] = None,
        config: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {"status": "success"}

    def process_list_command(self) -> List[Dict[str, Any]]:
        return [{"id": "demo1"}]

    def process_info_command(self, demo_id: str) -> Dict[str, Any]:
        return {"id": demo_id, "status": "completed"}

    def get_help(self, command: Optional[str] = None) -> str:
        return "Help text"

    def handle_cli_arguments(self, args: Optional[List[str]] = None) -> Dict[str, Any]:
        return {"command": "create"}

    def normalize_input_paths(self, paths: Union[str, List[str]]) -> List[Path]:
        return [Path("normalized/path")]

    def generate_project_id(self, title: str) -> str:
        return "project-123"


class TestMockInputProcessor:
    """Tests for a concrete implementation of InputProcessorInterface."""

    def test_can_instantiate_concrete_implementation(self):
        """Test that a concrete implementation can be instantiated."""
        mock = MockInputProcessor()
        assert isinstance(mock, InputProcessorInterface)

    def test_concrete_implementation_methods(self):
        """Test that concrete implementation methods work as expected."""
        mock = MockInputProcessor()
        assert len(mock.validate_images("test.jpg")) == 1
        assert mock.process_info_command("demo1")["id"] == "demo1"
        assert mock.generate_project_id("Test Project") == "project-123"
