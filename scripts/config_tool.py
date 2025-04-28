#!/usr/bin/env python3
"""
Configuration Management Tool

A command-line tool for managing DemoMaker configuration.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import toml

from src.modules.configuration.config_manager import Configuration


def get_config_path(args):
    """Get the configuration path from arguments or default."""
    if args.config:
        return Path(args.config)

    # Try the default paths
    for path in Configuration.DEFAULT_CONFIG_PATHS:
        if path.exists():
            return path

    # If no config exists, use the first default path
    return Configuration.DEFAULT_CONFIG_PATHS[0]


def show_config(args):
    """Display the current configuration."""
    config = Configuration(args.env)
    config_path = get_config_path(args)

    if not config_path.exists():
        print(f"No configuration file found at {config_path}")
        return 1

    print(f"Loading configuration from {config_path}")
    config.load_configuration(config_path)

    if args.section:
        # Show a specific section
        try:
            section_data = config.get_section(args.section)
            print(f"\nSection: {args.section}")
            print(json.dumps(section_data, indent=2))
        except Exception as e:
            print(f"Error getting section: {str(e)}")
            return 1
    elif args.key:
        # Show a specific key
        value = config.get_value(args.key)
        if value is None:
            print(f"Key not found: {args.key}")
            return 1

        print(f"\nKey: {args.key}")
        if isinstance(value, (dict, list)):
            print(json.dumps(value, indent=2))
        else:
            print(value)
    else:
        # Show the entire configuration
        all_config = config.get_all()
        print("\nCurrent configuration:")
        print(json.dumps(all_config, indent=2))

        # Show the current environment
        print(f"\nCurrent environment: {config.get_environment()}")

    return 0


def set_value(args):
    """Set a configuration value."""
    config = Configuration(args.env)
    config_path = get_config_path(args)

    if not args.key:
        print("Error: Key is required for set operation")
        return 1

    if args.value is None:
        print("Error: Value is required for set operation")
        return 1

    # Load existing configuration
    if config_path.exists():
        print(f"Loading configuration from {config_path}")
        config.load_configuration(config_path)

    # Parse the value according to its type
    try:
        # Try to parse as JSON
        value = json.loads(args.value)
    except json.JSONDecodeError:
        # Use as string if not valid JSON
        value = args.value

    # Set the value
    result = config.set_value(args.key, value)
    if not result:
        print(f"Failed to set value for key: {args.key}")
        return 1

    print(f"Value set for key: {args.key}")

    # Save the configuration
    print(f"Saving configuration to {config_path}")
    if not config.save_configuration(config_path):
        print("Failed to save configuration")
        return 1

    print("Configuration saved successfully")
    return 0


def validate_config(args):
    """Validate the configuration against a schema."""
    config = Configuration(args.env)
    config_path = get_config_path(args)

    if not config_path.exists():
        print(f"No configuration file found at {config_path}")
        return 1

    print(f"Loading configuration from {config_path}")
    config.load_configuration(config_path)

    # Load schema if provided
    schema = None
    if args.schema:
        schema_path = Path(args.schema)
        if not schema_path.exists():
            print(f"Schema file not found: {schema_path}")
            return 1

        print(f"Loading schema from {schema_path}")
        config.load_schema(schema_path)

    # Validate configuration
    try:
        result = config.validate_configuration()
        if result:
            print("Configuration is valid!")
            return 0
        else:
            print("Configuration validation failed")
            return 1
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return 1


def main():
    """Main entry point for the configuration tool."""
    parser = argparse.ArgumentParser(
        description="DemoMaker Configuration Management Tool"
    )

    # Global options
    parser.add_argument("-c", "--config", help="Path to configuration file")
    parser.add_argument(
        "-e",
        "--env",
        choices=["development", "testing", "production"],
        help="Environment to use",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show configuration")
    show_parser.add_argument("-s", "--section", help="Show only a specific section")
    show_parser.add_argument(
        "-k", "--key", help="Show only a specific key (dot notation supported)"
    )

    # Set command
    set_parser = subparsers.add_parser("set", help="Set configuration value")
    set_parser.add_argument(
        "key", help="Configuration key to set (dot notation supported)"
    )
    set_parser.add_argument(
        "value", help="Value to set (will be parsed as JSON if possible)"
    )

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate configuration")
    validate_parser.add_argument("-s", "--schema", help="Path to JSON schema file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "show":
        return show_config(args)
    elif args.command == "set":
        return set_value(args)
    elif args.command == "validate":
        return validate_config(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
