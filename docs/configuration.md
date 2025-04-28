# Configuration Management

The DemoMaker application uses a layered configuration system that supports multiple environments (development, testing, production) and allows for flexible customization. This documentation explains how the configuration system works and how to use it effectively.

## Overview

The configuration system is designed with several key principles:

1. **Layered Configuration** - Configuration values can come from multiple sources, with each layer overriding the previous one:
   - Default values hardcoded in the application
   - System-wide configuration file
   - User-specific configuration file
   - Environment variables
   - Command-line arguments

2. **Environment Support** - Different settings can be applied based on the current environment (development, testing, production)

3. **Validation** - Configuration values are validated against a schema to ensure correctness

4. **Security** - Sensitive information is handled securely and masked when saving configuration

## Configuration Files

DemoMaker supports configuration files in TOML and JSON formats. The application looks for configuration files in the following locations (in order):

1. `./config.toml` - Current directory
2. `./src/config/config.toml` - Source directory
3. `~/.demomaker/config.toml` - User's home directory

You can also specify a custom configuration file path when starting the application.

### Configuration File Structure

Configuration files should follow this structure:

```toml
# Default configuration applies to all environments
[default]
log_level = "INFO"
temp_dir = "temp"
allowed_image_formats = ["jpg", "jpeg", "png"]

# Environment-specific configuration
[development]
log_level = "DEBUG"
ai_model = "local"

[testing]
test_data_dir = "tests/data"

[production]
log_level = "WARNING"
ai_model = "cloud"
```

Common configuration options are placed in the `default` section, while environment-specific overrides are placed in their respective sections (`development`, `testing`, `production`).

## Environment Variables

You can override configuration values using environment variables. The environment variables should be prefixed with `DEMOMAKER_` followed by the configuration key with dots replaced by underscores.

For example:
- `DEMOMAKER_LOG_LEVEL=DEBUG` sets the `log_level` to `DEBUG`
- `DEMOMAKER_DATABASE_HOST=localhost` sets the `database.host` to `localhost`

Environment variables take precedence over values in configuration files.

## Using the Configuration System

### In Code

```python
from src.modules.configuration import Configuration

# Initialize configuration (defaults to "development" environment)
config = Configuration()

# Or specify an environment
config = Configuration("production")

# Get a configuration value
log_level = config.get_value("log_level")

# Get a nested value using dot notation
db_host = config.get_value("database.host")

# Get a value with a default if not found
timeout = config.get_value("timeout", 30)

# Get an entire section
db_config = config.get_section("database")

# Set a configuration value
config.set_value("log_level", "DEBUG")

# Save configuration
config.save_configuration()
```

### Command-Line Tool

A command-line tool is available to manage configuration:

```bash
# Show current configuration
python scripts/config_tool.py show

# Show a specific section
python scripts/config_tool.py show --section database

# Show a specific key
python scripts/config_tool.py show --key database.host

# Set a configuration value
python scripts/config_tool.py set database.host localhost

# Validate configuration
python scripts/config_tool.py validate --schema src/config/config.schema.json

# Specify environment
python scripts/config_tool.py --env production show
```

## Configuration Schema

The configuration schema defines the expected structure and validation rules for the configuration. The schema is defined in JSON Schema format and is located at `src/config/config.schema.json`.

## Best Practices

1. **Use Environment-Specific Configuration**: Place common settings in the `default` section and environment-specific overrides in their respective sections.

2. **Don't Store Secrets in Configuration Files**: Use environment variables for sensitive information like API keys and passwords.

3. **Validate Configuration**: Always validate configuration against the schema to catch errors early.

4. **Use Dot Notation**: When accessing nested configuration values, use dot notation to make the code more readable.

5. **Prefer Explicit Defaults**: When getting a configuration value, provide an explicit default value if applicable.

## Advanced Usage

### Configuration Validation

You can validate configuration against a schema:

```python
from pathlib import Path
from src.modules.configuration import Configuration

config = Configuration()
schema_path = Path("src/config/config.schema.json")
config.load_schema(schema_path)
is_valid = config.validate_configuration()
```

### Reloading Configuration

You can reload configuration from the source file:

```python
config = Configuration()
config.reload_configuration()
```

### Changing Environments

You can change the environment at runtime:

```python
config = Configuration("development")
# Later, switch to production
config.set_environment("production")
```

### Thread Safety

The configuration system is thread-safe, allowing multiple threads to safely access and modify configuration values concurrently.
