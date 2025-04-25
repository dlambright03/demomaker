"""
Unit tests for the Narration Generator Interface.

This module contains tests that verify the NarrationGeneratorInterface design,
including method signatures and exception classes.
"""

from abc import ABC
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.interfaces.narration_generator import (
    AudioProcessingError,
    InvalidScriptError,
    NarrationGenerationError,
    NarrationGeneratorInterface,
    TimingAdjustmentError,
    TTSServiceError,
    VoiceNotAvailableError,
)


class TestNarrationGeneratorInterface:
    """Tests for the NarrationGeneratorInterface class."""

    def test_is_abstract_base_class(self):
        """Test that NarrationGeneratorInterface is an abstract base class."""
        assert issubclass(NarrationGeneratorInterface, ABC)

        # Verify we can't instantiate it directly
        with pytest.raises(TypeError):
            NarrationGeneratorInterface()

    def test_required_methods(self):
        """Test that NarrationGeneratorInterface has all required abstract methods."""
        required_methods = [
            "generate_narration",
            "set_voice",
            "get_available_voices",
            "set_speech_rate",
            "set_speech_pitch",
            "estimate_narration_time",
            "cancel_generation",
            "split_narration_by_segment",
            "adjust_timing",
        ]

        for method in required_methods:
            assert hasattr(NarrationGeneratorInterface, method)
            assert getattr(NarrationGeneratorInterface, method).__isabstractmethod__

    def test_method_signatures(self):
        """Test method signatures have the correct parameters and return types."""
        # Sample method signature tests
        generate_narration = NarrationGeneratorInterface.generate_narration
        assert "script" in generate_narration.__annotations__
        assert "output_dir" in generate_narration.__annotations__
        assert generate_narration.__annotations__["return"] == Path

        set_voice = NarrationGeneratorInterface.set_voice
        assert "voice_id" in set_voice.__annotations__
        assert set_voice.__annotations__["return"] is None

        # Add more signature tests as needed

    def test_exception_hierarchy(self):
        """Test that the exception hierarchy is properly structured."""
        # NarrationGenerationError is the base exception
        assert issubclass(NarrationGenerationError, Exception)

        # Other exceptions inherit from NarrationGenerationError
        assert issubclass(TTSServiceError, NarrationGenerationError)
        assert issubclass(InvalidScriptError, NarrationGenerationError)
        assert issubclass(VoiceNotAvailableError, NarrationGenerationError)
        assert issubclass(AudioProcessingError, NarrationGenerationError)
        assert issubclass(TimingAdjustmentError, NarrationGenerationError)


# Mock implementation for testing inheritance
class MockNarrationGenerator(NarrationGeneratorInterface):
    """Mock implementation of NarrationGeneratorInterface for testing."""

    def generate_narration(self, script: Dict[str, Any], output_dir: Path) -> Path:
        return Path("/mock/output/narration.mp3")

    def set_voice(self, voice_id: str) -> None:
        pass

    def get_available_voices(self) -> List[Dict[str, Any]]:
        return [{"id": "voice1", "name": "Mock Voice"}]

    def set_speech_rate(self, rate: float) -> None:
        pass

    def set_speech_pitch(self, pitch: float) -> None:
        pass

    def estimate_narration_time(self, script: Dict[str, Any]) -> int:
        return 60

    def cancel_generation(self) -> bool:
        return True

    def split_narration_by_segment(
        self, narration_file: Path, script: Dict[str, Any]
    ) -> List[Path]:
        return [Path("/mock/output/segment_1.mp3")]

    def adjust_timing(
        self, narration_segments: List[Path], script: Dict[str, Any]
    ) -> Dict[str, Any]:
        return script
