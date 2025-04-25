"""
Test script to verify the Module Factory functionality with error handling.
This script will catch and display any exceptions that occur.
"""

import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main function to test the ModuleFactory with error handling."""
    logger.info("Testing Module Factory")

    try:
        logger.info("Importing ModuleFactory")
        from src.core.module_factory import ModuleFactory

        logger.info("Creating Module Factory")
        factory = ModuleFactory()

        try:
            logger.info("Creating Configuration")
            config = factory.create_configuration()
            logger.info(f"Configuration type: {type(config).__name__}")
        except Exception as e:
            logger.error(f"Error creating Configuration: {str(e)}")
            logger.error(traceback.format_exc())

        try:
            logger.info("Creating Storage Manager")
            storage = factory.create_storage_manager()
            logger.info(f"Storage Manager type: {type(storage).__name__}")
        except Exception as e:
            logger.error(f"Error creating Storage Manager: {str(e)}")
            logger.error(traceback.format_exc())

        try:
            logger.info("Creating Input Processor")
            input_processor = factory.create_input_processor()
            logger.info(f"Input Processor type: {type(input_processor).__name__}")
        except Exception as e:
            logger.error(f"Error creating Input Processor: {str(e)}")
            logger.error(traceback.format_exc())

    except Exception as e:
        logger.error(f"Error initializing Module Factory: {str(e)}")
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
