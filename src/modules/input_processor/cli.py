"""
Command Line Processor

This module provides the CommandLineProcessor class, which is responsible
for handling command-line arguments and validating user inputs for the
DemoMaker application.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

from src.interfaces.input_processor import InputProcessorInterface

# Supported image formats
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif"]

# Configure module logger
logger = logging.getLogger(__name__)


class CommandLineProcessor(InputProcessorInterface):
    """
    Handles command-line arguments and input validation for the DemoMaker application.
    """

    def __init__(self):
        """Initialize the command-line processor."""
        self.parser = self._create_argument_parser()

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser with all supported commands and arguments.

        Returns:
            argparse.ArgumentParser: The configured argument parser.
        """
        # Create the main parser
        parser = argparse.ArgumentParser(
            prog="demomaker",
            description="DemoMaker - Create professional demo videos from images and text",
            epilog="For more information, visit: https://github.com/dlambright03/demomaker",
        )

        # Create subparsers for commands
        subparsers = parser.add_subparsers(
            dest="command",
            title="commands",
            description="valid commands",
            help="specify the command to execute",
        )

        # Create command parser
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

        # List command parser
        list_parser = subparsers.add_parser(
            "list", help="List previously created demo videos"
        )

        # Info command parser
        info_parser = subparsers.add_parser(
            "info", help="Display information about a specific demo"
        )
        info_parser.add_argument(
            "demo_id", help="ID of the demo to get information about"
        )

        return parser

    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """
        Parse command-line arguments.

        Args:
            args: Command-line arguments to parse. If None, sys.argv is used.

        Returns:
            argparse.Namespace: The parsed arguments.
        """
        parsed_args = self.parser.parse_args(args)
        logger.debug(f"Parsed arguments: {parsed_args}")
        return parsed_args

    def get_help(self) -> str:
        """
        Get help information for the command-line interface.

        Returns:
            str: The help text.
        """
        # Capture help output in a string
        import io

        help_io = io.StringIO()
        self.parser.print_help(file=help_io)
        return help_io.getvalue()

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
        logger.info(f"Processing create command with images={images}, output={output}")

        # Validate inputs
        validated_images = self.validate_images(images)
        output_dir = self.validate_output_directory(output)

        # Validate description
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")

        # Load config if provided
        config_data = {}
        if config:
            config_data = self.load_config(config)

        # Generate title if not provided
        if not title:
            # Use first 5 words of description or first 50 chars, whichever is shorter
            title_from_desc = " ".join(description.split()[:5])
            title = title_from_desc[:50] + ("..." if len(title_from_desc) > 50 else "")

        # Collect metadata from images
        image_metadata = self._extract_image_metadata(validated_images)

        # Create a unique ID for this demo
        import time
        import uuid

        demo_id = f"demo_{int(time.time())}_{uuid.uuid4().hex[:8]}"

        result = {
            "id": demo_id,
            "title": title,
            "description": description,
            "images": [str(img) for img in validated_images],
            "image_metadata": image_metadata,
            "output_directory": str(output_dir),
            "duration": duration,
            "config": config_data,
            "timestamp": int(time.time()),
        }

        # Save result as a demo project file
        self._save_demo_project(result, output_dir)

        return result

    def process_list_command(self) -> List[Dict]:
        """
        Process the 'list' command.

        Returns:
            List[Dict]: A list of dictionaries containing information about existing demos.
        """
        # This is a placeholder implementation
        # In a real implementation, we would scan for demo project files
        # For now, we'll return a mock list
        logger.info("Processing list command")

        # Mock data for demonstration purposes
        return [
            {"id": "demo_12345", "title": "Sample Demo 1", "timestamp": 1619654400},
            {"id": "demo_67890", "title": "Sample Demo 2", "timestamp": 1619740800},
        ]

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
        logger.info(f"Processing info command for demo_id={demo_id}")

        # Validate demo ID
        if not demo_id or not demo_id.strip():
            raise ValueError("Demo ID cannot be empty")

        # This is a placeholder implementation
        # In a real implementation, we would look up the demo project file
        # For now, we'll return mock data
        if demo_id == "demo_12345":
            return {
                "id": "demo_12345",
                "title": "Sample Demo 1",
                "description": "This is a sample demo",
                "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],
                "output_directory": "/path/to/output",
                "timestamp": 1619654400,
                "status": "completed",
            }
        elif demo_id == "demo_67890":
            return {
                "id": "demo_67890",
                "title": "Sample Demo 2",
                "description": "This is another sample demo",
                "images": ["/path/to/image3.jpg", "/path/to/image4.jpg"],
                "output_directory": "/path/to/output",
                "timestamp": 1619740800,
                "status": "in_progress",
            }
        else:
            raise ValueError(f"Demo with ID {demo_id} not found")

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
        validated_images = []

        # Handle string input (single path or directory)
        if isinstance(images, str):
            path = Path(images)

            # Check if it's a directory
            if path.is_dir():
                # Collect all supported image files in the directory
                for ext in SUPPORTED_IMAGE_FORMATS:
                    validated_images.extend(list(path.glob(f"*{ext}")))

                if not validated_images:
                    raise ValueError(f"No supported images found in directory: {path}")

            # Check if it's a comma-separated list of paths
            elif "," in images:
                image_list = [p.strip() for p in images.split(",")]
                return self.validate_images(image_list)

            # Check if it's a single file
            elif path.is_file():
                if path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
                    raise ValueError(
                        f"Unsupported image format: {path.suffix}. "
                        f"Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
                    )
                validated_images.append(path)

            else:
                raise ValueError(f"Image path not found: {path}")

        # Handle list input
        elif isinstance(images, list):
            for img_path in images:
                path = Path(img_path)

                if not path.is_file():
                    raise ValueError(f"Image file not found: {path}")

                if path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
                    raise ValueError(
                        f"Unsupported image format: {path.suffix}. "
                        f"Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
                    )

                validated_images.append(path)

        else:
            raise ValueError("Images must be a string path or a list of paths")

        # Sort images by name for consistent ordering
        validated_images.sort()

        logger.info(f"Validated {len(validated_images)} images")
        return validated_images

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
        if not output or not output.strip():
            raise ValueError("Output directory path cannot be empty")

        output_path = Path(output)

        # Create directory if it doesn't exist
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise ValueError(
                f"Permission denied when creating output directory: {output_path}"
            )
        except OSError as e:
            raise ValueError(f"Error creating output directory: {e}")

        # Check if the directory is writable
        if not os.access(output_path, os.W_OK):
            raise ValueError(f"Output directory is not writable: {output_path}")

        logger.info(f"Validated output directory: {output_path}")
        return output_path

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
        if not config_path or not config_path.strip():
            raise ValueError("Configuration file path cannot be empty")

        config_file = Path(config_path)

        if not config_file.is_file():
            raise ValueError(f"Configuration file not found: {config_file}")

        # Check file extension and load accordingly
        if config_file.suffix.lower() == ".json":
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    logger.info(f"Loaded JSON configuration from {config_file}")
                    return config
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in configuration file: {e}")
            except Exception as e:
                raise ValueError(f"Error loading configuration file: {e}")
        else:
            raise ValueError(
                f"Unsupported configuration file format: {config_file.suffix}"
            )

    def _extract_image_metadata(self, images: List[Path]) -> List[Dict]:
        """
        Extract metadata from images.

        Args:
            images: List of validated image paths.

        Returns:
            List[Dict]: A list of dictionaries containing metadata for each image.
        """
        metadata = []

        for img_path in images:
            # Basic metadata that doesn't require additional libraries
            meta = {
                "path": str(img_path),
                "filename": img_path.name,
                "size_bytes": img_path.stat().st_size,
                "format": img_path.suffix.lower().lstrip("."),
            }

            # In a full implementation, we would use a library like Pillow to extract:
            # - Image dimensions (width, height)
            # - Color mode
            # - EXIF data
            # For now, we'll use placeholder values
            meta.update(
                {
                    "width": 1920,
                    "height": 1080,
                    "aspect_ratio": "16:9",
                    "color_mode": "RGB",
                }
            )

            metadata.append(meta)

        return metadata

    def _save_demo_project(self, project_data: Dict, output_dir: Path) -> None:
        """
        Save demo project data to a file.

        Args:
            project_data: The project data to save.
            output_dir: The output directory.

        Raises:
            ValueError: If the project data cannot be saved.
        """
        # This is a placeholder implementation
        # In a real implementation, we would save to a database or file
        project_file = output_dir / f"{project_data['id']}.json"

        try:
            with open(project_file, "w") as f:
                json.dump(project_data, f, indent=2)
            logger.info(f"Saved demo project to {project_file}")
        except Exception as e:
            logger.error(f"Error saving demo project: {e}")
            raise ValueError(f"Failed to save demo project: {e}")
