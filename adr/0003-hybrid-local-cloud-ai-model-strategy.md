# 3. Hybrid Local-Cloud AI Model Strategy

Date: April 21, 2025

## Status

Accepted

## Context

DemoMaker requires several AI capabilities:
- Script generation using large language models
- Visual content generation using text-to-image models
- Voice synthesis using text-to-speech models
- Intelligent scene composition using multimodal AI models

These AI models can be resource-intensive and may exceed the capabilities of typical local machines, especially for large language models and advanced image generation. However, we want the application to run locally while still providing high-quality results.

We considered several approaches:
1. Embedding smaller AI models directly with the application
2. Allowing users to download models on first use and cache locally
3. Creating a local API gateway to external AI services
4. Using a hybrid approach with some local models and some cloud connections

## Decision

We will implement a hybrid approach where:

1. The application core and execution pipeline will run entirely locally
2. For LLM-based operations (script generation, content planning), we'll connect to cloud services like Azure OpenAI
3. For less resource-intensive AI tasks, we'll provide options for local execution using downloadable models
4. We'll implement a provider pattern that abstracts the specific implementation (local vs. cloud)
5. We'll include fallback capabilities where possible to degrade gracefully when cloud services are unavailable
