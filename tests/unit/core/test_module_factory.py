"""
Tests for the Module Factory component.

These tests verify that the Module Factory correctly creates and connects
all the core modules of the DemoMaker application.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.core.module_factory import ModuleFactory
from src.interfaces.configuration import ConfigurationInterface
from src.interfaces.input_processor import InputProcessorInterface
from src.interfaces.narration_generator import NarrationGeneratorInterface
from src.interfaces.script_generator import ScriptGeneratorInterface
from src.interfaces.storage_manager import StorageManagerInterface
from src.interfaces.video_assembler import VideoAssemblerInterface


class TestModuleFactory(unittest.TestCase):
    """Test cases for the ModuleFactory class."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = ModuleFactory()

    def test_create_configuration(self):
        """Test creating a Configuration module."""
        config = self.factory.create_configuration()
        self.assertIsNotNone(config)
        self.assertIsInstance(config, ConfigurationInterface)

    def test_create_storage_manager(self):
        """Test creating a StorageManager module."""
        storage = self.factory.create_storage_manager()
        self.assertIsNotNone(storage)
        self.assertIsInstance(storage, StorageManagerInterface)

    def test_create_input_processor(self):
        """Test creating an InputProcessor module."""
        processor = self.factory.create_input_processor()
        self.assertIsNotNone(processor)
        self.assertIsInstance(processor, InputProcessorInterface)

    def test_create_script_generator(self):
        """Test creating a ScriptGenerator module."""
        generator = self.factory.create_script_generator()
        self.assertIsNotNone(generator)
        self.assertIsInstance(generator, ScriptGeneratorInterface)

    def test_create_narration_generator(self):
        """Test creating a NarrationGenerator module."""
        generator = self.factory.create_narration_generator()
        self.assertIsNotNone(generator)
        self.assertIsInstance(generator, NarrationGeneratorInterface)

    def test_create_video_assembler(self):
        """Test creating a VideoAssembler module."""
        assembler = self.factory.create_video_assembler()
        self.assertIsNotNone(assembler)
        self.assertIsInstance(assembler, VideoAssemblerInterface)

    def test_module_caching(self):
        """Test that modules are cached and reused."""
        config1 = self.factory.create_configuration()
        config2 = self.factory.create_configuration()
        self.assertIs(config1, config2, "Factory should cache module instances")

    def test_clear_cache(self):
        """Test clearing the module cache."""
        config1 = self.factory.create_configuration()
        self.factory.clear_cache()
        config2 = self.factory.create_configuration()
        self.assertIsNot(
            config1, config2, "Factory should create new instances after clearing cache"
        )

    def test_override_implementation(self):
        """Test overriding a module implementation."""
        # Create a mock implementation
        mock_config_class = MagicMock()
        mock_config = MagicMock(spec=ConfigurationInterface)
        mock_config_class.return_value = mock_config

        # Override the implementation
        self.factory.override_implementation(ConfigurationInterface, mock_config_class)

        # Get the module
        config = self.factory.create_configuration()

        # Verify it's our mock
        self.assertIs(config, mock_config)
        mock_config_class.assert_called_once()

    def test_dependency_injection(self):
        """Test that dependencies are properly injected."""
        with patch(
            "src.modules.script_generator.ai_script_generator.ScriptGenerator"
        ) as mock_script_generator:
            # Create a mock
            mock_instance = MagicMock(spec=ScriptGeneratorInterface)
            mock_script_generator.return_value = mock_instance

            # Override the implementation
            self.factory.override_implementation(
                ScriptGeneratorInterface, mock_script_generator
            )

            # Get the module
            script_gen = self.factory.create_script_generator()

            # Verify dependencies were passed
            mock_script_generator.assert_called_once()
            args = mock_script_generator.call_args[1]

            # Check that dependencies were passed
            self.assertIn("config", args)
            self.assertIn("storage_manager", args)
            self.assertIsInstance(args["config"], ConfigurationInterface)
            self.assertIsInstance(args["storage_manager"], StorageManagerInterface)


if __name__ == "__main__":
    unittest.main()
