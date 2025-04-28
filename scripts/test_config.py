#!/usr/bin/env python3
"""
Simple test for the Configuration module.
"""

import json
import tempfile
from pathlib import Path

from src.modules.configuration.config_manager import Configuration


def main():
    """Run a simple test of the Configuration class."""
    # Create a temporary test configuration
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_path = temp_path / "config.json"

        # Create a test config file
        test_config = {
            "default": {"log_level": "INFO", "temp_dir": "temp"},
            "development": {"log_level": "DEBUG"},
        }

        with open(config_path, "w") as f:
            json.dump(test_config, f)

        # Test the Configuration class
        config = Configuration()
        print(f"Default environment: {config.get_environment()}")

        config.load_configuration(config_path)
        print(f"Loaded configuration from: {config_path}")

        log_level = config.get_value("log_level")
        print(f"log_level: {log_level}")

        temp_dir = config.get_value("temp_dir")
        print(f"temp_dir: {temp_dir}")

        # Test setting a value
        config.set_value("new_setting", "test_value")
        new_value = config.get_value("new_setting")
        print(f"new_setting: {new_value}")

        # Test saving configuration
        new_config_path = temp_path / "new_config.json"
        config.save_configuration(new_config_path)
        print(f"Saved configuration to: {new_config_path}")

        print("Configuration test completed successfully!")


if __name__ == "__main__":
    main()
