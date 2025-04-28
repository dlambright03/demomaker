"""
Configuration System Module for DemoMaker.

This module exports the Configuration class for managing application settings
across different environments (development, testing, production).
"""

from .config_manager import Configuration

__all__ = ["Configuration"]
