# 12. Agent Interaction Library Selection

Date: April 21, 2025

## Status

Accepted

## Context

DemoMaker requires interaction with multiple AI agents and models:
- Script Agent using LLMs
- Visual Agent using text-to-image models
- Narration Agent using text-to-speech models
- Director Agent coordinating the workflow

We need to select a library or framework that will:
- Provide a consistent interface across different AI services
- Support both cloud-based and local model execution
- Allow for structured interactions with agent components
- Handle context management and prompt engineering
- Be compatible with our Python 3.11+ environment
- Meet security requirements

Several options are available:
1. Microsoft Semantic Kernel - Framework for integrating AI with programming languages
2. LlamaIndex - Specialized in data connection and retrieval for LLMs
3. LangChain - Comprehensive framework for LLM applications with agent support (excluded due to security concerns)
4. Custom implementation using direct API clients
5. Combination of specialized libraries for each agent type

## Decision

We will use **Microsoft Semantic Kernel** as our primary agent interaction library, supplemented with specialized libraries for specific capabilities:

1. **Microsoft Semantic Kernel** will be used for:
   - Core agent implementation and orchestration
   - LLM interaction (Script Agent, Director Agent)
   - Semantic function design and management
   - Structured prompt templating via skills and functions
   - Memory and context management
   - Planning and sequential processing workflows

2. **Supplementary libraries**:
   - Stability SDK or DALL-E client libraries for image generation (Visual Agent)
   - ElevenLabs Python SDK for voice synthesis (Narration Agent)
   - Custom adapters to integrate these specialized libraries with Semantic Kernel's plugin system

3. **Implementation approach**:
   - Create a skill-based architecture using Semantic Kernel's plugin system
   - Implement native and semantic functions for core capabilities
   - Develop custom connectors for specialized AI services
   - Use planner for agent orchestration
   - Leverage memory system for context management across interactions
