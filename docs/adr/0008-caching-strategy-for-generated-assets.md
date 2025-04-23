# 8. Caching Strategy for Generated Assets

Date: April 21, 2025

## Status

Accepted

## Context

DemoMaker generates various assets during the demo creation process:
- Text content (scripts, captions)
- Images and visual elements
- Audio files (narration, music, sound effects)
- Video segments and transitions
- Rendered output files

These assets:
- Can be resource-intensive and time-consuming to generate
- May need to be accessed repeatedly during the editing process
- Might be reused across different parts of a demo
- Take up disk space that should be managed

An effective caching strategy is needed to:
- Reduce redundant operations
- Improve responsiveness of the UI
- Manage disk space usage
- Support recovery in case of failures
- Enable efficient iteration during the creative process

## Decision

We will implement a multi-level caching strategy for generated assets:

1. **Cache Structure**:
   - Project-level cache folder within the project directory
   - System-level cache for shareable assets (e.g., common sound effects)
   - In-memory cache for frequently accessed small assets
   - Cache registry in JSON for tracking and management

2. **Cache Identification**:
   - Content-based hashing for deterministic assets
   - Input parameters + timestamp for non-deterministic assets (e.g., AI-generated content)
   - Hierarchical naming scheme for easy browsing
   - Metadata to track dependencies between cached items

3. **Cache Management**:
   - Time-based expiration for system-level cache items
   - User-configurable cache size limits
   - LRU (Least Recently Used) eviction policy
   - Manual cache clearing option in the UI
   - Automatic cleanup of orphaned cache entries

4. **Cache Invalidation**:
   - Dependency tracking to invalidate dependent assets when inputs change
   - Version tagging to handle algorithm changes
   - Soft invalidation where possible (mark as invalid but don't delete)
   - Validation of cached assets before use

5. **Caching Policies**:
   - Always cache final output assets
   - Cache intermediate results for in-progress projects
   - Optional caching for easily regenerated assets
   - Prioritize caching resource-intensive operations
