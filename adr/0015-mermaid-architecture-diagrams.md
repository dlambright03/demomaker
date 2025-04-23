# 15. Mermaid Architecture Diagrams

Date: April 21, 2025

## Status

Accepted

## Context

While the ASCII art diagrams in ADR #13 provide a basic visualization of the architecture, they have limitations in terms of clarity, maintainability, and aesthetics. Mermaid diagrams offer a more professional, maintainable, and readable alternative that can be rendered in many markdown viewers and documentation systems.

## Decision

We will supplement our architecture documentation with Mermaid diagrams that correspond to the ASCII diagrams created in ADR #13. These diagrams will help stakeholders better understand the system architecture.

### 1. High-Level System Architecture

```mermaid
graph TD
    subgraph DemoMakerApp["DemoMaker Application"]
        UI[Streamlit UI]
        TaskQueue[Task Queue & Workers]
        AgentSystem[Agent System<br>Semantic Kernel]
        Storage[File-based Storage]
        ServiceAdapters[Service Adapters]
    end
    
    UI --> UserInteraction[User Interaction]
    TaskQueue --> BgProcessing[Background Processing]
    AgentSystem --> LocalAI[Local AI Models]
    Storage --> ProjectFiles[Project Files]
    ServiceAdapters --> CloudAI[Cloud AI Services]
      classDef mainComponents fill:#e0e8ff,stroke:#333,stroke-width:2px;
    class DemoMakerApp mainComponents;
```

### 2. Component Architecture

```mermaid
graph TD
    subgraph DemoMakerComponents["DemoMaker Components"]
        Input[Input Processing]
        Content[Content Generation]
        Narration[Narration System]
        Output[Output Production]
    end
    
    Input --> TextAnalysis[Text Analysis<br>Reference Material<br>Processing]
    Content --> ScriptGen[Script Generation<br>Visual Assets<br>Storyboarding]
    Narration --> VoiceSynth[Voice Synthesis<br>Audio Mixing<br>Synchronization]
    Output --> VideoRender[Video Rendering<br>Format Conversion<br>Metadata]
      classDef mainComponents fill:#d0e0ff,stroke:#333,stroke-width:2px;
    class DemoMakerComponents mainComponents;
```

### 3. Agent System Architecture

```mermaid
graph TD
    subgraph AgentSystem["Agent System (Semantic Kernel)"]
        ScriptAgent[Script Agent]
        VisualAgent[Visual Agent]
        NarrationAgent[Narration Agent]
        DirectorAgent[Director Agent]
    end
    
    ScriptAgent --> ScriptFunc[Generate Structure<br>Optimize for Narration]
    VisualAgent --> VisualFunc[Create Images<br>Design Layouts<br>Generate Visualizations]
    NarrationAgent --> NarrationFunc[Text-to-Speech<br>Voice Selection<br>Pacing Control<br>Audio Effects]
    DirectorAgent --> DirectorFunc[Workflow Planning<br>Quality Assurance<br>Inter-agent Coordination]
      classDef agentComponents fill:#d8f0d8,stroke:#333,stroke-width:2px;
    class AgentSystem agentComponents;
```

### 4. Data Flow Diagram

```mermaid
graph TD
    UserInput[User Input<br>Parameters] --> ScriptGen[Script Generation]
    ScriptGen --> VisualGen[Visual Generation]
    VisualGen --> NarrationGen[Narration Generation]
    
    ScriptGen --> ScriptFiles[Script Files]
    VisualGen --> ImageAssets[Image Assets]
    NarrationGen --> AudioFiles[Audio Files]
    
    ScriptFiles --> VideoAssembly[Video Assembly]
    ImageAssets --> VideoAssembly
    AudioFiles --> VideoAssembly
    
    VideoAssembly --> FinalOutput[Final Output]
      classDef inputOutput fill:#f8d9d9,stroke:#333,stroke-width:1px;
    classDef process fill:#d0e0ff,stroke:#333,stroke-width:1px;
    classDef data fill:#d8f0d8,stroke:#333,stroke-width:1px;
    
    class UserInput,FinalOutput inputOutput;
    class ScriptGen,VisualGen,NarrationGen,VideoAssembly process;
    class ScriptFiles,ImageAssets,AudioFiles data;
```

### 5. Processing Pipeline

```mermaid
graph LR
    subgraph TaskQueuePipeline["Task Queue Processing Pipeline"]
        InputTasks[Input Tasks] --> ScriptTasks[Script Tasks]
        ScriptTasks --> VisualTasks[Visual Tasks]
        VisualTasks --> AudioTasks[Audio Tasks]
        AudioTasks --> VideoTasks[Video Tasks]
        
        subgraph WorkerProcesses["Worker Processes"]
            Worker1[Worker 1]
            Worker2[Worker 2]
            Worker3[Worker 3]
            Worker4[Worker 4]
            WorkerN[Worker N]
        end
    end
      classDef pipeline fill:#e0e8ff,stroke:#333,stroke-width:2px;
    classDef tasks fill:#f8e8d9,stroke:#333,stroke-width:1px;
    classDef workers fill:#d8f0d8,stroke:#333,stroke-width:1px;
    
    class TaskQueuePipeline pipeline;
    class InputTasks,ScriptTasks,VisualTasks,AudioTasks,VideoTasks tasks;
    class WorkerProcesses workers;
    class Worker1,Worker2,Worker3,Worker4,WorkerN workers;
```

### 6. UI Architecture

```mermaid
graph TD
    subgraph StreamlitUI["Streamlit UI"]
        ProjectSelection[Project Selection]
        
        subgraph WizardFlow["New Project Wizard Flow"]
            ProjectSetup[Project Setup] --> ScriptCreation[Script Creation]
            ScriptCreation --> VisualDesign[Visual Design]
            VisualDesign --> AudioCreation[Audio Creation]
            AudioCreation --> OutputOptions[Output Options]
        end
        
        subgraph TabbedUI["Existing Project Tabbed UI"]
            DashboardTab[Dashboard Tab]
            ScriptTab[Script Tab]
            VisualTab[Visual Tab]
            AudioTab[Audio Tab]
            RenderTab[Render Tab]
        end
        
        PersistentSidebar[Persistent Sidebar]
    end
      classDef ui fill:#e0e8ff,stroke:#333,stroke-width:2px;
    classDef wizard fill:#d0e0ff,stroke:#333,stroke-width:1px;
    classDef tabs fill:#d8f0d8,stroke:#333,stroke-width:1px;
    classDef sidebar fill:#f8e8d9,stroke:#333,stroke-width:1px;
    
    class StreamlitUI ui;
    class WizardFlow wizard;
    class ProjectSetup,ScriptCreation,VisualDesign,AudioCreation,OutputOptions wizard;
    class TabbedUI tabs;
    class DashboardTab,ScriptTab,VisualTab,AudioTab,RenderTab tabs;
    class PersistentSidebar,ProjectSelection sidebar;
```

### 7. File Storage Structure

```mermaid
graph TD
    DemoMaker[demo_maker/] --> Projects[projects/]
    DemoMaker --> Cache[cache/]
    DemoMaker --> Config[config/]
    DemoMaker --> Logs[logs/]
    
    Projects --> Project1[project_1/]
    Projects --> Project2[project_2/]
    
    Project1 --> Metadata[metadata.json]
    Project1 --> Input[input/]
    Project1 --> Script[script/]
    Project1 --> Visuals[visuals/]
    Project1 --> Audio[audio/]
    Project1 --> Output[output/]
    Project1 --> ProjectCache[cache/]
    
    Visuals --> Raw[raw/]
    Visuals --> Processed[processed/]
    Visuals --> Storyboard[storyboard/]
    
    Audio --> Narration[narration/]
    Audio --> Music[music/]
    Audio --> Effects[effects/]
    
    Output --> Drafts[drafts/]
    Output --> Final[final/]
    
    Cache --> Models[models/]
    Cache --> Templates[templates/]
    Cache --> SharedAssets[shared_assets/]
    
    Config --> AppSettings[app_settings.json]
    Config --> UserProfiles[user_profiles/]
    Config --> ApiKeys[api_keys.enc]
    
    Logs --> AppLog[app.log]
    Logs --> ErrorsLog[errors.log]
    Logs --> PerformanceLog[performance.log]
    
    classDef root fill:#f9f,stroke:#333,stroke-width:2px;
    classDef mainDir fill:#bbf,stroke:#333,stroke-width:1px;
    classDef subDir fill:#bfb,stroke:#333,stroke-width:1px;
    classDef file fill:#fdb,stroke:#333,stroke-width:1px;
    
    class DemoMaker root;
    class Projects,Cache,Config,Logs mainDir;
    class Project1,Project2,Visuals,Audio,Output subDir;
    class Metadata,AppSettings,ApiKeys,AppLog,ErrorsLog,PerformanceLog file;
```
