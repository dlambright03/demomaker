# 4. Use File-Based Storage for Project Data

Date: April 21, 2025

## Status

Accepted

## Context

DemoMaker needs to store several types of data:
- Project metadata (title, description, parameters)
- Generated scripts and storyboards
- Visual assets (images, slides, transitions)
- Audio files (narration, music, sound effects)
- Final rendered videos
- User preferences and settings

We considered several storage options:
1. File-based storage (projects as files/folders with metadata and assets)
2. SQLite database (embedded database for structured data)
3. Hybrid approach (SQLite + file system for large assets)
4. Local document database (like MongoDB)

Key considerations included:
- The application runs locally on user machines
- Data includes large binary assets (images, audio, video)
- Users may want to manually access or back up their project files
- Future cloud migration should be possible
- Simplicity of implementation and maintenance

## Decision

We will implement a file-based storage system where:

1. Each project will be stored in its own directory structure
2. Project metadata will be stored in JSON files
3. Assets will be stored in appropriate subdirectories (images, audio, video)
4. Consistent naming conventions and directory structures will be used
5. A versioning scheme will be included in the file structure
6. File locking mechanisms will be implemented for concurrent access safety
