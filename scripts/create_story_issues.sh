#!/bin/bash

# Script to create GitHub issues for each story in the DemoMaker project
# This script assumes you're already authenticated with GitHub CLI

STORIES_DIR="/workspaces/demomaker/docs/stories"
REPO="dlambright03/demomaker"

# Function to extract content between two patterns
extract_content() {
  local file=$1
  local start_pattern=$2
  local end_pattern=$3
  
  # Use sed to extract content between patterns, removing the patterns themselves
  sed -n "/$start_pattern/,/$end_pattern/{/$start_pattern/d;/$end_pattern/d;p}" "$file"
}

# Loop through all story files
for story_file in "$STORIES_DIR"/*.md; do
  # Extract story ID from filename
  story_id=$(basename "$story_file" | cut -d'-' -f1)
  
  # Extract title
  title=$(grep "^# Story" "$story_file" | sed 's/^# Story [A-Z0-9]\+: //')
  
  # Format full title with story ID
  full_title="$story_id: $title"
  
  # Extract status
  status=$(extract_content "$story_file" "^## Status" "^##" | tr -d '\n' | xargs)
  
  # Extract description
  description=$(extract_content "$story_file" "^## Description" "^##")
  
  # Extract requirements
  requirements=$(extract_content "$story_file" "^## Requirements" "^##")
  
  # Extract acceptance criteria
  acceptance=$(extract_content "$story_file" "^## Acceptance Criteria" "^$")
  
  # Build the body of the issue
  body="## Status\n$status\n\n## Description\n$description\n\n## Requirements\n$requirements\n\n## Acceptance Criteria\n$acceptance\n\n---\nOriginal file: $story_file"
  
  # Create labels based on status
  labels=""
  if [[ "$status" == "Complete" ]]; then
    labels="--label \"status: complete\""
  elif [[ "$status" == "In Progress" ]]; then
    labels="--label \"status: in progress\""
  else
    labels="--label \"status: not started\""
  fi
  
  # Add story label
  labels="$labels --label \"story\""
  
  # Create the GitHub issue using gh cli
  echo "Creating issue for $full_title (Status: $status)"
  
  # Use eval to properly handle the labels parameter
  eval "gh issue create --repo $REPO --title \"$full_title\" --body \"$body\" $labels"
  
  # Pause briefly to avoid rate limiting
  sleep 1
done

echo "All issues created successfully!"
