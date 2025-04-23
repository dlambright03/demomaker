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

- Python 3.10 or higher
- FFmpeg (for video processing)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/demo_maker.git
   cd demo_maker
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Getting Started

After installation, you can create a simple demo by running:

```
python -m src.main --images path/to/images --description "A brief description of your demo"
```

## Development

DemoMaker follows a modular monolithic architecture with clear interfaces between modules. This allows for independent development of modules while maintaining a single deployable unit.

### Module Development

Each module has a defined interface in the `src/interfaces` directory. Any implementation must adhere to these interfaces.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
