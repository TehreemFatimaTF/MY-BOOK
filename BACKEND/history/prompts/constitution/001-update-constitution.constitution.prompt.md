---
id: 001
title: Update Constitution
stage: constitution
date: 2025-12-24
surface: agent
model: Qwen
feature: none
branch: 001-book-rag-chatbot
user: user
command: /sp.constitution
labels: [constitution,rag,chatbot,book-interaction]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: sp.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

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


/sp.constitution Project: Integrated RAG Chatbot Development for Embedded Book Interaction
Core principles:
- Accuracy in responses by strictly grounding answers in book content or user-selected text
- Efficiency using free-tier services and optimized APIs for low latency and cost
- User-centric design for seamless embedding and intuitive interactions within the book
- Modularity for easy maintenance and scalability (e.g., swapping AI providers if needed)
Key standards:
- All responses must be generated using Cohere API (no OpenAI); integrate via official SDK
- Retrieval must use Qdrant for vector search; database operations via Neon Postgres for metadata
- Backend built with FastAPI; development workflow incorporating SpecifyKit Plus for prompt specification and Qwen CLI for local testing
- Handle user-selected text by dynamically scoping retrieval to selections only
- Security: API keys stored securely (e.g., environment variables); no storage of user data beyond sessions
- Code quality: PEP 8 compliant Python; include docstrings and comments for all functions
- Testing: Minimum 80% unit test coverage; integration tests for RAG pipeline
Constraints:
- API usage: Cohere API key only; adhere to free-tier limits for Qdrant and Neon
- Book embedding: Compatible with digital formats (e.g., HTML/PDF with JS); no native app development
- Development tools: Must use SpecifyKit Plus or Qwen CLI for prototyping and refinement
- Timeline: Assume iterative development; no strict deadline but aim for MVP in 2-4 weeks
- Budget: Zero-cost beyond free tiers; no paid upgrades
Success criteria:
- Chatbot accurately answers 95% of book-related queries in tests (evaluated via manual review or benchmarks)
- Supports user-selected text mode without hallucinations (responses limited to provided context)
- Successfully embedded in a sample published book (e.g., demo e-book) with functional interactions
- Passes code review for quality, security, and efficiency
- Zero critical bugs in deployment; positive feedback on "boht hi acha or behtreen" usability

## Response snapshot

I have successfully updated the project constitution for the Integrated RAG Chatbot Development project. Here's what was accomplished:

1. Updated the constitution file at `.specify/memory/constitution.md` with the specific project details:
   - Project name: Integrated RAG Chatbot Development for Embedded Book Interaction
   - Core principles: Accuracy in Responses, Efficiency and Cost Optimization, User-Centric Design, Modularity and Scalability, Security and Data Protection, Code Quality and Testing Standards
   - Added sections for Key Standards, Development Workflow, and Success Criteria

2. Applied the Sync Impact Report as an HTML comment at the top of the constitution file, documenting:
   - Version change from 1.0.0 to 1.1.0
   - Modified principles with their new titles
   - Added sections: Key Standards, Development Workflow, Success Criteria
   - Templates requiring updates (with pending status)

3. The constitution now reflects the specific requirements provided by the user:
   - Accuracy in responses by grounding answers in book content
   - Efficiency using free-tier services
   - User-centric design for seamless embedding
   - Modularity for easy maintenance
   - Using Cohere API, Qdrant for retrieval, Neon Postgres for metadata
   - Backend built with FastAPI
   - Security requirements for API keys
   - Code quality standards (PEP 8, docstrings)
   - Testing requirements (80% coverage)

The updated constitution follows all specified formatting requirements and is ready for use in the project.

## Outcome

- ✅ Impact: Updated constitution with project-specific principles and requirements
- 🧪 Tests: No tests required for constitution update
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: /sp.specify to implement feature specification based on updated constitution
- 🧠 Reflection: Constitution now properly reflects the RAG chatbot project requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on updated constitution