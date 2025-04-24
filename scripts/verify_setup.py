#!/usr/bin/env python
"""
Verification script for DemoMaker development environment.
This script checks that all required dependencies and tools are properly installed.
"""

import importlib
import shutil
import sys
import subprocess
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def check_python_version():
    """Check that Python version is 3.8 or higher."""
    major, minor = sys.version_info.major, sys.version_info.minor
    if major < 3 or (major == 3 and minor < 8):
        print(f"{RED}❌ Python version 3.8+ required, but {major}.{minor} found{RESET}")
        return False
    else:
        print(f"{GREEN}✓ Python version: {major}.{minor}{RESET}")
        return True

def check_package(package_name):
    """Check if a Python package is installed."""
    try:
        importlib.import_module(package_name)
        print(f"{GREEN}✓ Found package: {package_name}{RESET}")
        return True
    except ImportError:
        print(f"{RED}❌ Package not found: {package_name}{RESET}")
        return False

def check_command(command, error_message=None):
    """Check if a system command is available."""
    if shutil.which(command):
        try:
            if command == "ffmpeg":
                # Run ffmpeg -version and capture the first line of output
                result = subprocess.run([command, "-version"], capture_output=True, text=True)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    print(f"{GREEN}✓ Found {command}: {version_line}{RESET}")
                else:
                    print(f"{GREEN}✓ Found {command}{RESET}")
            else:
                print(f"{GREEN}✓ Found {command}{RESET}")
            return True
        except Exception as e:
            print(f"{YELLOW}⚠ {command} found but execution failed: {e}{RESET}")
            return False
    else:
        if error_message:
            print(f"{RED}❌ {error_message}{RESET}")
        else:
            print(f"{RED}❌ Command not found: {command}{RESET}")
        return False

def check_env_file():
    """Check if .env file exists."""
    if Path('.env').exists():
        print(f"{GREEN}✓ Found .env file{RESET}")
        return True
    else:
        print(f"{RED}❌ .env file not found{RESET}")
        return False

def main():
    """Run all verification checks."""
    print("\n=== DemoMaker Environment Verification ===\n")
    
    all_checks_passed = True
    
    print("Checking Python installation...")
    all_checks_passed &= check_python_version()
    
    print("\nChecking core dependencies...")
    core_packages = ['dotenv', 'pydantic', 'click', 'tqdm', 'openai', 'semantic_kernel', 'transformers']
    for package in core_packages:
        all_checks_passed &= check_package(package)
    
    print("\nChecking media processing libraries...")
    media_packages = ['gtts', 'pyttsx3', 'moviepy', 'PIL']
    for package in media_packages:
        all_checks_passed &= check_package(package)
    
    print("\nChecking system dependencies...")
    all_checks_passed &= check_command('ffmpeg', "ffmpeg not found. Please install ffmpeg to enable video processing")
    
    print("\nChecking configuration...")
    all_checks_passed &= check_env_file()
    
    print("\n=== Verification Summary ===\n")
    if all_checks_passed:
        print(f"{GREEN}✓ All checks passed! Your environment is ready for development.{RESET}")
    else:
        print(f"{YELLOW}⚠ Some checks failed. Please fix the issues above before proceeding.{RESET}")
        print(f"{YELLOW}  See the documentation at docs/setup.md for troubleshooting tips.{RESET}")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
