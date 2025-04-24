# DemoMaker

A Python-based application that leverages AI agents to automatically create and narrate professional demo videos.

## Project Overview

DemoMaker is a modular monolithic application designed to generate demo videos from user-provided images and text descriptions. It uses AI to generate scripts, creates audio narration through text-to-speech, and assembles everything into a polished demo video.

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

After installation, you can create a simple demo by running:

```
python -m src.main --images path/to/images --description "A brief description of your demo"
```

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
