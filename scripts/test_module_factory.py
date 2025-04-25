"""
Test script to verify the Module Factory functionality.
This is a simple script that creates and uses a ModuleFactory instance.
"""

import logging

from src.core.module_factory import ModuleFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main function to test the ModuleFactory."""
    logger.info("Creating Module Factory")
    factory = ModuleFactory()

    logger.info("Creating Configuration")
    config = factory.create_configuration()
    logger.info(f"Configuration type: {type(config).__name__}")

    logger.info("Creating Storage Manager")
    storage = factory.create_storage_manager()
    logger.info(f"Storage Manager type: {type(storage).__name__}")

    logger.info("Creating Input Processor")
    input_processor = factory.create_input_processor()
    logger.info(f"Input Processor type: {type(input_processor).__name__}")

    logger.info("Creating Script Generator")
    script_generator = factory.create_script_generator()
    logger.info(f"Script Generator type: {type(script_generator).__name__}")

    logger.info("Creating Narration Generator")
    narration_generator = factory.create_narration_generator()
    logger.info(f"Narration Generator type: {type(narration_generator).__name__}")

    logger.info("Creating Video Assembler")
    video_assembler = factory.create_video_assembler()
    logger.info(f"Video Assembler type: {type(video_assembler).__name__}")

    logger.info("All modules created successfully")

    # Test caching
    logger.info("Testing module caching")
    config2 = factory.create_configuration()
    if config is config2:
        logger.info("Module caching is working")
    else:
        logger.error("Module caching is NOT working")

    # Test cache clearing
    logger.info("Testing cache clearing")
    factory.clear_cache()
    config3 = factory.create_configuration()
    if config is not config3:
        logger.info("Cache clearing is working")
    else:
        logger.error("Cache clearing is NOT working")


if __name__ == "__main__":
    main()
