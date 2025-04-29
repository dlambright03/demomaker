"""
AI Provider Factory.

This module provides a factory for creating AI providers for script generation.
"""

import logging
from typing import Any, Dict, Optional

from src.modules.script_generator.ai_providers.base_provider import BaseAIProvider
from src.modules.script_generator.ai_providers.local_provider import LocalProvider
from src.modules.script_generator.ai_providers.openai_provider import OpenAIProvider

# Configure logging
logger = logging.getLogger(__name__)


class AIProviderFactory:
    """Factory for creating AI providers."""

    # Map of provider names to their implementation classes
    _PROVIDERS = {
        "local-model": LocalProvider,
        "gpt-3.5-turbo": OpenAIProvider,
        "gpt-4": OpenAIProvider,
        "gpt-4-vision-preview": OpenAIProvider,
        "openai": OpenAIProvider,
        # Add more providers here as they are implemented
        # "claude-instant": ClaudeProvider,
        # "claude-2": ClaudeProvider,
    }

    @classmethod
    def create_provider(
        cls, model_name: str, config: Optional[Dict[str, Any]] = None
    ) -> BaseAIProvider:
        """
        Create an AI provider for the specified model.

        Args:
            model_name: Name of the model to use
            config: Optional configuration for the provider

        Returns:
            An initialized AI provider

        Raises:
            ValueError: If the model is not supported
        """
        provider_class = cls._get_provider_class(model_name)
        provider_config = config or {}

        # Add model-specific configurations
        if model_name.startswith("gpt"):
            if model_name == "gpt-4-vision-preview":
                provider_config["vision_model"] = model_name
            else:
                provider_config["chat_model"] = model_name

        # Create and initialize the provider
        provider = provider_class(provider_config)

        # Initialize with API key if present in config
        api_key = provider_config.get("api_key")
        if api_key:
            provider.initialize(api_key=api_key)
        else:
            provider.initialize()

        return provider

    @classmethod
    def _get_provider_class(cls, model_name: str) -> type:
        """
        Get the provider class for the specified model.

        Args:
            model_name: Name of the model

        Returns:
            The provider class

        Raises:
            ValueError: If the model is not supported
        """
        provider_class = cls._PROVIDERS.get(model_name)
        if not provider_class:
            # If not found directly, try to find a partial match
            for provider_key, provider_value in cls._PROVIDERS.items():
                if provider_key in model_name:
                    provider_class = provider_value
                    break

        if not provider_class:
            # If still not found, default to local provider with a warning
            logger.warning(
                f"Model '{model_name}' not recognized. Using local provider."
            )
            provider_class = LocalProvider

        return provider_class

    @classmethod
    def get_available_models(cls) -> list:
        """
        Get a list of available models.

        Returns:
            List of available model names
        """
        return list(cls._PROVIDERS.keys())
