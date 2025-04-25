"""
Unit tests for the Video Assembler Interface.

This module contains tests that verify the VideoAssemblerInterface design,
including method signatures and exception classes.
"""

from abc import ABC
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.interfaces.video_assembler import (
    FFMPEGError,
    FormatNotSupportedError,
    ResolutionNotSupportedError,
    VideoAssemblerInterface,
    VideoAssemblyError,
)


class TestVideoAssemblerInterface:
    """Tests for the VideoAssemblerInterface class."""

    def test_is_abstract_base_class(self):
        """Test that VideoAssemblerInterface is an abstract base class."""
        assert issubclass(VideoAssemblerInterface, ABC)

        # Verify we can't instantiate it directly
        with pytest.raises(TypeError):
            VideoAssemblerInterface()

    def test_required_methods(self):
        """Test that VideoAssemblerInterface has all required abstract methods."""
        required_methods = [
            "assemble_video",
            "set_output_format",
            "set_output_resolution",
            "set_transition_style",
            "set_transition_duration",
            "get_supported_formats",
            "get_supported_transitions",
            "add_watermark",
            "add_background_music",
            "create_preview",
            "estimate_assembly_time",
            "cancel_assembly",
        ]

        for method in required_methods:
            assert hasattr(VideoAssemblerInterface, method)
            assert getattr(VideoAssemblerInterface, method).__isabstractmethod__

    def test_method_signatures(self):
        """Test method signatures have the correct parameters and return types."""
        # Sample method signature tests
        assemble_video = VideoAssemblerInterface.assemble_video
        assert "images" in assemble_video.__annotations__
        assert "narration_audio" in assemble_video.__annotations__
        assert "script" in assemble_video.__annotations__
        assert "output_path" in assemble_video.__annotations__
        assert "title" in assemble_video.__annotations__
        assert assemble_video.__annotations__["return"] == Path

        set_output_format = VideoAssemblerInterface.set_output_format
        assert "format_name" in set_output_format.__annotations__
        assert set_output_format.__annotations__["return"] is None

        # Add more signature tests as needed

    def test_exception_hierarchy(self):
        """Test that the exception hierarchy is properly structured."""
        # VideoAssemblyError is the base exception
        assert issubclass(VideoAssemblyError, Exception)

        # Other exceptions inherit from VideoAssemblyError
        assert issubclass(FormatNotSupportedError, VideoAssemblyError)
        assert issubclass(ResolutionNotSupportedError, VideoAssemblyError)
        assert issubclass(FFMPEGError, VideoAssemblyError)


# Mock implementation for testing inheritance
class MockVideoAssembler(VideoAssemblerInterface):
    """Mock implementation of VideoAssemblerInterface for testing."""

    def assemble_video(
        self,
        images: List[Path],
        narration_audio: Path,
        script: Dict[str, Any],
        output_path: Path,
        title=None,
    ) -> Path:
        return Path("/mock/output/video.mp4")

    def set_output_format(self, format_name: str) -> None:
        pass

    def set_output_resolution(self, width: int, height: int) -> None:
        pass

    def set_transition_style(self, style: str) -> None:
        pass

    def set_transition_duration(self, duration: float) -> None:
        pass

    def get_supported_formats(self) -> List[str]:
        return ["mp4", "webm"]

    def get_supported_transitions(self) -> List[str]:
        return ["fade", "dissolve", "slide"]

    def add_watermark(self, image_path: Path) -> None:
        pass

    def add_background_music(self, audio_path: Path, volume: float = 0.2) -> None:
        pass

    def create_preview(
        self, images: List[Path], script: Dict[str, Any], preview_path: Path
    ) -> Path:
        return Path("/mock/output/preview.mp4")

    def estimate_assembly_time(self, num_images: int, video_duration: int) -> int:
        return 120

    def cancel_assembly(self) -> bool:
        return True
