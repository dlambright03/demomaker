#!/bin/bash

# This script removes the "Status" sections from all story description files in the docs/stories directory

STORIES_DIR="/workspaces/demomaker/docs/stories"

# Make sure the directory exists
if [ ! -d "$STORIES_DIR" ]; then
    echo "Error: Stories directory not found at $STORIES_DIR"
    exit 1
fi

echo "Removing status sections from story files..."

# Process each markdown file in the stories directory
for story_file in "$STORIES_DIR"/*.md; do
    if [ -f "$story_file" ]; then
        echo "Processing $story_file"
        
        # Create a temporary file
        temp_file=$(mktemp)
        
        # Use awk to remove the Status section
        # This looks for lines between "## Status" and the next section starting with "##"
        awk '
        BEGIN {skip=0}
        /^## Status/ {skip=1; next}
        /^## / && skip {skip=0}
        !skip {print}
        ' "$story_file" > "$temp_file"
        
        # Replace the original file with the modified content
        mv "$temp_file" "$story_file"
    fi
done

echo "Done! Status sections have been removed from all story files."
