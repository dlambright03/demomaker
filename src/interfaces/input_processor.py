"""
Input Processor Interface

This module defines the interface for the input processing components
of the DemoMaker application, including command-line argument handling
and input validation.
"""
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict, List, Optional, Union


class InputProcessorInterface(ABC):
    """
    Interface for input processing components that handle user inputs,
    including command-line arguments and configuration files.
    """

    @abstractmethod
    def parse_args(self, args: Optional[List[str]] = None) -> Namespace:
        """
        Parse command-line arguments.

        Args:
            args: Command-line arguments to parse. If None, sys.argv is used.

        Returns:
            Namespace: The parsed arguments.
        """
        pass

    @abstractmethod
    def get_help(self) -> str:
        """
        Get help information for the command-line interface.

        Returns:
            str: The help text.
        """
        pass

    @abstractmethod
    def process_create_command(
        self,
        images: Union[str, List[str]],
        output: str,
        description: str,
        title: Optional[str] = None,
        duration: Optional[int] = None,
        config: Optional[str] = None,
    ) -> Dict:
        """
        Process the 'create' command.

        Args:
            images: Path to image directory or list of image paths.
            output: Output directory path.
            description: Text description of the demo content.
            title: Title of the demo (optional).
            duration: Target duration in seconds (optional).
            config: Path to a custom configuration file (optional).

        Returns:
            Dict: A dictionary containing the processed inputs.

        Raises:
            ValueError: If any input is invalid.
        """
        pass

    @abstractmethod
    def process_list_command(self) -> List[Dict]:
        """
        Process the 'list' command.

        Returns:
            List[Dict]: A list of dictionaries containing information about existing demos.
        """
        pass

    @abstractmethod
    def process_info_command(self, demo_id: str) -> Dict:
        """
        Process the 'info' command.

        Args:
            demo_id: The ID of the demo to get information about.

        Returns:
            Dict: A dictionary containing information about the specified demo.

        Raises:
            ValueError: If the demo ID is invalid or not found.
        """
        pass

    @abstractmethod
    def validate_images(self, images: Union[str, List[str]]) -> List[Path]:
        """
        Validate image paths and formats.

        Args:
            images: Path to image directory or list of image paths.

        Returns:
            List[Path]: A list of validated image paths.

        Raises:
            ValueError: If any image path is invalid or the image format is not supported.
        """
        pass

    @abstractmethod
    def validate_output_directory(self, output: str) -> Path:
        """
        Validate and create the output directory if it doesn't exist.

        Args:
            output: Output directory path.

        Returns:
            Path: The validated output directory path.

        Raises:
            ValueError: If the output directory path is invalid.
        """
        pass

    @abstractmethod
    def load_config(self, config_path: str) -> Dict:
        """
        Load and validate a configuration file.

        Args:
            config_path: Path to the configuration file.

        Returns:
            Dict: The loaded configuration.

        Raises:
            ValueError: If the configuration file is invalid or cannot be loaded.
        """
        pass
