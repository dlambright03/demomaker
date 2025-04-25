"""
Module Factory for DemoMaker application.

This factory is responsible for creating and connecting all the core modules
of the DemoMaker application, ensuring proper dependency injection and
maintaining loose coupling between components.
"""

import logging
from typing import Dict, Optional, Type

from src.interfaces.configuration import ConfigurationInterface
from src.interfaces.input_processor import InputProcessorInterface
from src.interfaces.narration_generator import NarrationGeneratorInterface
from src.interfaces.script_generator import ScriptGeneratorInterface
from src.interfaces.storage_manager import StorageManagerInterface
from src.interfaces.video_assembler import VideoAssemblerInterface
from src.modules.configuration.config_manager import Configuration
from src.modules.input_processor.cli import CommandLineProcessor
from src.modules.narration_generator.tts_generator import NarrationGenerator
from src.modules.script_generator.ai_script_generator import ScriptGenerator
from src.modules.storage_manager.file_storage_manager import FileStorageManager
from src.modules.video_assembler.video_assembler import VideoAssembler

logger = logging.getLogger(__name__)


class ModuleFactory:
    """
    Factory class for creating and connecting DemoMaker modules.

    This class is responsible for instantiating the core modules of the application
    and handling the dependencies between them. It follows the Factory pattern and
    supports dependency injection for testability.
    """

    def __init__(self):
        """Initialize the ModuleFactory with default implementations."""
        self._module_registry: Dict[Type, object] = {}
        self._module_overrides: Dict[Type, Type] = {}

        # Register default implementations
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register the default implementations for all modules."""
        logger.debug("Registering default module implementations")
        # No instances created yet, just mapping interfaces to implementations
        self._module_overrides[ConfigurationInterface] = Configuration
        self._module_overrides[InputProcessorInterface] = CommandLineProcessor
        self._module_overrides[ScriptGeneratorInterface] = ScriptGenerator
        self._module_overrides[NarrationGeneratorInterface] = NarrationGenerator
        self._module_overrides[StorageManagerInterface] = FileStorageManager
        self._module_overrides[VideoAssemblerInterface] = VideoAssembler

    def override_implementation(self, interface: Type, implementation: Type) -> None:
        """
        Override the default implementation of a module.

        Args:
            interface: The interface to override
            implementation: The implementation class to use
        """
        logger.debug(
            f"Overriding implementation for {interface.__name__} with {implementation.__name__}"
        )
        self._module_overrides[interface] = implementation

        # Clear any cached instance
        if interface in self._module_registry:
            del self._module_registry[interface]

    def create_configuration(self) -> ConfigurationInterface:
        """
        Create or return a cached Configuration module instance.

        Returns:
            A Configuration module instance
        """
        return self._get_or_create_module(ConfigurationInterface)

    def create_storage_manager(self) -> StorageManagerInterface:
        """
        Create or return a cached StorageManager module instance.

        Returns:
            A StorageManager module instance
        """
        config = self.create_configuration()
        return self._get_or_create_module(StorageManagerInterface, config=config)

    def create_input_processor(self) -> InputProcessorInterface:
        """
        Create or return a cached InputProcessor module instance.

        Returns:
            An InputProcessor module instance
        """
        config = self.create_configuration()
        storage = self.create_storage_manager()
        return self._get_or_create_module(
            InputProcessorInterface, config=config, storage_manager=storage
        )

    def create_script_generator(self) -> ScriptGeneratorInterface:
        """
        Create or return a cached ScriptGenerator module instance.

        Returns:
            A ScriptGenerator module instance
        """
        config = self.create_configuration()
        storage = self.create_storage_manager()
        return self._get_or_create_module(
            ScriptGeneratorInterface, config=config, storage_manager=storage
        )

    def create_narration_generator(self) -> NarrationGeneratorInterface:
        """
        Create or return a cached NarrationGenerator module instance.

        Returns:
            A NarrationGenerator module instance
        """
        config = self.create_configuration()
        storage = self.create_storage_manager()
        return self._get_or_create_module(
            NarrationGeneratorInterface, config=config, storage_manager=storage
        )

    def create_video_assembler(self) -> VideoAssemblerInterface:
        """
        Create or return a cached VideoAssembler module instance.

        Returns:
            A VideoAssembler module instance
        """
        config = self.create_configuration()
        storage = self.create_storage_manager()
        return self._get_or_create_module(
            VideoAssemblerInterface, config=config, storage_manager=storage
        )

    def _get_or_create_module(self, interface: Type, **kwargs) -> object:
        """
        Get a cached module instance or create a new one if it doesn't exist.

        Args:
            interface: The interface to get an implementation for
            **kwargs: Additional arguments to pass to the constructor

        Returns:
            A module instance

        Raises:
            KeyError: If no implementation is registered for the interface
        """
        if interface not in self._module_registry:
            if interface not in self._module_overrides:
                logger.error(f"No implementation registered for {interface.__name__}")
                raise KeyError(f"No implementation registered for {interface.__name__}")

            implementation_class = self._module_overrides[interface]
            logger.debug(f"Creating new instance of {implementation_class.__name__}")
            self._module_registry[interface] = implementation_class(**kwargs)

        return self._module_registry[interface]

    def clear_cache(self) -> None:
        """Clear all cached module instances."""
        logger.debug("Clearing module cache")
        self._module_registry.clear()


# Simple self-test code that runs when this module is executed directly
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("Testing ModuleFactory...")
    factory = ModuleFactory()

    print("Creating Configuration...")
    config = factory.create_configuration()
    print(f"Configuration type: {type(config).__name__}")

    print("Creating Storage Manager...")
    storage = factory.create_storage_manager()
    print(f"Storage Manager type: {type(storage).__name__}")

    print("All tests completed successfully")
