# Epic E001: Core System Architecture and Setup with CLI-Based Video Assembly

## Overview
This epic establishes the foundational architecture and infrastructure for the DemoMaker application with a simplified command-line approach. It implements a core pipeline that takes user-provided images and generates a demo video with AI-created script and narration.

## Background and Context
DemoMaker is a Python-based application that leverages AI agents to automatically create and narrate professional demo videos. This initial epic focuses on establishing the core functionality with a command-line interface, enabling users to generate videos from provided images and text descriptions.

## Goals
- Establish a modular system architecture that follows the ADRs
- Create a working CLI-based application that can generate demo videos
- Implement core AI-powered script and narration generation
- Build a video assembly pipeline using user-provided images
- Set up a file-based storage system for all assets

## Key Components

### Project Structure
- Directory structure following the modular monolithic architecture
- Core module separation and interfaces
- Package management and dependency configuration

### Command-line Interface
- Input validation and processing
- Command parsing and execution
- User feedback and error reporting

### Core Modules
- **Input Processor Module**: Handles command-line arguments, validation of user inputs, and processing of user-provided images
- **Script Generator Module**: Takes input and produces a structured demo script
- **Narration Generator Module**: Creates audio narration from the script
- **Video Assembler Module**: Combines user-provided images and narration into a final video
- **Storage Manager**: Manages file-based storage of all inputs, intermediate assets, and outputs
- **Configuration System**: Provides basic configuration management for different environments

## Success Criteria
- Project structure is established with correctly organized modules following the modular monolithic architecture defined in ADR-0002
- Development environment can be set up within 15 minutes on a new machine using a documented process
- Application can be launched via command-line interface and processes user inputs correctly
- Application successfully assembles a video from user-provided images and AI-generated narration
- File-based storage system is implemented and successfully performs CRUD operations as defined in ADR-0004
- Basic configuration system supports at least 3 environments (development, testing, production) with appropriate separation of concerns
- All core dependencies are properly managed with version pinning and documented requirements
- Project passes initial automated tests that validate the architectural requirements

## Out of Scope
- Graphical user interface
- AI-powered slide/image generation
- Advanced customization options
- Cloud integration
- Multi-user support

## Open Questions
- Which specific AI models should be used for script generation and narration?
- What format and structure should be used for the configuration system?
- What hardware requirements should be recommended for optimal performance?
- How should we handle edge cases like very long videos or unusual image formats?
- What metrics should be tracked to evaluate system performance?

## Dependencies
- ADR-0002: Use Modular Monolithic Architecture
- ADR-0004: Use File-Based Storage
- ADR-0003: Hybrid Local-Cloud AI Model Strategy (for AI integration)
- ADR-0010: AI Model Integration Patterns

## Timeline
- Estimated Duration: 3 weeks
- Estimated Start Date: May 1, 2025
- Estimated Completion Date: May 22, 2025

## Stories/Tasks
1. Set up project structure and repository
2. Create development environment setup process and documentation
3. Implement command-line interface and input processing
4. Develop script generation module with AI integration
5. Build narration generation module with TTS integration
6. Create video assembly module using FFMPEG
7. Implement file-based storage system
8. Set up basic configuration management
9. Write automated tests for core functionality
10. Create documentation for the initial implementation

## Risks and Mitigations
- **Risk**: AI model integration complexity may exceed estimates
  - **Mitigation**: Start with simpler AI models and improve incrementally

- **Risk**: Video processing performance issues on standard hardware
  - **Mitigation**: Implement efficient processing approaches and test on various hardware profiles

- **Risk**: Dependencies on external libraries may introduce compatibility issues
  - **Mitigation**: Pin dependency versions and create a comprehensive requirements file

## Related Documentation
- [Requirements Document](../requirements.md)
- [ADR-0002: Use Modular Monolithic Architecture](../adr/0002-use-modular-monolithic-architecture.md)
- [ADR-0004: Use File-Based Storage](../adr/0004-use-file-based-storage.md)
