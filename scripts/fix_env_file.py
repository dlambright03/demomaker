#!/usr/bin/env python
"""
Utility script to fix encoding issues in .env file.
This script creates a backup of the original .env file and then creates a new
properly encoded version with the same content.
"""
import os
import sys
from pathlib import Path


def fix_env_file(env_path):
    """Fix encoding issues in .env file by reading it in binary mode and rewriting it correctly."""
    # First, check if the file exists
    if not os.path.exists(env_path):
        print(f"Error: {env_path} does not exist.")
        return False

    # Create a backup of the original file
    backup_path = f"{env_path}.bak"
    try:
        with open(env_path, "rb") as original:
            binary_content = original.read()

        with open(backup_path, "wb") as backup:
            backup.write(binary_content)

        print(f"Created backup of original .env file at {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

    # Try to create a new .env file with proper UTF-8 encoding
    try:
        # First, try to decode as UTF-8 with error handling
        try:
            content = binary_content.decode("utf-8", errors="replace")
        except UnicodeDecodeError:
            # If that fails, try Latin-1 which can decode any byte sequence
            content = binary_content.decode("latin-1")

        # Write the content back with proper UTF-8 encoding
        with open(env_path, "w", encoding="utf-8") as new_file:
            new_file.write(content)

        print(f"Successfully created new .env file with proper UTF-8 encoding")
        return True
    except Exception as e:
        print(f"Error fixing .env file: {e}")
        # Restore the backup if we failed
        try:
            with open(backup_path, "rb") as backup:
                with open(env_path, "wb") as original:
                    original.write(backup.read())
            print(f"Restored original .env file from backup")
        except Exception as restore_err:
            print(f"Error restoring backup: {restore_err}")
        return False


if __name__ == "__main__":
    # Get the repository root directory
    repo_root = Path(__file__).parent.parent
    env_path = repo_root / ".env"

    print(f"Fixing .env file at: {env_path}")
    success = fix_env_file(str(env_path))

    if success:
        print("✅ Fixed encoding issues in .env file")
        sys.exit(0)
    else:
        print("❌ Failed to fix encoding issues in .env file")
        sys.exit(1)
