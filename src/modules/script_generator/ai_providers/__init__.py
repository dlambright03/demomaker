"""
AI Provider interfaces and implementations.
"""

import abc
from typing import Any, Dict, List, Optional


class AIProviderInterface(abc.ABC):
    """Interface for AI providers used in script generation."""

    @abc.abstractmethod
    def initialize(self, api_key: Optional[str] = None, **kwargs) -> bool:
        """Initialize the AI provider with credentials."""
        pass

    @abc.abstractmethod
    def is_available(self) -> bool:
        """Check if the AI provider is available."""
        pass

    @abc.abstractmethod
    def analyze_image_content(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze image content using the AI provider."""
        pass

    @abc.abstractmethod
    def generate_script_from_images(
        self, image_analyses: List[Dict[str, Any]], description: str
    ) -> Dict[str, Any]:
        """Generate a script from a set of analyzed images."""
        pass
