# DemoMaker Epics

This document provides an index of all project epics for the DemoMaker system. Each epic represents a significant piece of functionality that delivers value to users.

## Epic Overview

| ID | Title | Status | Priority | Description |
|----|-------|--------|----------|-------------|
| E001 | Core System Architecture with CLI-Based Video Assembly | In Progress | Critical | Establishes the foundational architecture and implements a core pipeline that takes user-provided images and generates a demo video with AI-created script and narration. |
| E002 | User Interface Implementation with Streamlit | Planning | High | Develops a user-friendly web interface using Streamlit that allows users to interact with the system more easily, upload images, review generated content, and download final videos. |
| E003 | Project Wizard Implementation | Planning | High | Implements a step-by-step project creation wizard following the hybrid wizard-tabs architecture, focusing on software demos with AI script assistance. |
| E004 | AI-Powered Slide Generation and Enhancement | Planning | Medium | Implements AI capabilities to automatically generate and enhance slides based on script content, with support for various media types including videos. |
| E005 | Advanced Customization Options | Planning | Medium | Enhances DemoMaker with fine-grained controls for video appearance and behavior, including AI-assisted editing for slides and videos. |

## Epic Details

Each epic is defined in a separate file within the `epics` directory. The filename follows the pattern `EXXX-epic-title.md` where XXX is the epic number.

## Epic Statuses

- **Planning**: Epic is being defined and scoped
- **Ready**: Epic is defined and ready for implementation
- **In Progress**: Work on the epic has started
- **Completed**: Epic has been fully implemented
- **Blocked**: Work on the epic is blocked by external factors

## Priority Levels

- **Critical**: Must be completed for MVP
- **High**: Important for core functionality
- **Medium**: Adds significant value but not essential
- **Low**: Nice to have, could be deferred
