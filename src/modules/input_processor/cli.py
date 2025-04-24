"""
Command-line Interface (CLI) for DemoMaker

This module implements the command-line interface for the DemoMaker
application using argparse. It provides commands for creating demos,
listing existing demos, retrieving info about specific demos, and
getting help.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from src.interfaces.input_processor import InputProcessorInterface

# Configure logging
logger = logging.getLogger(__name__)


class CommandLineProcessor(InputProcessorInterface):
    """Implementation of the InputProcessorInterface for command-line interactions."""

    SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif"]

    def __init__(self):
        """Initialize the CommandLineProcessor."""
        self.parser = self._create_argument_parser()

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser for the CLI.

        Returns:
            An argparse.ArgumentParser instance
        """
        # Create the main parser
        parser = argparse.ArgumentParser(
            prog="demomaker",
            description="DemoMaker - AI-powered Demo Video Generator",
            epilog="For more information, see the documentation.",
        )

        # Add subparsers for commands
        subparsers = parser.add_subparsers(
            title="commands", dest="command", help="Command to execute"
        )

        # Create command
        create_parser = subparsers.add_parser(
            "create", help="Create a new demo video from images and text"
        )
        create_parser.add_argument(
            "--images",
            "-i",
            required=True,
            help="Directory containing images or a list of image paths",
        )
        create_parser.add_argument(
            "--output",
            "-o",
            required=True,
            help="Output directory for the generated video",
        )
        create_parser.add_argument("--title", "-t", help="Title of the demo (optional)")
        create_parser.add_argument(
            "--description",
            "-d",
            required=True,
            help="Text description of the demo content",
        )
        create_parser.add_argument(
            "--duration", "-D", type=int, help="Target duration in seconds (optional)"
        )
        create_parser.add_argument(
            "--config", "-c", help="Path to a custom configuration file (optional)"
        )

        # List command
        list_parser = subparsers.add_parser(
            "list", help="List previously created demo videos"
        )

        # Info command
        info_parser = subparsers.add_parser(
            "info", help="Display information about a specific demo"
        )
        info_parser.add_argument(
            "demo_id", help="ID of the demo to get information about"
        )

        # Help command is automatically handled by argparse

        return parser

    def parse_args(self, args=None):
        """
        Parse command-line arguments.

        Args:
            args: List of arguments to parse (defaults to sys.argv[1:])

        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args(args)

    def validate_images(self, image_paths: Union[str, List[str]]) -> List[Path]:
        """
        Validate that the provided image paths exist and are of supported formats.

        Args:
            image_paths: A directory containing images or a list of image paths

        Returns:
            A list of validated image Path objects

        Raises:
            ValueError: If any image path is invalid or of an unsupported format
        """
        valid_images = []

        # Handle a directory of images
        if isinstance(image_paths, str):
            path = Path(image_paths)
            if path.is_dir():
                # Get all image files in the directory
                for format in self.SUPPORTED_IMAGE_FORMATS:
                    valid_images.extend(list(path.glob(f"*{format}")))

                if not valid_images:
                    raise ValueError(
                        f"No supported image files found in directory: {image_paths}"
                    )
            else:
                # Handle a single image path
                if not path.exists():
                    raise ValueError(f"Image file does not exist: {image_paths}")

                if path.suffix.lower() not in self.SUPPORTED_IMAGE_FORMATS:
                    raise ValueError(
                        f"Unsupported image format: {path.suffix}. "
                        f"Supported formats: {', '.join(self.SUPPORTED_IMAGE_FORMATS)}"
                    )
                valid_images.append(path)

        # Handle a list of image paths
        else:
            for img_path in image_paths:
                path = Path(img_path)
                if not path.exists():
                    raise ValueError(f"Image file does not exist: {img_path}")

                if path.suffix.lower() not in self.SUPPORTED_IMAGE_FORMATS:
                    raise ValueError(
                        f"Unsupported image format: {path.suffix}. "
                        f"Supported formats: {', '.join(self.SUPPORTED_IMAGE_FORMATS)}"
                    )
                valid_images.append(path)

        logger.info(f"Validated {len(valid_images)} image(s)")
        return valid_images

    def extract_image_metadata(self, image_paths: List[Path]) -> List[Dict[str, Any]]:
        """
        Extract metadata from the provided images.

        Args:
            image_paths: A list of validated image Path objects

        Returns:
            A list of dictionaries containing metadata for each image
            (resolution, aspect ratio, etc.)
        """
        # In a real implementation, we would use a library like PIL/Pillow to extract
        # actual metadata from images. For this implementation, we'll return basic info.
        metadata = []

        for path in image_paths:
            meta = {
                "path": str(path),
                "filename": path.name,
                "extension": path.suffix,
                "size_bytes": path.stat().st_size,
                # In a real implementation, we would extract resolution, aspect ratio, etc.
                "resolution": {"width": 0, "height": 0},
                "aspect_ratio": 0.0,
            }
            metadata.append(meta)

        logger.info(f"Extracted metadata from {len(metadata)} image(s)")
        return metadata

    def process_create_command(
        self,
        images: Union[str, List[str]],
        output: str,
        description: str,
        title: Optional[str] = None,
        duration: Optional[int] = None,
        config: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process the 'create' command inputs and prepare data for the pipeline.

        Args:
            images: Directory containing images or a list of image paths
            output: Output directory for the generated video
            description: Text description of the demo content
            title: Title of the demo (optional)
            duration: Target duration in seconds (optional)
            config: Path to a custom configuration file (optional)

        Returns:
            A dictionary containing all processed inputs ready for the pipeline

        Raises:
            ValueError: If any input is invalid
        """
        # Validate output directory
        output_path = Path(output)
        if not output_path.exists():
            logger.info(f"Creating output directory: {output_path}")
            output_path.mkdir(parents=True, exist_ok=True)
        elif not output_path.is_dir():
            raise ValueError(f"Output path exists but is not a directory: {output}")

        # Validate images
        valid_images = self.validate_images(images)

        # Extract image metadata
        image_metadata = self.extract_image_metadata(valid_images)

        # Validate config file if provided
        config_data = {}
        if config:
            config_path = Path(config)
            if not config_path.exists():
                raise ValueError(f"Configuration file does not exist: {config}")
            # In a real implementation, we would read and parse the config file
            logger.info(f"Using configuration file: {config_path}")

        # Prepare result
        result = {
            "images": valid_images,
            "image_metadata": image_metadata,
            "output_directory": output_path,
            "description": description,
            "title": title or "Untitled Demo",
            "duration": duration,
            "config": config_data,
        }

        logger.info(f"Processed create command with {len(valid_images)} images")
        return result

    def process_list_command(self) -> List[Dict[str, Any]]:
        """
        Process the 'list' command and retrieve all available demos.

        Returns:
            A list of dictionaries containing information about each demo
        """
        # In a real implementation, we would retrieve this information from storage
        # For now, return an empty list
        logger.info("Processed list command")
        return []

    def process_info_command(self, demo_id: str) -> Dict[str, Any]:
        """
        Process the 'info' command and retrieve information about a specific demo.

        Args:
            demo_id: The ID of the demo to get information about

        Returns:
            A dictionary containing detailed information about the demo

        Raises:
            ValueError: If the demo ID is invalid
        """
        # In a real implementation, we would retrieve this information from storage
        # For now, raise an error indicating the demo ID is not found
        logger.info(f"Processing info command for demo: {demo_id}")
        raise ValueError(f"Demo ID not found: {demo_id}")

    def get_help(self, command: Optional[str] = None) -> str:
        """
        Get help information for the CLI.

        Args:
            command: The specific command to get help for (optional)

        Returns:
            A string containing help information
        """
        # Use argparse's built-in help functionality
        import io

        f = io.StringIO()
        if command:
            # Get help for a specific command
            try:
                # Find the parser for the specified command
                if command == "create":
                    self.parser._actions[1].choices["create"].print_help(f)
                elif command == "list":
                    self.parser._actions[1].choices["list"].print_help(f)
                elif command == "info":
                    self.parser._actions[1].choices["info"].print_help(f)
                else:
                    f.write(f"Unknown command: {command}\n")
                    self.parser.print_help(f)
            except (KeyError, IndexError):
                self.parser.print_help(f)
        else:
            # Get general help
            self.parser.print_help(f)

        return f.getvalue()
