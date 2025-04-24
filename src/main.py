#!/usr/bin/env python3
"""
DemoMaker - Main entry point

This is the main entry point for the DemoMaker application.
It parses command-line arguments and orchestrates the workflow
through the different modules.
"""
import argparse
import logging
import sys
from pathlib import Path

from src.modules.input_processor import CommandLineProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for the DemoMaker application.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    try:
        cli_processor = CommandLineProcessor()
        args = cli_processor.parse_args()

        if not args.command:
            # No command specified, show help
            print(cli_processor.get_help())
            return 0

        # Process the specified command
        if args.command == "create":
            result = cli_processor.process_create_command(
                images=args.images,
                output=args.output,
                description=args.description,
                title=args.title,
                duration=args.duration,
                config=args.config,
            )
            print(f"✅ Demo creation initiated: {result['title']}")
            print(f"🖼️  Processing {len(result['images'])} images")
            print(f"📁 Output will be saved to: {result['output_directory']}")
            # In a real implementation, we would pass the result to the next module in the pipeline

        elif args.command == "list":
            demos = cli_processor.process_list_command()
            if demos:
                print(f"📋 Found {len(demos)} demos:")
                for i, demo in enumerate(demos, 1):
                    print(
                        f"{i}. {demo.get('title', 'Untitled')} (ID: {demo.get('id', 'unknown')})"
                    )
            else:
                print("📋 No demos found")

        elif args.command == "info":
            try:
                demo_info = cli_processor.process_info_command(args.demo_id)
                print(f"ℹ️ Demo Information: {demo_info.get('title', 'Untitled')}")
                for key, value in demo_info.items():
                    if key != "title":
                        print(f"  {key}: {value}")
            except ValueError as e:
                print(f"❌ Error: {str(e)}")
                return 1

        return 0

    except ValueError as e:
        print(f"❌ Error: {str(e)}")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        print(f"❌ An unexpected error occurred: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
