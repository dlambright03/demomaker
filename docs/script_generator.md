# Script Generator Module

## Overview

The Script Generator module is a key component of the DemoMaker system that automatically generates coherent and engaging scripts based on provided images and descriptions. It leverages AI models to analyze image content, create narrative text, and provide timing information for video assembly.

## Features

- **AI-Powered Image Analysis**: Automatically analyzes images to detect objects, text, colors, and composition
- **Narrative Generation**: Creates coherent narratives that tie together multiple images
- **Timing Information**: Provides timing details for segment duration and transitions
- **Multiple AI Models**: Supports various AI models including GPT-3.5, GPT-4, and Claude
- **Local Fallback**: Includes a local mock implementation for development and testing

## Architecture

The Script Generator module follows a modular architecture:

- **ScriptGeneratorInterface**: Defines the interface for all script generators
- **ScriptGenerator**: Primary implementation that handles script generation
- **AI Providers**: Pluggable AI providers for different models and services
  - BaseAIProvider: Base class for all AI providers
  - LocalProvider: Mock implementation for development and testing
  - OpenAIProvider: Integration with OpenAI's GPT models

## Usage

### Basic Usage

```python
from src.modules.script_generator import ScriptGenerator
from pathlib import Path

# Initialize the script generator
generator = ScriptGenerator()

# Generate a script from images
script = generator.generate_script(
    images=[Path("image1.png"), Path("image2.png")],
    description="Demo of our new product features",
    title="Product Demo",
    target_duration=60  # Target 60 seconds total
)

# Access the generated script
for segment in script["segments"]:
    print(f"Segment {segment['id']}")
    print(f"Duration: {segment['duration']} seconds")
    print(f"Narration: {segment['narration']}")
    print()
```

### Selecting AI Models

```python
# List available models
available_models = generator.get_available_models()
print(f"Available models: {', '.join(available_models)}")

# Set a specific model
generator.set_ai_model("gpt-4")

# Generate with the selected model
script = generator.generate_script(...)
```

### Estimating Generation Time

```python
# Estimate time required for generation
estimated_time = generator.estimate_generation_time(
    num_images=5,
    description_length=len("Description of the demo content")
)
print(f"Estimated generation time: {estimated_time} seconds")
```

## Command Line Tools

The module includes several command-line tools:

- **demo_script_generator.py**: Demonstrates the script generator functionality
- **generate_script.py**: Command-line tool for generating scripts from images
- **test_models.py**: Tests different AI models and compares their output
- **verify_script_generator.py**: Verifies the script generator installation

## Configuration

The script generator can be configured by passing a configuration dictionary to the constructor:

```python
generator = ScriptGenerator({
    "model": "gpt-3.5-turbo",  # Default AI model
    "api_key": "your-api-key",  # API key for the service
    "timeout": 60,  # Timeout in seconds for script generation
})
```

## Error Handling

The module defines several exception types for error handling:

- **ScriptGenerationError**: Base class for all script generation errors
- **AIModelError**: Errors related to AI model usage
- **InvalidInputError**: Input validation errors
- **ModelNotAvailableError**: Requested AI model is not available
- **ImageAnalysisError**: Errors during image analysis
- **ScriptGenerationTimeoutError**: Script generation timed out

## Future Enhancements

Planned enhancements for the Script Generator module include:

- Support for additional AI models and services
- Improved image analysis capabilities
- Style-based script generation (formal, casual, technical, etc.)
- Multi-language support
- Content moderation and safety filters
- Fine-tuning capabilities for domain-specific content
