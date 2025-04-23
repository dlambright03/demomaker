"""
Interface for the Narration Generator Module.

This module is responsible for converting generated scripts into
audio narration using text-to-speech (TTS) services.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any


class NarrationGeneratorInterface(ABC):
    """Interface for the Narration Generator Module."""
    
    @abstractmethod
    def generate_narration(self, script: Dict[str, Any], output_dir: Path) -> Path:
        """
        Generate audio narration from a script.
        
        Args:
            script: Dictionary containing the structured script with timing information
            output_dir: Directory to save the generated audio files
            
        Returns:
            Path to the generated audio file
            
        Raises:
            NarrationGenerationError: If narration generation fails
        """
        pass
    
    @abstractmethod
    def set_voice(self, voice_id: str) -> None:
        """
        Set the voice to use for narration.
        
        Args:
            voice_id: The ID of the voice to use
            
        Raises:
            ValueError: If the voice ID is invalid or unavailable
        """
        pass
    
    @abstractmethod
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get a list of available voices for narration.
        
        Returns:
            A list of dictionaries containing information about each voice
            (id, name, gender, language, etc.)
        """
        pass
    
    @abstractmethod
    def set_speech_rate(self, rate: float) -> None:
        """
        Set the speech rate for narration.
        
        Args:
            rate: Speech rate multiplier (1.0 is normal speed)
            
        Raises:
            ValueError: If the rate is outside the valid range
        """
        pass
    
    @abstractmethod
    def set_speech_pitch(self, pitch: float) -> None:
        """
        Set the speech pitch for narration.
        
        Args:
            pitch: Speech pitch multiplier (1.0 is normal pitch)
            
        Raises:
            ValueError: If the pitch is outside the valid range
        """
        pass
    
    @abstractmethod
    def estimate_narration_time(self, script: Dict[str, Any]) -> int:
        """
        Estimate the time required to generate narration.
        
        Args:
            script: Dictionary containing the structured script
            
        Returns:
            Estimated time in seconds
        """
        pass
    
    @abstractmethod
    def cancel_generation(self) -> bool:
        """
        Cancel an ongoing narration generation process.
        
        Returns:
            True if cancellation was successful, False otherwise
        """
        pass
