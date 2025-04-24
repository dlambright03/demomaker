"""
Interface for the Configuration System Module.

This module is responsible for managing configuration settings for the
DemoMaker application across different environments (development, testing, production).
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, Union


class ConfigurationInterface(ABC):
    """Interface for the Configuration System Module."""
    
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
        Save current configuration to a file.
        
        Args:
            config_path: Path to save the configuration to (optional)
            
        Returns:
            True if configuration was saved successfully, False otherwise
            
        Raises:
            ConfigurationError: If saving the configuration fails
        """
        pass
    
    @abstractmethod
    def get_environment(self) -> str:
        """
        Get the current environment (development, testing, production).
        
        Returns:
            String representing the current environment
        """
        pass
    
    @abstractmethod
    def set_environment(self, environment: str) -> bool:
        """
        Set the current environment and load corresponding configuration.
        
        Args:
            environment: Environment name (development, testing, production)
            
        Returns:
            True if environment was set successfully, False otherwise
            
        Raises:
            ValueError: If the environment name is invalid
        """
        pass
    
    @abstractmethod
    def reload_configuration(self) -> bool:
        """
        Reload configuration from all sources.
        
        Returns:
            True if configuration was reloaded successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def validate_configuration(self) -> Dict[str, List[str]]:
        """
        Validate current configuration against schema.
        
        Returns:
            Dictionary of validation errors by section
        """
        pass
    
    @abstractmethod
    def get_configuration_schema(self) -> Dict[str, Any]:
        """
        Get the configuration schema.
        
        Returns:
            Dictionary representing the configuration schema
        """
        pass
