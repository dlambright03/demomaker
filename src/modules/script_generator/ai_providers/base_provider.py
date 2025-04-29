"""
Base AI Provider implementation.

This module provides a base implementation of the AI provider interface
that can be extended by specific providers.
"""

import logging
from typing import Any, Dict, Optional

from src.modules.script_generator.ai_providers import AIProviderInterface

# Configure logging
logger = logging.getLogger(__name__)


class BaseAIProvider(AIProviderInterface):
    """Base implementation of the AI provider interface."""

    def __init__(self, provider_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the base AI provider.

        Args:
            provider_name: Name of the provider
            config: Optional configuration dictionary
        """
        self._name = provider_name
        self._config = config or {}
        self._api_key = self._config.get("api_key")
        self._initialized = False

    def initialize(self, api_key: Optional[str] = None, **kwargs) -> bool:
        """
        Initialize the AI provider with credentials.

        Args:
            api_key: Optional API key for the provider
            kwargs: Additional initialization parameters

        Returns:
            True if initialization succeeded, False otherwise
        """
        try:
            # Set API key if provided
            if api_key:
                self._api_key = api_key

            # Call provider-specific initialization
            self._initialize_client()
            self._validate_config()

            self._initialized = True
            return True

        except Exception as e:
            logger.error(f"Error initializing {self._name} provider: {str(e)}")
            self._initialized = False
            return False

    def is_available(self) -> bool:
        """
        Check if the AI provider is available.

        Returns:
            True if the provider is initialized and available, False otherwise
        """
        return self._initialized

    def _validate_config(self) -> None:
        """
        Validate the configuration parameters.

        This method should be overridden by subclasses to validate
        provider-specific configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        pass

    def _initialize_client(self) -> None:
        """
        Initialize the client for the AI provider.

        This method should be overridden by subclasses to initialize
        provider-specific clients or connections.

        Raises:
            Exception: If client initialization fails
        """
        pass
