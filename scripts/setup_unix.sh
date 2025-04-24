#!/bin/bash
# Setup script for DemoMaker development environment on Unix-based systems

echo "Setting up DemoMaker development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher from your package manager or https://www.python.org/downloads/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed or not in PATH"
    echo "Please ensure pip is installed with your Python installation"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: ffmpeg is not installed or not in PATH"
    echo "Please install ffmpeg from your package manager:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file with sample values..."
    echo "OPENAI_API_KEY=your_api_key_here" > .env
    echo "VIDEO_OUTPUT_DIR=./output" >> .env
fi

echo ""
echo "Setup complete! To activate the environment, run:"
echo "    source venv/bin/activate"
echo ""
echo "To verify the setup, run:"
echo "    python scripts/verify_setup.py"
echo ""
