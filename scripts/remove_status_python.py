#!/usr/bin/env python3

import os
import re


def remove_status_sections(directory):
    """Remove Status sections from all markdown files in the specified directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            print(f"Processing {filepath}")

            with open(filepath, "r") as file:
                content = file.read()

            # Pattern to match the Status section (from '## Status' until the next section starting with '##')
            pattern = r"## Status\s*\n.*?\n(?=## |$)"
            # Replace that section with an empty string
            new_content = re.sub(pattern, "", content, flags=re.DOTALL)

            with open(filepath, "w") as file:
                file.write(new_content)

            print(f"  Status section removed from {filename}")


if __name__ == "__main__":
    stories_dir = "/workspaces/demomaker/docs/stories"
    print(f"Removing Status sections from story files in {stories_dir}")
    remove_status_sections(stories_dir)
    print("Done!")
