# DemoMaker Development Environment Setup

This document provides instructions for setting up the development environment for the DemoMaker application.

## Setup with DevContainers (Recommended)

DevContainers provide a consistent, reproducible development environment across different machines. This is the recommended approach for DemoMaker development.

### Prerequisites for DevContainer Setup

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your machine
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) for VS Code

### DevContainer Setup Instructions

1. Clone the repository:
   ```
   git clone [repository-url]
   cd demo_maker
   ```

2. Open the project in Visual Studio Code:
   ```
   code .
   ```

3. VS Code will detect the devcontainer configuration and prompt you to "Reopen in Container". Click on this prompt.
   - Alternatively, press `F1`, type "Remote-Containers: Reopen in Container", and select it.

4. VS Code will build the development container with all required dependencies and tools pre-installed:
   - Python 3.11
   - FFmpeg
   - All Python packages from requirements.txt
   - Development tools (black, isort, flake8, mypy)

5. The container setup may take a few minutes the first time. Once complete, you'll have a fully configured development environment.

6. Verify the setup by running the verification script from the VS Code terminal:
   ```
   python scripts/verify_setup.py
   ```

## Alternative Setup (Manual Virtual Environment)

If you prefer not to use DevContainers or are unable to install Docker, you can use the traditional virtual environment approach.

### Prerequisites for Manual Setup

- Python 3.8 or higher
- pip (Python package manager)
- Git
- FFmpeg (required for video processing)

## Environment Variables

The setup scripts create a `.env` file with sample values. Update this file with your actual values:

```
OPENAI_API_KEY=your_api_key_here
VIDEO_OUTPUT_DIR=./output
```

## System Dependencies

### FFmpeg Installation

FFmpeg is required for video processing. If the setup script indicates FFmpeg is not installed, follow these instructions:

#### Windows
- Using Chocolatey: `choco install ffmpeg`
- Manual download: [FFmpeg Windows Builds](https://ffmpeg.org/download.html#build-windows)

#### macOS
- Using Homebrew: `brew install ffmpeg`

#### Linux (Ubuntu/Debian)
- Using apt: `sudo apt install ffmpeg`

## Development Tools

The development environment includes the following tools:

- **pytest**: For running tests
- **black**: Code formatter
- **isort**: Import sorter
- **mypy**: Type checker
- **flake8**: Linter

## Troubleshooting

### Common Issues

#### "Python not found" or "pip not found"
- Ensure Python is installed and added to your system PATH

#### "FFmpeg not found"
- Install FFmpeg using the instructions above
- Ensure FFmpeg is added to your system PATH

#### Package installation failures
- Try updating pip: `python -m pip install --upgrade pip`
- If behind a proxy, configure pip to use the proxy

#### Virtual environment issues
- If you encounter errors with the virtual environment, try removing the `venv` directory and running the setup script again

## Hardware Requirements

- **CPU**: Minimum 4 cores recommended
- **RAM**: Minimum 8GB, 16GB recommended for running AI models
- **Disk Space**: At least 5GB for development environment and dependencies

## IDE Configuration

### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort
- Flake8

Settings (add to .vscode/settings.json):
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## Updating Dependencies

When new dependencies are added:

1. Update the relevant requirements file
2. Run `pip install -r requirements-dev.txt` to install the new dependencies

## Verification

To verify that your environment is set up correctly:

```
python scripts/verify_setup.py
```

This script checks for required packages, system dependencies, and proper configuration.
