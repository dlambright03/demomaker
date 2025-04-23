# 2. Use Modular Monolithic Architecture

Date: April 21, 2025

## Status

Accepted

## Context

DemoMaker needs an architecture that balances several factors:
- It's a local-only application in its initial version
- It requires multiple AI components (script, visual, narration, director)
- Processing is resource-intensive and asynchronous
- We need to design with future cloud migration in mind
- The system should be maintainable and testable

We considered three architectural approaches:
1. A monolithic architecture where all components are tightly integrated
2. A modular architecture with clear boundaries but still in a single application
3. A local microservices approach where components communicate via APIs

## Decision

We will implement DemoMaker using a modular monolithic architecture. This means:

- The application will run as a single process
- Internal components will have well-defined interfaces and responsibilities
- Components will communicate through in-process method calls and events
- Business logic will be organized into separate modules by domain (input processing, content generation, narration, rendering)
- Common infrastructure concerns (logging, caching, data access) will be shared
