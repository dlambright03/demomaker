"""
Unit tests for the Script Generator Interface.

This module contains tests that verify the ScriptGeneratorInterface design,
including method signatures and exception classes.
"""

from abc import ABC
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.interfaces.script_generator import (
    AIModelError,
    ImageAnalysisError,
    InvalidInputError,
    ModelNotAvailableError,
    ScriptGenerationError,
    ScriptGenerationTimeoutError,
    ScriptGeneratorInterface,
)


class TestScriptGeneratorInterface:
    """Tests for the ScriptGeneratorInterface class."""

    def test_is_abstract_base_class(self):
        """Test that ScriptGeneratorInterface is an abstract base class."""
        assert issubclass(ScriptGeneratorInterface, ABC)

        # Verify we can't instantiate it directly
        with pytest.raises(TypeError):
            ScriptGeneratorInterface()

    def test_required_methods(self):
        """Test that ScriptGeneratorInterface has all required abstract methods."""
        required_methods = [
            "generate_script",
            "set_ai_model",
            "get_available_models",
            "estimate_generation_time",
            "cancel_generation",
            "analyze_images",
        ]

        for method in required_methods:
            assert hasattr(ScriptGeneratorInterface, method)
            assert getattr(ScriptGeneratorInterface, method).__isabstractmethod__

    def test_method_signatures(self):
        """Test method signatures have the correct parameters and return types."""
        # Sample method signature tests
        generate_script = ScriptGeneratorInterface.generate_script
        assert "images" in generate_script.__annotations__
        assert "description" in generate_script.__annotations__
        assert "title" in generate_script.__annotations__
        assert "target_duration" in generate_script.__annotations__
        assert generate_script.__annotations__["return"] == Dict[str, Any]

        set_ai_model = ScriptGeneratorInterface.set_ai_model
        assert "model_name" in set_ai_model.__annotations__
        assert set_ai_model.__annotations__["return"] is None

        # Add more signature tests as needed

    def test_exception_hierarchy(self):
        """Test that the exception hierarchy is properly structured."""
        # ScriptGenerationError is the base exception
        assert issubclass(ScriptGenerationError, Exception)

        # Other exceptions inherit from ScriptGenerationError
        assert issubclass(AIModelError, ScriptGenerationError)
        assert issubclass(InvalidInputError, ScriptGenerationError)
        assert issubclass(ModelNotAvailableError, ScriptGenerationError)
        assert issubclass(ImageAnalysisError, ScriptGenerationError)
        assert issubclass(ScriptGenerationTimeoutError, ScriptGenerationError)


# Mock implementation for testing inheritance
class MockScriptGenerator(ScriptGeneratorInterface):
    """Mock implementation of ScriptGeneratorInterface for testing."""

    def generate_script(
        self, images: List[Path], description: str, title=None, target_duration=None
    ) -> Dict[str, Any]:
        return {"segments": [], "duration": 60}

    def set_ai_model(self, model_name: str) -> None:
        pass

    def get_available_models(self) -> List[str]:
        return ["gpt-3.5", "gpt-4"]

    def estimate_generation_time(self, num_images: int, description_length: int) -> int:
        return 30

    def cancel_generation(self) -> bool:
        return True

    def analyze_images(self, images: List[Path]) -> List[Dict[str, Any]]:
        return [{"content": "sample image content"} for _ in images]
