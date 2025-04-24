@echo off
rem Setup script for DemoMaker development environment on Windows

echo Setting up DemoMaker development environment...

rem Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    exit /b 1
)

rem Check if pip is installed
pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: pip is not installed or not in PATH
    echo Please ensure pip is installed with your Python installation
    exit /b 1
)

rem Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

rem Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

rem Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

rem Install development dependencies
echo Installing development dependencies...
pip install -r requirements-dev.txt

rem Check if ffmpeg is installed
where ffmpeg >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Warning: ffmpeg is not installed or not in PATH
    echo Please install ffmpeg from https://ffmpeg.org/download.html
    echo or using a package manager like Chocolatey: choco install ffmpeg
)

rem Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file with sample values...
    echo OPENAI_API_KEY=your_api_key_here > .env
    echo VIDEO_OUTPUT_DIR=./output >> .env
)

echo.
echo Setup complete! To activate the environment, run:
echo     call venv\Scripts\activate
echo.
echo To verify the setup, run:
echo     python scripts\verify_setup.py
echo.
