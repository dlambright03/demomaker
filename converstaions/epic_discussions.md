# Epic Discussions for DemoMaker

This file captures our conversations about project epics. Each discussion should result in a formalized epic entry that will be added to the epics directory.

## Discussion Format

For each epic discussion, use the following format:

```
## [Date] - [Epic Topic]

### Initial Proposal
[Initial description of the epic]

### Discussion
[Record of our conversation, including questions, clarifications, and decisions]

### Consensus
[The final agreement on the epic details]

### Action Items
- Create epic document
- Update relevant architecture decisions
- Other follow-up tasks
```

## List of Discussions

1. [2025-04-22] - [Core System Architecture and Setup]
2. [2025-04-22] - [User Interface Implementation]
3. [2025-04-22] - [Project Wizard Implementation]
4. [2025-04-22] - [AI-Powered Slide Generation]
5. [2025-04-22] - [Advanced Customization Options]
6. [Future discussions will be added here]

## 2025-04-22 - Core System Architecture and Setup

### Initial Proposal

**Epic Title**: Core System Architecture and Setup

**Description**: This epic focuses on establishing the foundational architecture and infrastructure for the DemoMaker application. It includes setting up the project structure, implementing the modular monolithic architecture, establishing the development environment, and creating the basic application framework that other epics will build upon.

**Key Components**:
- Project initialization and structure
- Development environment setup
- Implementation of the modular architecture
- Basic application framework
- Local data storage system
- Configuration management
- Core dependency management
- CI/CD pipeline setup

**Success Criteria**:
- Project structure is established with correctly organized modules following the modular monolithic architecture defined in ADR-0002
- Development environment can be set up within 15 minutes on a new machine using a documented process
- Application can be launched via command-line interface and processes user inputs correctly
- Application successfully assembles a video from user-provided images and AI-generated narration
- File-based storage system is implemented and successfully performs CRUD operations as defined in ADR-0004
- Basic configuration system supports at least 3 environments (development, testing, production) with appropriate separation of concerns
- All core dependencies are properly managed with version pinning and documented requirements
- Project passes initial automated tests that validate the architectural requirements

### Discussion

**Initial scope refinement:**

I think we should focus on getting a system that works without a UI that is very basic and just generates a video with a script and a series of slide images.

This approach makes sense as it allows us to:
1. Focus on the core functionality without getting distracted by UI complexities
2. Establish the foundational pipeline that transforms input into a complete video
3. Test the integration of the various AI components with minimal overhead
4. Get a working prototype faster to validate the core concept

This would mean our initial architecture should prioritize:
- A command-line interface for accepting basic inputs
- The core script generation capability
- Basic video assembly from user-provided images and narration (rather than generating slides ourselves)
- File-based storage of all assets and outputs

**Further simplification:**

Let's push generating slides to a later epic. The user can just provide pictures they'd like to use as slides in the initial version. This allows us to:
1. Focus on the core video assembly and narration pipeline
2. Reduce complexity in the first iteration
3. Allow users to maintain creative control over visual content initially
4. Defer the more complex AI-based image generation to a future enhancement

### Consensus

**Epic Title**: Core System Architecture and Setup with CLI-Based Video Assembly

**Description**: This epic focuses on establishing the foundational architecture and infrastructure for the DemoMaker application with a simplified command-line approach. It implements a core pipeline that takes user-provided images and generates a demo video with AI-created script and narration.

**Key Components**:
- Project initialization and structure
- Development environment setup
- Implementation of the modular architecture
- Command-line interface
- Input processor module
- Script generator module
- Narration generator module
- Video assembler module
- File-based storage system
- Basic configuration system
- Core dependency management

**Success Criteria**:
- Project structure is established with correctly organized modules following the modular monolithic architecture defined in ADR-0002
- Development environment can be set up within 15 minutes on a new machine using a documented process
- Application can be launched via command-line interface and processes user inputs correctly
- Application successfully assembles a video from user-provided images and AI-generated narration
- File-based storage system is implemented and successfully performs CRUD operations as defined in ADR-0004
- Basic configuration system supports at least 3 environments (development, testing, production) with appropriate separation of concerns
- All core dependencies are properly managed with version pinning and documented requirements
- Project passes initial automated tests that validate the architectural requirements

**Out of Scope**:
- Graphical user interface
- AI-powered slide/image generation
- Advanced customization options
- Cloud integration
- Multi-user support

### Action Items
- Create epic document with the agreed details
- Update ADR-0002 and ADR-0004 if needed to reflect CLI-first approach
- Set up initial project structure following the modular architecture
- Establish development environment setup instructions

## 2025-04-22 - User Interface Implementation

### Initial Proposal

**Epic Title**: User Interface Implementation with Streamlit

**Description**: This epic focuses on developing a user-friendly web interface for DemoMaker using Streamlit. Building on the core CLI functionality established in Epic E001, this epic will create an intuitive graphical interface that allows users to interact with the system more easily, upload images, review generated content, and download final videos.

**Key Components**:
- Streamlit application structure and setup
- Main dashboard and project management UI
- Image upload and management interface
- Script review and editing capabilities
- Video preview and playback functionality
- Export and download options
- Form validation and error handling
- Responsive design for different screen sizes
- Integration with existing core modules

**Success Criteria**:
- Users can create new demo projects through an intuitive web interface
- Image upload functionality supports multiple file formats and provides preview capabilities
- Generated scripts can be viewed and edited through the UI
- Final videos can be previewed, downloaded, and shared
- UI automatically adapts to different screen sizes and devices
- Error messages are clear and provide guidance on resolution
- The application maintains consistent performance across supported browsers
- All core functionality available in the CLI is accessible through the UI

### Discussion

**Project wizard consideration:**

Does this include the new project wizard or is that for a future epic?

Let's keep it in the later epic. For this UI epic, we'll focus on the core UI functionality that directly interfaces with the existing CLI capabilities. A more sophisticated wizard-based project creation flow will be developed in a subsequent epic to enhance the user experience once the fundamental UI components are in place.

The current UI epic will include basic project creation forms but not the full step-by-step wizard experience described in ADR-0006 (hybrid-wizard-tabs-ui-architecture). This allows us to:

1. Get the essential UI functionality in place more quickly
2. Focus on the core user flows that interface with our existing backend capabilities
3. Defer the more complex wizard implementation until we have feedback on the basic UI
4. Implement the wizard later with insights from actual user interactions

### Consensus

**Epic Title**: User Interface Implementation with Streamlit

**Description**: This epic focuses on developing a user-friendly web interface for DemoMaker using Streamlit. Building on the core CLI functionality established in Epic E001, this epic will create an intuitive graphical interface that allows users to interact with the system more easily, upload images, review generated content, and download final videos.

**Key Components**:
- Streamlit application structure and setup
- Main dashboard and project management UI
- Image upload and management interface
- Script review and editing capabilities
- Video preview and playback functionality
- Export and download options
- Form validation and error handling
- Responsive design for different screen sizes
- Integration with existing core modules

**Success Criteria**:
- Users can create new demo projects through a basic form-based interface
- Image upload functionality supports multiple file formats and provides preview capabilities
- Generated scripts can be viewed and edited through the UI
- Final videos can be previewed, downloaded, and shared
- UI automatically adapts to different screen sizes and devices
- Error messages are clear and provide guidance on resolution
- The application maintains consistent performance across supported browsers
- All core functionality available in the CLI is accessible through the UI

**Out of Scope**:
- Step-by-step project creation wizard (will be addressed in a future epic)
- Advanced UI customization options
- Multi-user authentication and permissions
- Cloud-based storage integrations
- AI-powered slide/image generation (as decided in Epic E001)

### Action Items
- Create epic document with the agreed details
- Review ADR-0006 (hybrid-wizard-tabs-ui-architecture) to ensure future compatibility
- Set up Streamlit project structure within the existing architecture
- Define UI component hierarchy and interactions

## 2025-04-22 - Project Wizard Implementation

### Initial Proposal

**Epic Title**: Project Wizard Implementation with Hybrid Wizard-Tabs Architecture

**Description**: This epic focuses on implementing a step-by-step project creation wizard within the DemoMaker application, following the hybrid wizard-tabs architecture defined in ADR-0006. Building on the basic UI established in Epic E002, this epic will create an intuitive, guided experience for users to create demo projects with minimal effort while still allowing for advanced customization options.

**Key Components**:
- Wizard infrastructure based on the hybrid wizard-tabs architecture
- Step-by-step project creation flow
- Context-aware guidance and help system
- Demo type selection and customization
- Advanced slide sequencing and arrangement
- Intelligent content suggestions based on user inputs
- Narration style and voice customization
- Progress tracking and state management
- Integration with existing UI components

**Success Criteria**:
- Users can create new projects through an intuitive, guided wizard interface
- Wizard follows the hybrid pattern described in ADR-0006, combining step-by-step guidance with tab-based navigation
- Users receive context-sensitive help and guidance throughout the creation process
- The wizard validates inputs at each step before proceeding
- Users can navigate backward and forward through the wizard steps without losing data
- Advanced users can skip to specific sections using the tab interface
- The wizard provides intelligent defaults and suggestions based on the project type
- The wizard integrates seamlessly with the existing UI components

### Discussion

**Demo type prioritization and AI assistance:**

Software demos are the priority for this wizard implementation. While the system should support various demo types eventually, the initial wizard should focus primarily on creating effective software demonstrations, with specialized workflows and templates optimized for this use case.

Some AI assistance would be nice, specifically a script assistant integrated into the wizard. This AI script assistant would help users create more effective demo narratives by:

1. Analyzing the software being demonstrated to suggest key features to highlight
2. Providing structural templates for different types of software demos (e.g., product walkthrough, feature introduction, tutorial)
3. Offering suggestions for improving script clarity, engagement, and flow
4. Helping users tailor the script to different audience types (technical, business, etc.)
5. Generating connective language between user-defined key points

This AI script assistance should be integrated directly into the project creation flow, giving contextual suggestions at the appropriate steps rather than being a separate tool.

### Consensus

**Epic Title**: Project Wizard Implementation with Hybrid Wizard-Tabs Architecture

**Description**: This epic focuses on implementing a step-by-step project creation wizard within the DemoMaker application, following the hybrid wizard-tabs architecture defined in ADR-0006. Building on the basic UI established in Epic E002, this epic will create an intuitive, guided experience for users to create demo projects with minimal effort while still allowing for advanced customization options.

**Key Components**:
- Wizard infrastructure based on the hybrid wizard-tabs architecture
- Step-by-step project creation flow with software demos as the priority
- Context-aware guidance and help system
- AI script assistant for demo narrative creation
- Advanced slide sequencing and arrangement
- Demo type templates optimized for software demonstrations
- Narration style and voice customization
- Progress tracking and state management
- Integration with existing UI components

**Success Criteria**:
- Users can create software demo projects through an intuitive, guided wizard interface
- Wizard follows the hybrid pattern described in ADR-0006, combining step-by-step guidance with tab-based navigation
- AI script assistant provides contextual suggestions for improving demo narratives
- Users receive context-sensitive help and guidance throughout the creation process
- The wizard validates inputs at each step before proceeding
- Users can navigate backward and forward through the wizard steps without losing data
- Advanced users can skip to specific sections using the tab interface
- The wizard provides intelligent defaults and suggestions based on the software being demonstrated
- The wizard integrates seamlessly with the existing UI components

**Out of Scope**:
- AI-powered slide/image generation (to be addressed in a future epic)
- Advanced demo types beyond software demonstrations
- Multi-user collaboration features
- Real-time preview of the generated video
- Integration with third-party software analysis tools

### Action Items
- Create epic document with the agreed details
- Review ADR-0006 (hybrid-wizard-tabs-ui-architecture) to ensure implementation follows the defined patterns
- Define the specific steps and flow for software demo creation
- Design the AI script assistant integration points

## 2025-04-22 - AI-Powered Slide Generation

### Initial Proposal

**Epic Title**: AI-Powered Slide Generation and Enhancement

**Description**: This epic focuses on implementing AI-powered capabilities to automatically generate and enhance slides for demo videos. Building on the foundation established in the previous epics, this feature will reduce the manual effort required from users by creating visually compelling slides based on script content and user inputs, particularly for software demonstrations.

**Key Components**:
- Text-to-image generation for conceptual slides
- Screenshot analysis and enhancement for software demos
- Automatic layout and design system
- Visual consistency enforcement across slides
- Text overlay and annotation generation
- Branding and style customization
- Slide template creation and management
- Integration with script content for contextual relevance
- Slide sequence optimization

**Success Criteria**:
- System can generate visually consistent slides based on script content
- For software demos, system can enhance and annotate user-provided screenshots
- Generated slides follow design best practices for clarity and engagement
- Visual elements maintain consistency with user-defined branding and style guidelines
- Text overlays are properly positioned and sized for readability
- The generation process is efficient enough to create slides for a 5-minute demo in under 10 minutes
- Users can customize and adjust generated slides as needed
- The system integrates seamlessly with the existing project wizard and UI

### Discussion

**User control and wizard integration:**

I think the users should have control on the detailed app side but maybe less in the wizard. This suggests a two-tiered approach to slide generation:

1. In the wizard: A more streamlined, guided experience with fewer options but quicker results. The focus would be on generating consistent slides quickly with minimal user input required. This would help new users create decent slides without overwhelming them with options.

2. In the detailed app: More granular control over slide generation, including the ability to adjust individual slide elements, fine-tune generated content, and apply custom formatting. This would serve more experienced users who want precise control.

**Visual consistency and approval workflow:**

I would think for the wizard there would be an option to generate slides and also for visual consistency when all the slides are approved. This suggests implementing:

1. A slide generation option directly within the wizard flow, perhaps as an optional step
2. A visual consistency pass as a final step after all slides are approved, ensuring the entire presentation maintains a cohesive look and feel
3. An approval workflow where users can review and approve generated slides before finalizing

**AI model requirements:**

I'm not sure of the AI model requirements for this functionality. We'll need to investigate:

1. Which text-to-image models would be appropriate for generating concept slides
2. What computer vision capabilities would be needed for screenshot analysis and enhancement
3. How to implement design systems that follow presentation best practices
4. The computational requirements for running these models locally vs. cloud-based processing

This would need further research to determine the specific AI capabilities required and whether they can be implemented within our hybrid local-cloud AI model strategy (ADR-0003).

**Content visualization and media integration:**

I would think the slide generation would provide visualizations for the content being talked about at the moment in the script. If nothing is specified maybe just provide a background. This approach would:

1. Create a direct correlation between the narration and the visuals
2. Ensure that what's being shown is relevant to what's being said
3. Provide appropriate background visuals when no specific content is being referenced
4. Enhance understanding by visualizing concepts mentioned in the script

There may also be parts for transitions between slides or combining images into one slide. These features would allow:

1. Smooth visual flow between different segments of the presentation
2. Creation of composite slides that show multiple related images/screenshots
3. Visual comparison of different elements (before/after, feature comparisons, etc.)
4. More dynamic and engaging presentations beyond static single-image slides

Also we should have support to include recorded videos as slides for a presentation. This capability would:

1. Enable demonstrations of dynamic software features that still images can't capture
2. Allow inclusion of pre-recorded demo segments within the larger presentation
3. Support mixed-media presentations that combine still images and video clips
4. Provide more flexibility in content types for comprehensive demonstrations

### Consensus

**Epic Title**: AI-Powered Slide Generation and Enhancement

**Description**: This epic focuses on implementing AI-powered capabilities to automatically generate and enhance slides for demo videos. Building on the foundation established in the previous epics, this feature will reduce the manual effort required from users by creating visually compelling slides based on script content and user inputs, particularly for software demonstrations.

**Key Components**:
- Text-to-image generation for conceptual slides
- Screenshot analysis and enhancement for software demos
- Automatic layout and design system
- Visual consistency enforcement across slides
- Text overlay and annotation generation
- Branding and style customization
- Slide template creation and management
- Integration with script content for contextual relevance
- Slide sequence optimization
- Content-driven visualization generation
- Transition effects between slides
- Composite slide creation
- Video integration and support
- Two-tiered control system (simplified in wizard, detailed in main app)

**Success Criteria**:
- System can generate visually consistent slides based on script content
- For software demos, system can enhance and annotate user-provided screenshots
- Generated slides follow design best practices for clarity and engagement
- Visual elements maintain consistency with user-defined branding and style guidelines
- Text overlays are properly positioned and sized for readability
- The generation process is efficient enough to create slides for a 5-minute demo in under 10 minutes
- Users can customize and adjust generated slides as needed
- The system integrates seamlessly with the existing project wizard and UI
- System supports different levels of user control in wizard vs. detailed view
- System can incorporate video clips as slide elements
- Content visualizations correspond to the script narration at each point
- System can create composite slides combining multiple elements

**Out of Scope**:
- Real-time video rendering and effects
- User-trainable custom AI models
- Advanced animation creation
- Integration with third-party presentation tools
- Multi-user collaborative slide editing

**Open Questions**:
- Specific AI models to use for text-to-image generation and screenshot enhancement
- Performance considerations for video processing and integration
- Computation requirements and boundaries between local and cloud processing
- Detailed implementation for the approval workflow and visual consistency pass
- Specific slide templates optimized for software demonstrations

### Action Items
- Create epic document with the agreed details
- Research appropriate AI models for implementation
- Define integration points with the wizard from Epic E003
- Implement proof-of-concept for script-to-visualization mapping
- Design the two-tiered control system architecture

## 2025-04-22 - Advanced Customization Options

### Initial Proposal

**Epic Title**: Advanced Customization Options

**Description**: This epic focuses on enhancing DemoMaker with more fine-grained controls for video outputs and presentation customization. Building on the foundation established in previous epics, these advanced options will give users greater control over the appearance, style, and behavior of their demo videos, allowing for more professional and branded content creation.

**Key Components**:
- Custom branding templates and themes
- Advanced animation and transition effects
- Audio mixing and background music support
- Subtitle and accessibility features
- Fine-grained timing controls for slide presentations
- Custom overlay and annotation tools
- Video effect and filter options
- Enhanced text formatting and styling
- Custom color schemes and visual styles
- Personalized intro and outro sequences

**Success Criteria**:
- Users can apply custom branding across all generated content
- Advanced transitions between slides enhance visual flow
- Background music and audio mixing capabilities improve overall production quality
- Accessibility features including subtitles and screen reader support are available
- Fine-grained timing controls allow precise customization of presentation pacing
- Text formatting options support corporate style guidelines and enhanced readability
- Custom overlays and annotations provide additional context and emphasis
- The system maintains consistency while allowing for customization
- All customizations can be saved as reusable templates
- The interface for customization is intuitive and well-organized

### Discussion

**Customization approach:**

The advanced customization options should be designed to balance power and usability. We should use a layered approach that makes basic customizations easy while allowing advanced users to access more sophisticated controls when needed.

Key areas to focus on include:

1. **Corporate branding support** - Many software demos will need to adhere to corporate style guidelines, so we should make it easy to apply consistent branding across all slides, including:
   - Logo placement and sizing
   - Corporate color schemes and fonts
   - Standard intro and outro sequences
   - Consistent lower-third designs for identifying speakers or features

2. **Enhanced visual presentation** - Professional software demos benefit from visual enhancements that improve viewer engagement:
   - Smooth transitions between content sections
   - Highlight and focus effects to draw attention to specific UI elements
   - Motion effects to simulate interaction with the software
   - Zoom and pan capabilities for showcasing detailed UI elements

3. **Audio enhancements** - Audio quality significantly impacts viewer perception of professional quality:
   - Background music with appropriate volume mixing
   - Sound effects for transitions or key points
   - Noise reduction and audio normalization
   - Multiple narrator voices for different sections

4. **Accessibility and inclusivity** - Making demos accessible to all potential viewers:
   - High-contrast options for visually impaired users   - Subtitles and closed captions with formatting options
   - Transcript generation and export
   - Screen reader compatibility

5. **AI-assisted editing** - Providing intelligent assistance during the customization process:
   - Smart editing suggestions for improving slide visuals
   - Automated video enhancement and cleanup
   - Content-aware cropping and framing for video slides
   - Automatic highlight generation for important video moments
   - Intelligent removal of unwanted elements from video frames
   - Style transfer between slides to maintain consistency

**Future feature considerations:**

While implementing the advanced customization options, we should establish foundations for potential future epics, including:

1. **Cloud Integration and Deployment** - For future consideration, we could extend DemoMaker to support cloud-based deployment with:
   - Cloud storage for projects and assets
   - Cloud-based processing for resource-intensive operations
   - Sharing and collaboration capabilities
   - Cross-device access to projects

2. **Multi-User Collaboration** - Future functionality could include:
   - Real-time collaborative editing
   - Role-based access controls
   - Version control and change history
   - Review and approval workflows

3. **Analytics and Reporting** - Later enhancements could provide insights on:
   - Viewer engagement metrics
   - Content effectiveness analysis
   - Usage patterns and optimizations
   - Export options for analytics data

4. **Enterprise Integration** - For organizational use, we might consider:
   - SSO and enterprise authentication integration
   - Compliance and governance features
   - Integration with corporate content management systems
   - Department/team management

### Consensus

**Epic Title**: Advanced Customization Options

**Description**: This epic focuses on enhancing DemoMaker with more fine-grained controls for video outputs and presentation customization. Building on the foundation established in previous epics, these advanced options will give users greater control over the appearance, style, and behavior of their demo videos, allowing for more professional and branded content creation.

**Key Components**:
- Custom branding templates and themes
- Advanced animation and transition effects
- Audio mixing and background music support
- Subtitle and accessibility features
- Fine-grained timing controls for slide presentations
- Custom overlay and annotation tools
- Video effect and filter options
- Enhanced text formatting and styling
- Custom color schemes and visual styles
- Personalized intro and outro sequences
- AI-assisted slide and video editing capabilities

**Success Criteria**:
- Users can apply custom branding across all generated content
- Advanced transitions between slides enhance visual flow
- Background music and audio mixing capabilities improve overall production quality
- Accessibility features including subtitles and screen reader support are available
- Fine-grained timing controls allow precise customization of presentation pacing
- Text formatting options support corporate style guidelines and enhanced readability
- Custom overlays and annotations provide additional context and emphasis
- The system maintains consistency while allowing for customization
- All customizations can be saved as reusable templates
- The interface for customization is intuitive and well-organized
- AI can assist with editing and enhancing slides, including video content

**Out of Scope**:
- Real-time collaboration on customizations
- Cloud-based template storage and sharing
- Advanced video editing capabilities (beyond slide-based presentations)
- Integration with third-party design tools
- Custom animation creation tooling

**Open Questions**:
- What level of customization control should be exposed to different user personas?
- How can templates be structured to maximize reusability while maintaining flexibility?
- What is the performance impact of complex transitions and effects?
- How should accessibility features be prioritized and implemented?
- What standards should be supported for subtitle formats?

### Action Items
- Create epic document with the agreed details
- Research best practices for video customization interfaces
- Design template system for various customization options
- Ensure compatibility with existing content generation pipelines
- Develop prototype for key customization interfaces
