"""
Implementation of the Video Assembler Module.

This module is responsible for combining images, scripts, and narration
into the final demo video output.
"""

import json
import logging
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from src.interfaces.video_assembler import (
    AudioSyncError,
    EncodingError,
    FrameGenerationError,
    TransitionError,
    VideoAssemblerInterface,
    VideoAssemblyError,
    VideoAssemblyTimeoutError,
)

# Configure logging
logger = logging.getLogger(__name__)


class VideoAssembler(VideoAssemblerInterface):
    """Implementation of the Video Assembler Module."""

    # Default output settings
    DEFAULT_RESOLUTION = (1920, 1080)  # Full HD
    DEFAULT_FPS = 30
    DEFAULT_FORMAT = "mp4"
    DEFAULT_CODEC = "h264"

    def __init__(self):
        """Initialize the VideoAssembler."""
        self._resolution = self.DEFAULT_RESOLUTION
        self._fps = self.DEFAULT_FPS
        self._format = self.DEFAULT_FORMAT
        self._codec = self.DEFAULT_CODEC
        self._is_assembling = False
        self._progress_callback = None

    def assemble_video(
        self,
        images: List[Path],
        script: Dict[str, Any],
        narration: Path,
        output_path: Path,
    ) -> Path:
        """
        Assemble a video from images, script, and narration.

        Args:
            images: List of paths to input images
            script: Dictionary containing the script with timing information
            narration: Path to the narration audio file
            output_path: Path to save the output video

        Returns:
            Path to the generated video file

        Raises:
            VideoAssemblyError: If video assembly fails
        """
        try:
            # Mark assembly as started
            self._is_assembling = True
            self._report_progress(0, "Preparing video assembly")

            # Validate inputs
            self._validate_inputs(images, script, narration, output_path)

            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create a temporary working directory
            temp_dir = output_path.parent / f"temp_assembly_{int(time.time())}"
            temp_dir.mkdir(exist_ok=True)

            try:
                # Step 1: Generate frames for each segment
                self._report_progress(10, "Generating video frames")
                frame_paths = self._generate_frames(images, script, temp_dir)

                # Step 2: Add transitions between segments
                self._report_progress(40, "Adding transitions")
                transitions_paths = self._generate_transitions(
                    frame_paths, script, temp_dir
                )

                # Step 3: Combine frames with narration
                self._report_progress(70, "Combining frames with audio")
                output_file = self._encode_video(
                    transitions_paths, narration, output_path
                )

                # Step 4: Finalize video
                self._report_progress(90, "Finalizing video")
                finalized_output = self._finalize_video(output_file, script)

                self._report_progress(100, "Video assembly completed")
                self._is_assembling = False

                return finalized_output

            finally:
                # Clean up temporary directory
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

        except Exception as e:
            self._is_assembling = False
            logger.error(f"Error assembling video: {str(e)}", exc_info=True)
            raise VideoAssemblyError(f"Failed to assemble video: {str(e)}") from e

    def set_resolution(self, width: int, height: int) -> None:
        """
        Set the output video resolution.

        Args:
            width: Video width in pixels
            height: Video height in pixels

        Raises:
            ValueError: If the resolution is invalid
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid resolution: {width}x{height}")

        self._resolution = (width, height)
        logger.info(f"Video resolution set to: {width}x{height}")

    def set_frame_rate(self, fps: int) -> None:
        """
        Set the output video frame rate.

        Args:
            fps: Frames per second

        Raises:
            ValueError: If the frame rate is invalid
        """
        if fps <= 0 or fps > 240:
            raise ValueError(f"Invalid frame rate: {fps}")

        self._fps = fps
        logger.info(f"Video frame rate set to: {fps} fps")

    def set_output_format(self, format: str, codec: Optional[str] = None) -> None:
        """
        Set the output video format.

        Args:
            format: Output format (e.g., mp4, mov, avi)
            codec: Video codec to use (optional)

        Raises:
            ValueError: If the format is unsupported
        """
        valid_formats = ["mp4", "mov", "avi", "webm", "mkv"]
        if format.lower() not in valid_formats:
            raise ValueError(f"Unsupported video format: {format}")

        self._format = format.lower()

        if codec:
            self._codec = codec

        logger.info(f"Video format set to: {self._format} with codec: {self._codec}")

    def register_progress_callback(self, callback: callable) -> None:
        """
        Register a callback function to report progress.

        Args:
            callback: Function that takes (progress_percentage, status_message)
        """
        self._progress_callback = callback
        logger.debug("Progress callback registered")

    def cancel_assembly(self) -> bool:
        """
        Cancel an ongoing video assembly process.

        Returns:
            True if cancellation was successful, False otherwise
        """
        if not self._is_assembling:
            return False

        logger.info("Cancelling video assembly...")
        self._is_assembling = False

        return True

    def estimate_assembly_time(self, num_images: int, video_duration: int) -> int:
        """
        Estimate the time required to assemble a video.

        Args:
            num_images: Number of images in the input
            video_duration: Duration of the video in seconds

        Returns:
            Estimated time in seconds
        """
        # Base time for initialization
        estimated_time = 5

        # Time for frame generation
        estimated_time += num_images * 2

        # Time for transitions
        estimated_time += (num_images - 1) * 1

        # Time for encoding (based on video duration and resolution)
        encoding_factor = 0.5
        if self._resolution[0] >= 1920:  # HD or higher
            encoding_factor = 1.0

        estimated_time += video_duration * encoding_factor

        # Time for finalization
        estimated_time += 10

        return int(estimated_time)

    def get_supported_formats(self) -> List[Dict[str, Any]]:
        """
        Get a list of supported output formats and codecs.

        Returns:
            A list of dictionaries containing format information
        """
        return [
            {
                "format": "mp4",
                "codecs": ["h264", "h265", "vp9"],
                "description": "MPEG-4 Part 14 (MP4) - Widely supported format",
            },
            {
                "format": "mov",
                "codecs": ["h264", "prores"],
                "description": "QuickTime File Format - Good for Apple devices",
            },
            {
                "format": "webm",
                "codecs": ["vp8", "vp9"],
                "description": "WebM - Optimized for web playback",
            },
            {
                "format": "mkv",
                "codecs": ["h264", "h265", "vp9", "av1"],
                "description": "Matroska - Container format supporting many codecs",
            },
            {
                "format": "avi",
                "codecs": ["xvid", "mjpeg"],
                "description": "Audio Video Interleave - Legacy format",
            },
        ]

    def _validate_inputs(
        self,
        images: List[Path],
        script: Dict[str, Any],
        narration: Path,
        output_path: Path,
    ) -> None:
        """
        Validate that all input parameters are valid.

        Args:
            images: List of paths to input images
            script: Dictionary containing the script with timing information
            narration: Path to the narration audio file
            output_path: Path to save the output video

        Raises:
            ValueError: If any input is invalid
        """
        # Check images
        if not images:
            raise ValueError("No images provided")

        for img_path in images:
            if not img_path.exists() or not img_path.is_file():
                raise ValueError(f"Image not found: {img_path}")

        # Check script
        if not script:
            raise ValueError("No script provided")

        if "segments" not in script:
            raise ValueError("Invalid script format: missing segments")

        # Check narration
        if not narration.exists() or not narration.is_file():
            raise ValueError(f"Narration file not found: {narration}")

        # Check output path
        if output_path.exists() and output_path.is_dir():
            raise ValueError(f"Output path is a directory: {output_path}")

        # Ensure output directory exists or can be created
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create output directory: {str(e)}")

    def _generate_frames(
        self, images: List[Path], script: Dict[str, Any], temp_dir: Path
    ) -> List[Path]:
        """
        Generate frames for each script segment.

        Args:
            images: List of paths to input images
            script: Dictionary containing the script with timing information
            temp_dir: Temporary directory for storing frames

        Returns:
            List of paths to generated frame sequences

        Raises:
            FrameGenerationError: If frame generation fails
        """
        try:
            # Create frames directory
            frames_dir = temp_dir / "frames"
            frames_dir.mkdir(exist_ok=True)

            segments = script.get("segments", [])
            frame_sequences = []

            for i, segment in enumerate(segments):
                # Create segment directory
                segment_dir = frames_dir / f"segment_{i:03d}"
                segment_dir.mkdir(exist_ok=True)

                # Get the image for this segment
                if i < len(images):
                    image_path = images[i]
                else:
                    # Use the last image if we have more segments than images
                    image_path = images[-1]

                # In a real implementation, this would generate frames for each segment
                # including any effects, zooms, pans, etc.

                # For now, just create a placeholder file
                info_file = segment_dir / "info.json"
                with open(info_file, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "segment_id": segment.get("id", f"segment_{i}"),
                            "image_path": str(image_path),
                            "duration": segment.get("duration", 5),
                            "narration": segment.get("narration", ""),
                        },
                        f,
                        indent=2,
                    )

                frame_sequences.append(segment_dir)

            logger.info(f"Generated frames for {len(frame_sequences)} segments")

            return frame_sequences

        except Exception as e:
            logger.error(f"Error generating frames: {str(e)}", exc_info=True)
            raise FrameGenerationError(f"Failed to generate frames: {str(e)}") from e

    def _generate_transitions(
        self, frame_sequences: List[Path], script: Dict[str, Any], temp_dir: Path
    ) -> List[Path]:
        """
        Generate transitions between segments.

        Args:
            frame_sequences: List of paths to frame sequences
            script: Dictionary containing the script with timing information
            temp_dir: Temporary directory for storing transitions

        Returns:
            List of paths to frame sequences with transitions

        Raises:
            TransitionError: If transition generation fails
        """
        try:
            # Create transitions directory
            transitions_dir = temp_dir / "transitions"
            transitions_dir.mkdir(exist_ok=True)

            # In a real implementation, this would generate transition frames
            # between segments (fades, dissolves, etc.)

            # For now, just create placeholder files
            for i in range(len(frame_sequences) - 1):
                transition_dir = transitions_dir / f"transition_{i:03d}"
                transition_dir.mkdir(exist_ok=True)

                # Create info file with transition details
                info_file = transition_dir / "info.json"
                with open(info_file, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "from_segment": i,
                            "to_segment": i + 1,
                            "type": "fade",
                            "duration": 1.0,
                        },
                        f,
                        indent=2,
                    )

            logger.info(f"Generated {len(frame_sequences) - 1} transitions")

            # Return the original frame sequences
            # In a real implementation, this would return modified sequences with transitions
            return frame_sequences

        except Exception as e:
            logger.error(f"Error generating transitions: {str(e)}", exc_info=True)
            raise TransitionError(f"Failed to generate transitions: {str(e)}") from e

    def _encode_video(
        self, frame_sequences: List[Path], narration: Path, output_path: Path
    ) -> Path:
        """
        Encode the video with frames and narration.

        Args:
            frame_sequences: List of paths to frame sequences
            narration: Path to the narration audio file
            output_path: Path to save the output video

        Returns:
            Path to the encoded video

        Raises:
            EncodingError: If video encoding fails
        """
        try:
            # In a real implementation, this would use a video encoding library like FFmpeg
            # to combine frames and audio into a video

            # For this placeholder implementation, just create a mock video file
            with open(output_path, "wb") as f:
                f.write(b"DEMO_MAKER_VIDEO_PLACEHOLDER")

            logger.info(f"Encoded video saved to: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Error encoding video: {str(e)}", exc_info=True)
            raise EncodingError(f"Failed to encode video: {str(e)}") from e

    def _finalize_video(self, video_path: Path, script: Dict[str, Any]) -> Path:
        """
        Finalize the video with any additional processing.

        Args:
            video_path: Path to the encoded video
            script: Dictionary containing the script with timing information

        Returns:
            Path to the finalized video

        Raises:
            VideoAssemblyError: If video finalization fails
        """
        try:
            # In a real implementation, this would add any final touches like
            # credits, titles, watermarks, etc.

            # For this placeholder implementation, return the original path
            logger.info("Video finalization complete")

            return video_path

        except Exception as e:
            logger.error(f"Error finalizing video: {str(e)}", exc_info=True)
            raise VideoAssemblyError(f"Failed to finalize video: {str(e)}") from e

    def _report_progress(self, percentage: int, message: str) -> None:
        """
        Report progress to the registered callback function.

        Args:
            percentage: Progress percentage (0-100)
            message: Status message
        """
        logger.info(f"Progress: {percentage}% - {message}")

        if self._progress_callback:
            try:
                self._progress_callback(percentage, message)
            except Exception as e:
                logger.warning(f"Error in progress callback: {str(e)}")
                # Continue even if callback fails
