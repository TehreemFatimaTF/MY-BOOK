---
id: 003
title: Create Implementation Plan
stage: plan
date: 2025-12-24
surface: agent
model: Qwen
feature: book-rag-chatbot
branch: 001-book-rag-chatbot
user: user
command: /sp.plan
labels: [plan,rag,chatbot,book-interaction,architecture]
links:
  spec: specs/001-book-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-book-rag-chatbot/plan.md
  - specs/001-book-rag-chatbot/research.md
  - specs/001-book-rag-chatbot/data-model.md
  - specs/001-book-rag-chatbot/quickstart.md
  - specs/001-book-rag-chatbot/contracts/api-contracts.md
tests:
  - none
---

## Prompt

---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: sp.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: sp.checklist
    prompt: Create a checklist for the following domain...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType qwen`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.plan
Create: high-level system architecture diagram, data ingestion pipeline, FastAPI backend endpoints, Qdrant collection setup script, Neon Postgres schema, book embedding integration (e.g., JS widget), test suites for RAG accuracy and selected-text mode, deployment guide for demo e-book.
Decisions needing documentation:

Cohere model selection (e.g., command-r-plus vs embed-english-v3.0; tradeoffs: accuracy vs latency/cost on free tier)
Chunking strategy for book content (e.g., sentence-level vs paragraph-level; tradeoffs: retrieval precision vs embedding overhead)
Selected-text handling approach (e.g., on-the-fly embedding vs pre-indexed subsets; tradeoffs: flexibility vs performance)
Error handling mechanisms (e.g., fallback to default context vs user notification; tradeoffs: user experience vs system complexity)
Testing strategy:
Unit tests for individual components (e.g., embedding generation, vector search) aiming for 80% coverage
Integration tests for end-to-end RAG flow using sample queries and mock book data
Accuracy benchmarks: Manual review of 50+ test queries against success criteria (95% accuracy, no hallucinations in selected-text mode)
Security audits: Check for API key exposure and data leakage
Usability testing: Deploy in demo book and gather feedback on latency (<3s) and intuitiveness
Technical details:
Follow iterative development: Start with MVP (basic RAG without selected-text), then add features
Use SpecifyKit Plus for prompt engineering in Cohere integrations; Qwen CLI for offline prototyping of generation logic
Organize by phases: Setup (environment and credentials) → Data Ingestion (book parsing and Qdrant/Neon setup) → Backend Development (FastAPI endpoints) → Frontend Embedding (book integration) → Testing & Refinement → Deployment (demo e-book publish)
Securely handle credentials: Use environment variables for all keys (Cohere, Qdrant, Neon, etc.) as per provided dotenv
Adhere to PEP 8 and include comprehensive docstrings; aim for modularity to allow AI provider swaps

## Response snapshot

I have successfully completed the implementation planning for the Book RAG Chatbot feature. Here's what was accomplished:

1. Created the implementation plan (plan.md) with:
   - Technical context including language, dependencies, and platform
   - Constitution check ensuring alignment with project principles
   - Project structure for both documentation and source code

2. Created the research document (research.md) with:
   - Key technology decisions for Cohere model selection
   - Chunking strategy for book content
   - Selected-text handling approach
   - Error handling mechanisms
   - Best practices for technology integration

3. Created the data model document (data-model.md) with:
   - Detailed entities: Book Content, User Query, Retrieved Context, Generated Response, User Selection, and Query History
   - Attributes, relationships, and validation rules for each entity
   - State transitions for query processing flow

4. Created the quickstart guide (quickstart.md) with:
   - Setup instructions and prerequisites
   - Configuration steps with environment variables
   - Basic usage examples for querying book content
   - Development workflow guidance

5. Created the API contracts document (contracts/api-contracts.md) with:
   - Detailed endpoint specifications for book management, query processing, history, and health checks
   - Request/response formats for each endpoint
   - Error handling and authentication requirements

The implementation plan aligns with the project constitution principles of accuracy, efficiency, user-centric design, modularity, security, and code quality. All artifacts are ready for the next phase of development.

## Outcome

- ✅ Impact: Comprehensive planning artifacts created for Book RAG Chatbot implementation
- 🧪 Tests: Testing strategy documented in research file
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, and contracts/api-contracts.md created
- 🔁 Next prompts: /sp.tasks to break the plan into implementation tasks
- 🧠 Reflection: Planning phase complete with all necessary design artifacts created

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task breakdown with /sp.tasks