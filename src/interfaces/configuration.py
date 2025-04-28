"""
Interface for Configuration Management in DemoMaker.

This module defines the interface for the Configuration System,
which manages application settings across different environments.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigurationError(Exception):
    """Base exception for configuration errors."""

    pass


class ConfigurationLoadError(ConfigurationError):
    """Exception raised when loading configuration fails."""

    pass


class ConfigurationSaveError(ConfigurationError):
    """Exception raised when saving configuration fails."""

    pass


class ConfigurationValidationError(ConfigurationError):
    """Exception raised when configuration validation fails."""

    pass


class ConfigurationInterface(ABC):
    """Interface for Configuration System Module."""

    @abstractmethod
    def load_configuration(self, config_path: Optional[Path] = None) -> bool:
        """
        Load configuration from the specified path or default locations.

        Args:
            config_path: Path to a custom configuration file (optional)

        Returns:
            True if configuration was loaded successfully, False otherwise

        Raises:
            ConfigurationError: If loading the configuration fails
        """
        pass

    @abstractmethod
    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Args:
            key: Configuration key (can be a dot-notation path)
            default: Default value to return if key is not found

        Returns:
            Configuration value or default if not found
        """
        pass

    @abstractmethod
    def set_value(self, key: str, value: Any) -> bool:
        """
        Set a configuration value by key.

        Args:
            key: Configuration key (can be a dot-notation path)
            value: Value to set

        Returns:
            True if the value was set successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get an entire configuration section.

        Args:
            section: Name of the configuration section

        Returns:
            Dictionary containing the section's key-value pairs

        Raises:
            ConfigurationError: If the section is not found
        """
        pass

    @abstractmethod
    def save_configuration(self, config_path: Optional[Path] = None) -> bool:
        """
        Save configuration to the specified path or the path it was loaded from.

        Args:
            config_path: Path to save the configuration to (optional)

        Returns:
            True if configuration was saved successfully, False otherwise

        Raises:
            ConfigurationSaveError: If saving the configuration fails
        """
        pass

    @abstractmethod
    def validate_configuration(self, schema: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate the current configuration against a schema.

        Args:
            schema: JSON Schema to validate against

        Returns:
            True if the configuration is valid, False otherwise

        Raises:
            ConfigurationValidationError: If validation fails
        """
        pass

    @abstractmethod
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values.

        Returns:
            True if reset was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """
        Get the entire configuration.

        Returns:
            Dictionary containing all configuration key-value pairs
        """
        pass

    @abstractmethod
    def get_environment(self) -> str:
        """
        Get the current environment.

        Returns:
            The current environment (development, testing, production)
        """
        pass

    @abstractmethod
    def set_environment(self, environment: str) -> bool:
        """
        Set the current environment and reload environment-specific settings.

        Args:
            environment: The environment to use (development, testing, production)

        Returns:
            True if environment was set successfully, False otherwise
        """
        pass

    @abstractmethod
    def reload_configuration(self) -> bool:
        """
        Reload configuration from the original source.

        Returns:
            True if configuration was reloaded successfully, False otherwise
        """
        pass

    @abstractmethod
    def load_schema(self, schema_path: Path) -> bool:
        """
        Load a JSON schema for configuration validation.

        Args:
            schema_path: Path to the JSON schema file

        Returns:
            True if schema was loaded successfully, False otherwise
        """
        pass
