# DemoMaker

A Python-based application that leverages AI agents to automatically create and narrate professional demo videos.

## Disclaimer

This codebase was made as an experiment with using Github Copilot to completely plan and implement a project. It is not complete and not recommended to use.

## Project Overview

DemoMaker is a modular monolithic application designed to generate demo videos from user-provided images and text descriptions. It uses AI to generate scripts, creates audio narration through text-to-speech, and assembles everything into a polished demo video.

## Features

- **Environment-Based Configuration**: Supports development, testing, and production environments with appropriate configuration management
- **AI-Powered Script Generation**: Automatically creates narration scripts based on image content and user-provided descriptions
- **Text-to-Speech Narration**: Converts generated scripts into natural-sounding audio narration
- **Automatic Video Assembly**: Combines images and narration into a cohesive demo video
- **File-Based Storage System**: Manages project assets and output files
- **Command-Line Interface**: Easy-to-use CLI for batch processing and automation

## Directory Structure

```
demo_maker/
├── data/                 # Sample data and resources
├── docs/                 # Documentation
│   ├── adr/              # Architecture Decision Records
│   ├── conversations/    # Project discussions and meeting notes
│   ├── epics/            # Epic definitions
│   └── stories/          # User story definitions
├── scripts/              # Utility scripts
├── src/                  # Source code
│   ├── core/             # Core shared functionality
│   ├── config/           # Configuration management
│   ├── interfaces/       # Module interfaces
│   └── modules/          # Feature modules
│       ├── input_processor/     # Handles command-line inputs
│       ├── script_generator/    # AI-powered script generation
│       ├── narration_generator/ # Text-to-speech functionality
│       ├── video_assembler/     # Combines images and audio
│       └── storage_manager/     # File-based storage operations
└── tests/                # Test suite
    ├── unit/             # Unit tests
    ├── integration/      # Integration tests
    └── system/           # System tests
```

## Installation

### Prerequisites

- Docker Desktop installed on your machine
- Visual Studio Code with the following extensions:
  - [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (required for devcontainer support)
  - The devcontainer configuration will automatically install these extensions inside the container:
    - Python
    - Pylance
    - Black Formatter
    - Flake8
    - isort
    - mypy Type Checker

### Setup with DevContainer (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/your-username/demo_maker.git
   cd demo_maker
   ```

2. Open the project in Visual Studio Code:
   ```
   code .
   ```

3. When prompted, click "Reopen in Container" or use the command palette (F1) and select "Remote-Containers: Reopen in Container".

4. VS Code will build the development container with all dependencies pre-installed, including Python and FFmpeg.

5. The devcontainer will automatically create a `.env` file from the `sample.env` template if one doesn't exist yet.

### Alternative Setup (Manual)

If you prefer not to use DevContainers:

1. Ensure you have Python 3.10 or higher installed
2. Install FFmpeg (required for video processing)
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure your environment:
   ```
   cp sample.env .env
   ```
   Then edit the `.env` file to add your API keys and customize settings.

## Getting Started

DemoMaker provides a comprehensive command-line interface (CLI) for creating and managing demo videos. 

### Basic Usage

```bash
python -m src.main <command> [options]
```

### Available Commands

The DemoMaker CLI supports the following commands:

- `create`: Create a new demo video from images and text
- `list`: List all previously created demos
- `info`: Display detailed information about a specific demo
- `help`: Display help information

### Creating a Demo

To create a new demo video, use the `create` command with the following options:

```bash
python -m src.main create --images <path/to/images> --output <output/directory> --description "Your demo description" [options]
```

Required arguments:
- `--images` or `-i`: Directory containing images or a list of image paths
- `--output` or `-o`: Output directory for the generated video
- `--description` or `-d`: Text description of the demo content

Optional arguments:
- `--title` or `-t`: Title of the demo (defaults to "Untitled Demo")
- `--duration` or `-D`: Target duration in seconds
- `--config` or `-c`: Path to a custom configuration file

#### Examples

Create a demo using images from a directory:
```bash
python -m src.main create --images ./data/product_screenshots --output ./output --description "Product feature walkthrough"
```

Create a demo with a custom title and duration:
```bash
python -m src.main create --images ./data/product_screenshots --output ./output --description "Product feature walkthrough" --title "Product X Demo" --duration 120
```

### Listing Demos

To list all previously created demos:

```bash
python -m src.main list
```

### Getting Demo Information

To get detailed information about a specific demo:

```bash
python -m src.main info <demo_id>
```

### Getting Help

For general help:

```bash
python -m src.main --help
```

For command-specific help:

```bash
python -m src.main create --help
```

### Supported Image Formats

DemoMaker supports the following image formats:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)

## Environment Configuration

DemoMaker uses environment variables to configure various aspects of the application. These are stored in a `.env` file in the project root.

### Setting Up Your Environment

- **With DevContainer**: The devcontainer automatically creates a `.env` file from `sample.env` if one doesn't exist.
- **Manual Setup**: Copy `sample.env` to `.env` and edit it as needed: `cp sample.env .env`

### Key Configuration Values

The following environment variables are particularly important:

#### AI Service Configuration

- `OPENAI_API_KEY`: Required for script generation. Get your API key from [OpenAI](https://platform.openai.com/api-keys).
- `AZURE_OPENAI_API_KEY`: Alternative if using Azure OpenAI services.
- `HUGGINGFACE_TOKEN`: Required if using HuggingFace models for offline generation.

#### Text-to-Speech Configuration

- `TTS_SERVICE`: Choose your text-to-speech provider (`gtts`, `pyttsx3`, or `azure`).
- `TTS_VOICE`: Voice type to use for narration.
- `AZURE_SPEECH_KEY`: Required if using Azure Speech service for TTS.

#### Video Configuration

- `VIDEO_RESOLUTION`: Output video resolution (e.g., `1920x1080`).
- `VIDEO_FRAMERATE`: Frames per second (e.g., `30`).
- `VIDEO_FORMAT`: Output format (`mp4`, `mov`, etc.).

See `sample.env` for a complete list of available configuration options.

## Development

DemoMaker follows a modular monolithic architecture with clear interfaces between modules. This allows for independent development of modules while maintaining a single deployable unit.

### Module Development

Each module has a defined interface in the `src/interfaces` directory. Any implementation must adhere to these interfaces.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Status

All project tasks and their current status are tracked through GitHub issues. You can view the current project status and task details at:

- [GitHub Issues](https://github.com/dlambright03/demomaker/issues)
- [Project Board](https://github.com/users/dlambright03/projects/1)

## Configuration

DemoMaker uses a layered configuration system that supports multiple environments:

- **Environment Support**: Configure for development, testing, or production
- **Layered Configuration**: Default values, config files, environment variables, and command-line arguments
- **Validation**: Configuration values are validated against a JSON schema
- **Security**: Sensitive information is handled securely and masked when saving

For more details, see the [Configuration Documentation](docs/configuration.md).
