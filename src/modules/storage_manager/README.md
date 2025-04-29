# File-Based Storage System

This module implements the file-based storage system for the DemoMaker application, following the approach defined in [ADR-0004](../../../docs/adr/0004-use-file-based-storage.md).

## Features

- **Thread-safe operations** using file locking
- **Cross-platform compatibility** with Windows, macOS, and Linux
- **Consistent directory structure** for all project assets
- **Asset metadata and integrity checking**
- **Automatic cleanup** of temporary files
- **Search and filtering** capabilities
- **Import/export functionality** for project sharing
- **Comprehensive error handling** for all operations

## Directory Structure

Each project is stored in its own directory with the following structure:

```
project_id/
  ├── images/         # Input images
  |    ├── image_001.png
  |    ├── image_001.png.meta.json  # Metadata for the image
  |    └── ...
  ├── script/         # Generated scripts
  |    ├── script_20250429123456.json
  |    ├── script_20250429123456.json.meta.json  # Metadata for the script
  |    └── ...
  ├── narration/      # Audio narration files
  |    ├── narration_20250429123456.mp3
  |    ├── narration_20250429123456.mp3.meta.json  # Metadata for the narration
  |    └── ...
  ├── video/          # Output videos
  |    ├── video_20250429123456.mp4
  |    ├── video_20250429123456.mp4.meta.json  # Metadata for the video
  |    └── ...
  ├── metadata/       # Project metadata
  |    └── project.json  # Main project metadata file
  └── temp/           # Temporary processing files (cleaned up automatically)
```

## Usage

### Basic Operations

```python
from src.modules.storage_manager import FileStorageManager

# Initialize the storage manager
storage_manager = FileStorageManager()

# Create a new project
project_id = storage_manager.initialize_project("My Demo Project")

# Store input images
from pathlib import Path
image_paths = [Path("image1.png"), Path("image2.png")]
stored_images = storage_manager.store_input_images(project_id, image_paths)

# Store a script
script = {
    "title": "My Demo Script",
    "slides": [
        {"title": "Slide 1", "content": "Content 1"},
        {"title": "Slide 2", "content": "Content 2"}
    ]
}
script_path = storage_manager.store_script(project_id, script)

# Store narration
narration_path = Path("narration.mp3")
stored_narration = storage_manager.store_narration(project_id, narration_path)

# Store output video
video_path = Path("output.mp4")
stored_video = storage_manager.store_output_video(project_id, video_path)

# Get project metadata
metadata = storage_manager.get_project_metadata(project_id)

# Get project assets
all_assets = storage_manager.get_project_assets(project_id)
image_assets = storage_manager.get_project_assets(project_id, "images")

# Delete a project
storage_manager.delete_project(project_id)
```

### Advanced Features

```python
# Search for projects
projects = storage_manager.search_projects("Demo")

# Find assets by name pattern
assets = storage_manager.find_asset_by_name(project_id, "image_*.png")

# Verify project integrity
results = storage_manager.verify_project_integrity(project_id)

# Clean up temporary files
storage_manager.cleanup_temporary_files(project_id)

# Export a project
export_path = Path("exported_project.zip")
storage_manager.export_project(project_id, export_path)

# Import a project
imported_project_id = storage_manager.import_project(export_path)
```

## Error Handling

The storage manager provides specific exceptions for different error conditions:

- `StorageError`: Base exception for all storage-related errors
- `StorageAccessError`: Raised when storage access is denied or fails
- `ProjectNotFoundError`: Raised when a project cannot be found
- `AssetNotFoundError`: Raised when an asset cannot be found
- `AssetTypeError`: Raised when an invalid asset type is specified
- `InvalidProjectArchiveError`: Raised when a project archive is invalid or corrupted

Example error handling:

```python
from src.interfaces.storage_manager import ProjectNotFoundError, StorageError

try:
    assets = storage_manager.get_project_assets("non_existent_project")
except ProjectNotFoundError:
    print("Project does not exist")
except StorageError as e:
    print(f"Storage error: {e}")
```

## Concurrency and Thread Safety

All operations on a specific project are thread-safe using file locking. This means multiple threads or processes can safely access the same project without data corruption.

## Cleanup and Resource Management

Temporary files are automatically cleaned up:

1. When the application exits
2. Periodically during operation
3. Manually using the `cleanup_temporary_files` method

## Implementation Details

The storage system implements various features to ensure data integrity:

- File hashing for integrity verification
- Atomic file writes for metadata updates
- Project backups before deletion
- Comprehensive logging of all operations
- Cross-platform path handling using `pathlib`
