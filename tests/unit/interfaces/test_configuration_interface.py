"""
Unit tests for the Configuration Interface.

This module contains tests that verify the ConfigurationInterface design,
including method signatures and exception classes.
"""

from abc import ABC
from pathlib import Path
from typing import Any, Dict, Optional

import pytest

from src.interfaces.configuration import (
    ConfigurationError,
    ConfigurationInterface,
    ConfigurationLoadError,
    ConfigurationSaveError,
    ConfigurationValidationError,
)


class TestConfigurationInterface:
    """Tests for the ConfigurationInterface class."""

    def test_is_abstract_base_class(self):
        """Test that ConfigurationInterface is an abstract base class."""
        assert issubclass(ConfigurationInterface, ABC)

        # Verify we can't instantiate it directly
        with pytest.raises(TypeError):
            ConfigurationInterface()

    def test_required_methods(self):
        """Test that ConfigurationInterface has all required abstract methods."""
        required_methods = [
            "load_configuration",
            "get_value",
            "set_value",
            "get_section",
            "save_configuration",
            "get_environment",
            "reset_to_defaults",
            "merge_configuration",
            "validate_configuration",
        ]

        for method in required_methods:
            assert hasattr(ConfigurationInterface, method)
            assert getattr(ConfigurationInterface, method).__isabstractmethod__

    def test_method_signatures(self):
        """Test method signatures have the correct parameters and return types."""
        # Sample method signature tests
        load_config = ConfigurationInterface.load_configuration
        assert "config_path" in load_config.__annotations__
        assert load_config.__annotations__["return"] == bool

        get_value = ConfigurationInterface.get_value
        assert "key" in get_value.__annotations__
        assert "default" in get_value.__annotations__

        # Add more signature tests as needed

    def test_exception_hierarchy(self):
        """Test that the exception hierarchy is properly structured."""
        # ConfigurationError is the base exception
        assert issubclass(ConfigurationError, Exception)

        # Other exceptions inherit from ConfigurationError
        assert issubclass(ConfigurationLoadError, ConfigurationError)
        assert issubclass(ConfigurationSaveError, ConfigurationError)
        assert issubclass(ConfigurationValidationError, ConfigurationError)


# Mock implementation for testing inheritance
class MockConfigManager(ConfigurationInterface):
    """Mock implementation of ConfigurationInterface for testing."""

    def load_configuration(self, config_path: Optional[Path] = None) -> bool:
        return True

    def get_value(self, key: str, default: Any = None) -> Any:
        return default

    def set_value(self, key: str, value: Any) -> bool:
        return True

    def get_section(self, section: str) -> Dict[str, Any]:
        return {}

    def save_configuration(self, config_path: Optional[Path] = None) -> bool:
        return True

    def get_environment(self) -> str:
        return "test"

    def reset_to_defaults(self) -> bool:
        return True

    def merge_configuration(self, config_dict: Dict[str, Any]) -> bool:
        return True

    def validate_configuration(self) -> bool:
        return True


class TestMockConfigManager:
    """Tests for a concrete implementation of ConfigurationInterface."""

    def test_can_instantiate_concrete_implementation(self):
        """Test that a concrete implementation can be instantiated."""
        mock = MockConfigManager()
        assert isinstance(mock, ConfigurationInterface)

    def test_concrete_implementation_methods(self):
        """Test that concrete implementation methods work as expected."""
        mock = MockConfigManager()
        assert mock.load_configuration() is True
        assert mock.get_value("test") is None
        assert mock.get_environment() == "test"
