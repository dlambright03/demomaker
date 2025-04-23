# 13. Architecture Diagrams

Date: April 21, 2025

## Status

Accepted

## Context

As we've defined the architecture for DemoMaker through multiple ADRs, it's valuable to visualize the system to:
- Provide a shared understanding of the overall architecture
- Illustrate component relationships and interactions
- Support future development and onboarding
- Verify architectural decisions through visualization

## Decision

We will document the DemoMaker architecture using the following diagrams:

### 1. High-Level System Architecture

```
┌───────────────────────────────────────────────────────────────────────────┐
│                           DemoMaker Application                            │
├───────────┬───────────────┬────────────────┬──────────────┬───────────────┤
│           │               │                │              │               │
│  Streamlit│  Task Queue   │  Agent System  │  File-based  │  Service      │
│     UI    │  & Workers    │  (Sem. Kernel) │   Storage    │  Adapters     │
│           │               │                │              │               │
└─────┬─────┴───────┬───────┴────────┬───────┴──────┬───────┴───────┬───────┘
      │             │                │              │               │
      ▼             ▼                ▼              ▼               ▼
┌─────────────┐ ┌────────────┐ ┌──────────────┐ ┌───────────┐ ┌───────────────┐
│  User       │ │ Background │ │  Local AI     │ │ Project   │ │ Cloud AI      │
│ Interaction │ │ Processing │ │  Models       │ │ Files     │ │ Services      │
└─────────────┘ └────────────┘ └──────────────┘ └───────────┘ └───────────────┘
```

### 2. Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DemoMaker Components                                │
├────────────────┬──────────────────┬───────────────────┬─────────────────────────┤
│                │                  │                   │                         │
│  Input         │  Content         │  Narration        │  Output                 │
│  Processing    │  Generation      │  System           │  Production             │
│                │                  │                   │                         │
└────────┬───────┴────────┬─────────┴─────────┬─────────┴─────────────┬───────────┘
         │                │                   │                       │
         ▼                ▼                   ▼                       ▼
┌──────────────┐  ┌───────────────┐  ┌──────────────────┐   ┌──────────────────┐
│Text Analysis │  │Script         │  │Voice             │   │Video             │
│Reference     │  │Generation     │  │Synthesis         │   │Rendering         │
│Material      │  │Visual Assets  │  │Audio Mixing      │   │Format Conversion │
│Processing    │  │Storyboarding  │  │Synchronization   │   │Metadata          │
└──────────────┘  └───────────────┘  └──────────────────┘   └──────────────────┘
```

### 3. Agent System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         Agent System (Semantic Kernel)                        │
├───────────────┬───────────────────┬──────────────────┬───────────────────────┤
│               │                   │                  │                       │
│ Script Agent  │  Visual Agent     │  Narration Agent │  Director Agent       │
│               │                   │                  │                       │
└───────┬───────┴─────────┬─────────┴──────────┬───────┴───────────┬───────────┘
        │                 │                    │                   │
        ▼                 ▼                    ▼                   ▼
┌──────────────┐   ┌─────────────────┐   ┌────────────────┐  ┌───────────────────┐
│Generate      │   │Create Images    │   │Text-to-Speech  │  │Workflow Planning  │
│Structure     │   │Design Layouts   │   │Voice Selection │  │Quality Assurance  │
│Optimize for  │   │Generate         │   │Pacing Control  │  │Inter-agent        │
│Narration     │   │Visualizations   │   │Audio Effects   │  │Coordination       │
└──────────────┘   └─────────────────┘   └────────────────┘  └───────────────────┘
```

### 4. Data Flow Diagram

```
┌─────────────┐      ┌───────────────┐      ┌────────────────┐      ┌───────────────┐
│ User Input  │──►   │ Script        │──►   │ Visual         │──►   │ Narration     │
│ Parameters  │      │ Generation    │      │ Generation     │      │ Generation    │
└─────────────┘      └───────┬───────┘      └────────┬───────┘      └───────┬───────┘
                             │                       │                      │
                             ▼                       ▼                      ▼
                     ┌───────────────┐      ┌────────────────┐      ┌───────────────┐
                     │ Script Files  │      │ Image Assets   │      │ Audio Files   │
                     └───────┬───────┘      └────────┬───────┘      └───────┬───────┘
                             │                       │                      │
                             │                       │                      │
                             └───────────────┬───────┴──────────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Video Assembly  │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Final Output    │
                                    └─────────────────┘
```

### 5. Processing Pipeline

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              Task Queue Processing Pipeline                         │
│                                                                                    │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│  │ Input   │    │ Script  │    │ Visual  │    │ Audio   │    │ Video   │           │
│  │ Tasks   │───►│ Tasks   │───►│ Tasks   │───►│ Tasks   │───►│ Tasks   │           │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘           │
│                                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                           Worker Processes                                   │  │
│  │                                                                             │  │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │  │
│  │  │ Worker1 │    │ Worker2 │    │ Worker3 │    │ Worker4 │    │ WorkerN │   │  │
│  │  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘   │  │
│  │                                                                             │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### 6. UI Architecture

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                               Streamlit UI                                      │
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                           Project Selection                              │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────────┐│
│  │                                                                            ││
│  │                        New Project Wizard Flow                            ││
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  ││
│  │  │ Project │───►│ Script  │───►│ Visual  │───►│ Audio   │───►│ Output  │  ││
│  │  │ Setup   │    │ Creation│    │ Design  │    │ Creation│    │ Options │  ││
│  │  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  ││
│  │                                                                            ││
│  └────────────────────────────────────────────────────────────────────────────┘│
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────────┐│
│  │                                                                            ││
│  │                        Existing Project Tabbed UI                         ││
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  ││
│  │  │Dashboard│    │ Script  │    │ Visual  │    │ Audio   │    │ Render  │  ││
│  │  │   Tab   │    │   Tab   │    │   Tab   │    │   Tab   │    │   Tab   │  ││
│  │  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  ││
│  │                                                                            ││
│  └────────────────────────────────────────────────────────────────────────────┘│
│                                                                                │
│  ┌────────────────────────────────────────────────────────────────────────────┐│
│  │                          Persistent Sidebar                                ││
│  └────────────────────────────────────────────────────────────────────────────┘│
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

### 7. File Storage Structure

```
demo_maker/
├── projects/                       # Root directory for all projects
│   ├── project_1/                  # Individual project folder
│   │   ├── metadata.json           # Project configuration and metadata
│   │   ├── input/                  # User inputs and reference materials
│   │   ├── script/                 # Generated and edited scripts
│   │   ├── visuals/                # Generated images and visual assets
│   │   │   ├── raw/                # Original generated images
│   │   │   ├── processed/          # Modified/enhanced images
│   │   │   └── storyboard/         # Storyboard layouts
│   │   ├── audio/                  # Audio assets
│   │   │   ├── narration/          # Voice narration files
│   │   │   ├── music/              # Background music
│   │   │   └── effects/            # Sound effects
│   │   ├── output/                 # Final rendered videos
│   │   │   ├── drafts/             # Work-in-progress renders
│   │   │   └── final/              # Final output files
│   │   └── cache/                  # Project-specific cache
│   │
│   └── project_2/                  # Another project folder
│       └── ...
│
├── cache/                          # System-level cache
│   ├── models/                     # Downloaded AI models
│   ├── templates/                  # Reusable templates
│   └── shared_assets/              # Common assets (music, effects)
│
├── config/                         # Application configuration
│   ├── app_settings.json           # Global application settings
│   ├── user_profiles/              # User profile information
│   └── api_keys.enc                # Encrypted API keys
│
└── logs/                           # Application logs
    ├── app.log                     # Main application log
    ├── errors.log                  # Error logs
    └── performance.log             # Performance metrics
```
