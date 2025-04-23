# 6. Hybrid Wizard-Tabs UI Architecture

Date: April 21, 2025

## Status

Accepted

## Context

DemoMaker requires a user interface that balances ease of use for beginners with flexibility for experienced users. The application has a natural workflow progression (input → script → visuals → narration → output), but also needs to support non-linear editing and refinement of projects.

We considered several UI architecture patterns:
1. Page-based navigation with distinct pages for different functions
2. Single-page with tabs for different aspects of demo creation
3. Wizard-style flow guiding users step-by-step through demo creation
4. Dashboard-centric approach focused on project management

We evaluated these patterns based on:
- Ease of use for new users vs. efficiency for experienced users
- Support for both linear and non-linear workflows
- Technical feasibility within Streamlit's framework
- Alignment with the natural demo creation process

## Decision

We will implement a hybrid UI architecture that combines wizard-style flow with tabbed navigation:

1. The application will start with a project selection/creation screen
2. New project creation will follow a guided wizard-style flow through these steps:
   - Project details and input parameters
   - Script generation and editing
   - Visual content creation and customization
   - Narration generation and adjustment
   - Final rendering options
3. Existing projects will open in a tabbed interface with:
   - Dashboard tab for project overview and status
   - Separate tabs for each aspect of the demo (script, visuals, narration, output)
   - Settings tab for project configuration
4. A persistent sidebar will provide:
   - Project navigation
   - Global actions (save, export, etc.)
   - Status information
