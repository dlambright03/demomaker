"""
Unit tests for the Configuration System Module.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import toml

from src.modules.configuration.config_manager import Configuration


class TestConfiguration(unittest.TestCase):
    """Test cases for the Configuration class."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Create a test config file
        self.test_config = {
            "default": {
                "log_level": "INFO",
                "temp_dir": "temp",
                "allowed_image_formats": ["jpg", "png"],
            },
            "development": {"log_level": "DEBUG", "ai_model": "local"},
            "testing": {"log_level": "DEBUG", "test_data_dir": "tests/data"},
            "production": {"log_level": "WARNING", "ai_model": "cloud"},
        }

        # Create test configuration files
        self.toml_config_path = self.temp_path / "config.toml"
        with open(self.toml_config_path, "w") as f:
            toml.dump(self.test_config, f)

        self.json_config_path = self.temp_path / "config.json"
        with open(self.json_config_path, "w") as f:
            json.dump(self.test_config, f)

        # Create a test schema
        self.test_schema = {
            "type": "object",
            "properties": {
                "log_level": {
                    "type": "string",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR"],
                },
                "temp_dir": {"type": "string"},
                "allowed_image_formats": {"type": "array", "items": {"type": "string"}},
            },
        }

        self.schema_path = self.temp_path / "schema.json"
        with open(self.schema_path, "w") as f:
            json.dump(self.test_schema, f)

    def tearDown(self):
        """Clean up test environment after each test."""
        self.temp_dir.cleanup()

    def test_init_with_default_paths(self):
        """Test initialization with default paths."""
        # Patch DEFAULT_CONFIG_PATHS to use our test config
        with patch.object(
            Configuration, "DEFAULT_CONFIG_PATHS", [self.toml_config_path]
        ):
            config = Configuration()
            self.assertEqual(config.get_value("log_level"), "DEBUG")
            self.assertEqual(config.get_environment(), "development")

    def test_load_toml_configuration(self):
        """Test loading configuration from TOML file."""
        config = Configuration()
        result = config.load_configuration(self.toml_config_path)
        self.assertTrue(result)
        self.assertEqual(config.get_value("temp_dir"), "temp")
        self.assertEqual(config.get_value("log_level"), "DEBUG")

    def test_load_json_configuration(self):
        """Test loading configuration from JSON file."""
        config = Configuration()
        result = config.load_configuration(self.json_config_path)
        self.assertTrue(result)
        self.assertEqual(config.get_value("temp_dir"), "temp")
        self.assertEqual(config.get_value("log_level"), "DEBUG")

    def test_environment_specific_settings(self):
        """Test that environment-specific settings are applied."""
        # Development environment
        config = Configuration("development")
        config.load_configuration(self.toml_config_path)
        self.assertEqual(config.get_value("log_level"), "DEBUG")
        self.assertEqual(config.get_value("ai_model"), "local")

        # Production environment
        config = Configuration("production")
        config.load_configuration(self.toml_config_path)
        self.assertEqual(config.get_value("log_level"), "WARNING")
        self.assertEqual(config.get_value("ai_model"), "cloud")

    def test_get_value_with_dot_notation(self):
        """Test getting values using dot notation."""
        # Create config with nested values
        nested_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {"username": "user", "password": "secret"},
            }
        }

        config_path = self.temp_path / "nested.json"
        with open(config_path, "w") as f:
            json.dump(nested_config, f)

        config = Configuration()
        config.load_configuration(config_path)

        self.assertEqual(config.get_value("database.host"), "localhost")
        self.assertEqual(config.get_value("database.port"), 5432)
        self.assertEqual(config.get_value("database.credentials.username"), "user")
        self.assertEqual(config.get_value("database.credentials.password"), "secret")
        self.assertIsNone(config.get_value("database.credentials.api_key"))
        self.assertEqual(
            config.get_value("database.credentials.api_key", "default_key"),
            "default_key",
        )

    def test_set_value_with_dot_notation(self):
        """Test setting values using dot notation."""
        config = Configuration()

        # Set values with dot notation
        config.set_value("database.host", "localhost")
        config.set_value("database.port", 5432)
        config.set_value("database.credentials.username", "user")

        self.assertEqual(config.get_value("database.host"), "localhost")
        self.assertEqual(config.get_value("database.port"), 5432)
        self.assertEqual(config.get_value("database.credentials.username"), "user")

        # Set value at existing path
        config.set_value("database.host", "newhost")
        self.assertEqual(config.get_value("database.host"), "newhost")

    def test_get_section(self):
        """Test getting an entire configuration section."""
        config = Configuration()
        config.load_configuration(self.toml_config_path)

        # Get default section
        default_section = config.get_section("default")
        self.assertEqual(default_section["log_level"], "INFO")
        self.assertEqual(default_section["temp_dir"], "temp")
        self.assertEqual(default_section["allowed_image_formats"], ["jpg", "png"])

        # Modifying the returned section should not affect the original
        default_section["log_level"] = "ERROR"
        self.assertEqual(config.get_value("log_level"), "DEBUG")  # Still "DEBUG"

    def test_save_configuration(self):
        """Test saving configuration to a file."""
        config = Configuration()
        config.load_configuration(self.toml_config_path)

        # Modify configuration
        config.set_value("new_setting", "value")

        # Save to a new file
        new_config_path = self.temp_path / "new_config.toml"
        result = config.save_configuration(new_config_path)
        self.assertTrue(result)
        self.assertTrue(new_config_path.exists())

        # Load the saved configuration and verify
        new_config = Configuration()
        new_config.load_configuration(new_config_path)
        self.assertEqual(new_config.get_value("new_setting"), "value")

        # Test JSON format
        json_config_path = self.temp_path / "new_config.json"
        result = config.save_configuration(json_config_path)
        self.assertTrue(result)
        self.assertTrue(json_config_path.exists())

    def test_reset_to_defaults(self):
        """Test resetting configuration to defaults."""
        with patch.object(
            Configuration, "DEFAULT_CONFIG_PATHS", [self.toml_config_path]
        ):
            config = Configuration()

            # Modify configuration
            config.set_value("custom_setting", "value")
            self.assertEqual(config.get_value("custom_setting"), "value")

            # Reset to defaults
            result = config.reset_to_defaults()
            self.assertTrue(result)

            # Custom setting should be gone, defaults restored
            self.assertIsNone(config.get_value("custom_setting"))
            self.assertEqual(config.get_value("log_level"), "DEBUG")

    def test_set_environment(self):
        """Test changing the environment at runtime."""
        config = Configuration("development")
        config.load_configuration(self.toml_config_path)
        self.assertEqual(config.get_value("log_level"), "DEBUG")

        # Change to production
        result = config.set_environment("production")
        self.assertTrue(result)
        self.assertEqual(config.get_environment(), "production")
        self.assertEqual(config.get_value("log_level"), "WARNING")

        # Change to invalid environment
        result = config.set_environment("invalid")
        self.assertFalse(result)
        self.assertEqual(config.get_environment(), "production")

    def test_reload_configuration(self):
        """Test reloading configuration."""
        config = Configuration()
        config.load_configuration(self.toml_config_path)

        # Modify the file
        new_config = dict(self.test_config)
        new_config["default"]["new_setting"] = "new_value"
        with open(self.toml_config_path, "w") as f:
            toml.dump(new_config, f)

        # Reload
        result = config.reload_configuration()
        self.assertTrue(result)

        # New setting should be available
        self.assertEqual(config.get_value("new_setting"), "new_value")


if __name__ == "__main__":
    unittest.main()
