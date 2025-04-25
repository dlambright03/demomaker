"""
Implementation of the Configuration System Module.

This module manages configuration settings for the DemoMaker application
across different environments (development, testing, production).
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import toml

from src.interfaces.configuration import (
    ConfigurationError,
    ConfigurationInterface,
    ConfigurationLoadError,
    ConfigurationSaveError,
    ConfigurationValidationError,
)


class Configuration(ConfigurationInterface):
    """Implementation of the Configuration System Module."""

    DEFAULT_CONFIG_PATHS = [
        Path("./config.toml"),
        Path("./src/config/config.toml"),
        Path(os.path.expanduser("~/.demomaker/config.toml")),
    ]

    def __init__(self):
        """Initialize the Configuration object."""
        self._config_data = {}
        self._config_path = None
        # Try to load configuration from default paths
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                self.load_configuration(path)
                break

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
        if config_path is None:
            # Try default paths
            for path in self.DEFAULT_CONFIG_PATHS:
                if path.exists():
                    config_path = path
                    break
            if config_path is None:
                return False

        try:
            if not config_path.exists():
                return False

            self._config_path = config_path
            file_extension = config_path.suffix.lower()

            if file_extension == ".toml":
                with open(config_path, "r", encoding="utf-8") as file:
                    self._config_data = toml.load(file)
            elif file_extension in (".json", ".jsonc"):
                with open(config_path, "r", encoding="utf-8") as file:
                    self._config_data = json.load(file)
            else:
                raise ConfigurationLoadError(
                    f"Unsupported configuration file format: {file_extension}"
                )

            return True
        except Exception as e:
            raise ConfigurationLoadError(
                f"Failed to load configuration: {str(e)}"
            ) from e

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Args:
            key: Configuration key (can be a dot-notation path)
            default: Default value to return if key is not found

        Returns:
            Configuration value or default if not found
        """
        if not key:
            return default

        # Handle dot notation
        parts = key.split(".")
        current = self._config_data

        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]

        return current

    def set_value(self, key: str, value: Any) -> bool:
        """
        Set a configuration value by key.

        Args:
            key: Configuration key (can be a dot-notation path)
            value: Value to set

        Returns:
            True if the value was set successfully, False otherwise
        """
        if not key:
            return False

        # Handle dot notation
        parts = key.split(".")
        current = self._config_data

        # Navigate to the last dict in the path
        for i, part in enumerate(parts[:-1]):
            if not isinstance(current, dict):
                return False
            if part not in current:
                current[part] = {}
            current = current[part]

        if not isinstance(current, dict):
            return False

        # Set the value
        current[parts[-1]] = value
        return True

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
        value = self.get_value(section)
        if not isinstance(value, dict):
            raise ConfigurationError(f"Section not found: {section}")
        return value

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
        if config_path is None:
            if self._config_path is None:
                return False
            config_path = self._config_path

        try:
            # Create parent directories if they don't exist
            config_path.parent.mkdir(parents=True, exist_ok=True)

            file_extension = config_path.suffix.lower()

            if file_extension == ".toml":
                with open(config_path, "w", encoding="utf-8") as file:
                    toml.dump(self._config_data, file)
            elif file_extension in (".json", ".jsonc"):
                with open(config_path, "w", encoding="utf-8") as file:
                    json.dump(self._config_data, file, indent=2)
            else:
                raise ConfigurationSaveError(
                    f"Unsupported configuration file format: {file_extension}"
                )

            return True
        except Exception as e:
            raise ConfigurationSaveError(
                f"Failed to save configuration: {str(e)}"
            ) from e

    def validate_configuration(self, schema: Dict[str, Any]) -> bool:
        """
        Validate the current configuration against a schema.

        Args:
            schema: JSON Schema to validate against

        Returns:
            True if the configuration is valid, False otherwise

        Raises:
            ConfigurationValidationError: If validation fails
        """
        try:
            # This would use a JSON schema validator like jsonschema
            # For now, this is a placeholder
            # import jsonschema
            # jsonschema.validate(self._config_data, schema)
            return True
        except Exception as e:
            raise ConfigurationValidationError(
                f"Configuration validation failed: {str(e)}"
            ) from e

    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values.

        Returns:
            True if reset was successful, False otherwise
        """
        try:
            # This would load default configuration values
            # For now, this is a placeholder that simply clears the configuration
            self._config_data = {}
            return True
        except Exception:
            return False

    def get_all(self) -> Dict[str, Any]:
        """
        Get the entire configuration.

        Returns:
            Dictionary containing all configuration key-value pairs
        """
        return self._config_data.copy()
