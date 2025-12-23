# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `1-physical-ai-textbook` | **Date**: 2025-12-12 | **Spec**: specs/1-physical-ai-textbook/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a comprehensive Physical AI & Humanoid Robotics textbook platform using Docusaurus for the frontend and FastAPI for the backend RAG chatbot. The system will include detailed curriculum content on ROS 2, Digital Twin simulation, NVIDIA Isaac, and Vision-Language-Action systems. It will feature user authentication with Better-Auth, personalized content based on user hardware/software background (e.g., Jetson kits, sensor configurations), Urdu translation capabilities, capstone project guidance, and deployment to GitHub Pages. The architecture follows a minimalist approach with a clear separation between the static textbook content and dynamic backend services.

## Technical Context

**Language/Version**: Python 3.11 (FastAPI), JavaScript/Node.js (Docusaurus), SQL (PostgreSQL)
**Primary Dependencies**: Docusaurus, FastAPI, Neon Postgres, Qdrant, Better-Auth, OpenAI APIs, Cohere embeddings, NVIDIA Isaac SDK (reference documentation), ROS 2 documentation (reference content)
**Storage**: Neon Postgres (user data), Qdrant (vector storage for RAG), GitHub Pages (static content)
**Testing**: pytest (backend), Jest/Cypress (frontend)
**Target Platform**: Web application (client-server architecture)
**Project Type**: Web (frontend + backend structure)
**Performance Goals**: API response times under 2 seconds, page load times under 3 seconds, chatbot response times under 5 seconds
**Constraints**: <200ms p95 for API endpoints, Support 1000 concurrent users, Single-source-of-truth for textbook content, AI responses restricted to Physical AI curriculum only
**Scale/Scope**: 1000+ concurrent users, 20+ textbook chapters across 4 modules (ROS 2, Digital Twin, NVIDIA Isaac, VLA), Multiple language support, Hardware profile-based personalization
**Physical AI Content**: Curriculum covering ROS 2 (nodes, topics, services, URDF), Gazebo/Unity simulation, NVIDIA Isaac (Isaac Sim, Isaac ROS, VSLAM), Vision-Language-Action systems, capstone project implementation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Minimalist Architecture**: All components serve essential purposes; Docusaurus for textbook, FastAPI for RAG, Neon Postgres for user data, Qdrant for vector storage
- **Deterministic Workflows**: 7-task development process with clear sequential dependencies
- **Single-Source-of-Truth**: Textbook content as definitive information source for chatbot responses
- **Production-Ready Code**: All code meets production standards with error handling and security
- **Modular Component Design**: Frontend and backend components are modular and loosely coupled
- **Environment-Based Configuration**: All sensitive configs (API keys, DB URLs) will be environment-based

## Project Structure

### Documentation (this feature)

```text
specs/1-physical-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   ├── user.py          # User data models with hardware profile
│   │   ├── content.py       # Textbook content models for Physical AI curriculum
│   │   └── chat.py          # Chat/RAG models with Physical AI restrictions
│   ├── services/
│   │   ├── rag_service.py   # RAG implementation for Physical AI content
│   │   ├── auth_service.py  # Authentication service
│   │   ├── translation_service.py # Translation service for technical content
│   │   ├── personalization_service.py # Personalization based on hardware profiles
│   │   └── content_ingestion_service.py # Service to ingest Physical AI curriculum
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chat.py      # Chat API endpoints with Physical AI content filtering
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── user.py      # User management with hardware profile endpoints
│   │   │   ├── translation.py # Translation endpoints
│   │   │   └── content.py   # Content management endpoints
│   │   └── __init__.py
│   ├── database/
│   │   ├── connection.py    # Database connection
│   │   └── migrations.py    # Database migrations
│   ├── ai/
│   │   ├── embedding_manager.py # Cohere embedding manager for Physical AI content
│   │   └── response_validator.py # Ensures responses stay within Physical AI curriculum
│   └── utils/
│       ├── helpers.py       # Utility functions
│       ├── config.py        # Configuration management
│       └── hardware_profiles.py # Hardware profile definitions and validation
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── docs/
│   ├── intro.md
│   ├── setup-guides/
│   │   ├── digital-twin-workstation.md
│   │   ├── physical-ai-edge-kit.md
│   │   ├── cloud-native-development.md
│   │   ├── jetson-orin-nano-setup.md    # Hardware setup guide
│   │   ├── intel-realsense-setup.md     # Sensor setup guide
│   │   └── respeaker-setup.md           # Audio setup guide
│   ├── module-1-ros2/                   # The Robotic Nervous System
│   │   ├── chapter-1-intro-ros2.md      # ROS 2 Nodes, Topics, and Services
│   │   ├── chapter-2-nodes-topics.md
│   │   ├── chapter-3-services-actions.md
│   │   ├── chapter-4-urdf-modeling.md   # URDF for humanoid robots
│   │   ├── chapter-5-launch-files.md
│   │   └── chapter-6-rclpy-bridge.md    # Bridging Python Agents to ROS controllers
│   ├── module-2-digital-twin/           # The Digital Twin (Gazebo & Unity)
│   │   ├── chapter-1-physics-simulation.md  # Physics, gravity, and collisions in Gazebo
│   │   ├── chapter-2-rendering-unity.md     # High-fidelity rendering and human-robot interaction
│   │   ├── chapter-3-sensor-simulation.md   # LiDAR, Depth Cameras, and IMUs
│   │   └── chapter-4-sim-to-real.md         # Sim-to-real transfer techniques
│   ├── module-3-nvidia-isaac/           # The AI-Robot Brain (NVIDIA Isaac™)
│   │   ├── chapter-1-isaac-sim.md       # Photorealistic simulation and synthetic data generation
│   │   ├── chapter-2-isaac-ros.md       # Hardware-accelerated VSLAM and navigation
│   │   ├── chapter-3-nav2-path-planning.md # Path planning for bipedal humanoid movement
│   │   └── chapter-4-hardware-acceleration.md # GPU-accelerated robotics
│   ├── module-4-vla-humanoids/          # Vision-Language-Action (VLA)
│   │   ├── chapter-1-voice-to-action.md # Using OpenAI Whisper for voice commands
│   │   ├── chapter-2-cognitive-planning.md # LLMs translating natural language to ROS 2 actions
│   │   ├── chapter-3-computer-vision.md   # Object identification and manipulation
│   │   └── chapter-4-capstone-project.md  # Autonomous Humanoid implementation
│   ├── capstone-project/
│   │   ├── project-overview.md          # Robot receives voice command, plans path, navigates obstacles
│   │   ├── implementation-guide.md      # Identifies object using computer vision, manipulates it
│   │   ├── evaluation-criteria.md
│   │   └── showcase-examples.md
│   ├── hardware-guides/
│   │   ├── cloud-vs-onpremise.md        # Cost analysis: Cloud Workstations vs Local Hardware
│   │   ├── aws-g5-setup.md             # AWS g5.2xlarge instance setup
│   │   └── latency-considerations.md    # Cloud vs edge deployment trade-offs
│   ├── references.md
│   └── glossary.md
├── src/
│   ├── components/
│   │   ├── Homepage/
│   │   │   ├── WhyChooseThisBook.js
│   │   │   └── ReadyToBuildFuture.js
│   │   ├── ModuleCards/
│   │   │   └── ModuleCard.js            # Card-based UI for modules
│   │   ├── Chapter/
│   │   │   ├── TranslationButton.js     # Urdu translation button
│   │   │   ├── PersonalizationOptions.js # Hardware-aware content options
│   │   │   └── HardwarePrerequisites.js # Show hardware requirements for chapter
│   │   ├── Chat/
│   │   │   └── ChatbotWidget.js         # Embedded chat widget in book UI
│   │   ├── Capstone/
│   │   │   └── ProjectTracker.js        # Track capstone project progress
│   │   └── User/
│   │       └── HardwareProfileForm.js   # Collect hardware background during registration
│   ├── pages/
│   │   ├── index.js                   # Landing page
│   │   ├── why-choose-book.js         # Why Choose This Book page
│   │   ├── modules.js                 # Modules Page with card-based UI
│   │   ├── ready-to-build-future.js   # Ready to Build the Future page
│   │   └── capstone.js                # Capstone project landing page
│   ├── css/
│   │   └── custom.css
│   └── theme/
│       ├── MDXContent/
│       │   └── Wrapper.js
│       └── CodeBlock/
│           └── HardwareSpecific.js      # Hardware-specific code examples
├── static/
│   └── img/
├── docusaurus.config.js
├── sidebars.js
├── package.json
└── babel.config.js

# Configuration and deployment
.env.example
requirements.txt
pyproject.toml
README.md
```

**Structure Decision**: Selected web application structure with separate frontend (Docusaurus) and backend (FastAPI) to maintain clear separation of concerns. The frontend handles static textbook content and user interface, while the backend manages dynamic features like RAG chatbot, authentication, personalization, and translation.

## Physical AI Implementation Plan

### 1. Project Folder Structure
- Use existing `frontend/` and `backend/` directories
- Add Physical AI-specific content in `frontend/docs/` organized by modules
- Add backend services for hardware profile management and Physical AI content restrictions

### 2. File List with Purpose
**Backend Files:**
- `src/ai/response_validator.py` - Ensures AI responses stay within Physical AI curriculum boundaries
- `src/ai/embedding_manager.py` - Manages Cohere embeddings for Physical AI content
- `src/utils/hardware_profiles.py` - Defines hardware profile types and validation rules
- `src/services/content_ingestion_service.py` - Ingests Physical AI curriculum content from various sources
- `src/services/personalization_service.py` - Delivers hardware-aware content personalization

**Frontend Components:**
- `src/components/Chapter/HardwarePrerequisites.js` - Shows hardware requirements for each chapter
- `src/components/User/HardwareProfileForm.js` - Collects user's hardware background during registration
- `src/components/Capstone/ProjectTracker.js` - Tracks capstone project progress
- `src/components/ModuleCards/ModuleCard.js` - Card-based UI for Physical AI modules
- `src/theme/CodeBlock/HardwareSpecific.js` - Shows hardware-specific code examples

### 3. Module-specific Content Outline
**Module 1: The Robotic Nervous System (ROS 2)**
- Chapter 1: Introduction to ROS 2 concepts
- Chapter 2: ROS 2 Nodes, Topics, and Services
- Chapter 3: Actions and Parameters
- Chapter 4: URDF for Humanoid Robots
- Chapter 5: Launch Files and Package Management
- Chapter 6: Bridging Python Agents to ROS Controllers using rclpy

**Module 2: The Digital Twin (Gazebo & Unity)**
- Chapter 1: Physics Simulation in Gazebo (gravity, collisions)
- Chapter 2: High-fidelity Rendering in Unity
- Chapter 3: Sensor Simulation (LiDAR, Depth Cameras, IMUs)
- Chapter 4: Sim-to-Real Transfer Techniques

**Module 3: The AI-Robot Brain (NVIDIA Isaac™)**
- Chapter 1: NVIDIA Isaac Sim (photorealistic simulation, synthetic data)
- Chapter 2: Isaac ROS (hardware-accelerated VSLAM)
- Chapter 3: Nav2 for Bipedal Humanoid Movement
- Chapter 4: Hardware Acceleration Techniques

**Module 4: Vision-Language-Action (VLA)**
- Chapter 1: Voice-to-Action with OpenAI Whisper
- Chapter 2: Cognitive Planning with LLMs
- Chapter 3: Computer Vision for Object Manipulation
- Chapter 4: Capstone Project Implementation

### 4. RAG Chatbot Setup & DB Connections
- **Neon Postgres**: Store user profiles including hardware configurations and learning progress
- **Qdrant**: Store vector embeddings of Physical AI curriculum content (ROS 2, simulation, NVIDIA Isaac, VLA)
- **Content Restriction**: Implement response validator to ensure AI only responds to Physical AI curriculum
- **Hardware-Aware Responses**: Personalization service provides context based on user's hardware profile

### 5. User Personalization Flow
- **Registration**: Collect hardware profile (Jetson kit, sensors, experience level)
- **Content Adaptation**: Show relevant examples based on user's hardware setup
- **Path Guidance**: Recommend learning path based on hardware capabilities
- **Project Suggestions**: Suggest projects appropriate for user's hardware configuration

### 6. Urdu Translation Implementation
- **Chapter-level Integration**: Translation button on each chapter page
- **Technical Terminology**: Special handling for robotics-specific terms
- **Caching**: Cache translated content for performance
- **Backend API**: `/api/v1/translate` endpoint with content ID and target language parameters

### 7. Capstone Project Plan
- **Project Overview**: Autonomous humanoid receives voice command, plans path, navigates obstacles
- **Implementation Guide**: Identifies object using computer vision, manipulates it
- **Progress Tracking**: Frontend component to track project milestones
- **Evaluation Criteria**: Rubric for project assessment

### 8. Deployment Steps
- **Frontend**: Deploy to GitHub Pages via GitHub Actions
- **Backend**: Deploy to cloud platform (Railway, Heroku, or similar) with environment configuration
- **MCP Integration**: Connect to Docusaurus documentation and GitHub Pages automation
- **Database Setup**: Initialize Neon Postgres and Qdrant with Physical AI curriculum

### 9. Optional Bonus Features (Claude Code Subagents/Agent Skills)
- **Subagent System**: Reusable intelligence for common robotics queries
- **Agent Skills**: Module-specific skills for ROS 2, simulation, Isaac, and VLA concepts
- **Content Generation**: Subagents to help generate new robotics examples and exercises
- **Code Assistance**: Skills to help students debug ROS 2 and robotics code

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple repositories (frontend/backend) | Clear separation of static vs dynamic content | Mixing would create deployment complexity and security issues |
| Multiple database systems (Postgres + Qdrant) | Need for both structured user data and vector search | Single system insufficient for both relational and vector operations |
| Hardware profile complexity | Required for Physical AI curriculum personalization | Would limit effectiveness of personalized learning experience |