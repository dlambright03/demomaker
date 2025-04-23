"""
Interface for the Video Assembler Module.

This module is responsible for combining user-provided images and generated
narration into a cohesive video using FFMPEG.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any


class VideoAssemblerInterface(ABC):
    """Interface for the Video Assembler Module."""
    
    @abstractmethod
    def assemble_video(self, 
                      images: List[Path], 
                      narration_audio: Path, 
                      script: Dict[str, Any],
                      output_path: Path,
                      title: Optional[str] = None) -> Path:
        """
        Assemble a video from images and narration audio.
        
        Args:
            images: List of validated image Path objects
            narration_audio: Path to the narration audio file
            script: Dictionary containing the structured script with timing information
            output_path: Path to save the output video
            title: Title to include in the title frame (optional)
            
        Returns:
            Path to the assembled video
            
        Raises:
            VideoAssemblyError: If video assembly fails
        """
        pass
    
    @abstractmethod
    def set_output_format(self, format_name: str) -> None:
        """
        Set the output video format.
        
        Args:
            format_name: Name of the format (e.g., 'mp4', 'webm')
            
        Raises:
            ValueError: If the format is invalid or unsupported
        """
        pass
    
    @abstractmethod
    def set_output_resolution(self, width: int, height: int) -> None:
        """
        Set the output video resolution.
        
        Args:
            width: Video width in pixels
            height: Video height in pixels
            
        Raises:
            ValueError: If the resolution is invalid or unsupported
        """
        pass
    
    @abstractmethod
    def set_transition_style(self, style: str) -> None:
        """
        Set the transition style between images.
        
        Args:
            style: Name of the transition style (e.g., 'fade', 'dissolve', 'slide')
            
        Raises:
            ValueError: If the transition style is invalid or unsupported
        """
        pass
    
    @abstractmethod
    def set_transition_duration(self, duration: float) -> None:
        """
        Set the duration of transitions between images.
        
        Args:
            duration: Duration in seconds
            
        Raises:
            ValueError: If the duration is outside the valid range
        """
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        Get a list of supported output video formats.
        
        Returns:
            A list of supported format names
        """
        pass
    
    @abstractmethod
    def get_supported_transitions(self) -> List[str]:
        """
        Get a list of supported transition styles.
        
        Returns:
            A list of supported transition style names
        """
        pass
    
    @abstractmethod
    def estimate_assembly_time(self, 
                             num_images: int, 
                             video_duration: int) -> int:
        """
        Estimate the time required to assemble a video.
        
        Args:
            num_images: Number of images in the input
            video_duration: Duration of the video in seconds
            
        Returns:
            Estimated time in seconds
        """
        pass
    
    @abstractmethod
    def cancel_assembly(self) -> bool:
        """
        Cancel an ongoing video assembly process.
        
        Returns:
            True if cancellation was successful, False otherwise
        """
        pass
