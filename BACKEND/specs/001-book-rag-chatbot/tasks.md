---

description: "Task list for Book RAG Chatbot feature implementation"
---

# Tasks: Book RAG Chatbot

**Input**: Design documents from `/specs/001-book-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included based on requirements for 80%+ test coverage and integration testing.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `backend/tests/`
- All paths follow the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/
- [X] T002 Initialize Python 3.11 project with FastAPI, Cohere SDK, Qdrant client, Neon Postgres driver, Pydantic dependencies in backend/
- [X] T003 [P] Configure linting (flake8, black) and formatting tools in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework for Neon Postgres in backend/src/db/migrations/
- [X] T005 [P] Setup Qdrant collection for vector storage with appropriate dimensions for Cohere embeddings in backend/src/db/qdrant_setup.py
- [X] T006 [P] Setup environment configuration management with secure API key handling in backend/src/config/
- [X] T007 Create base models/entities that all stories depend on in backend/src/models/
- [X] T008 Configure error handling and logging infrastructure in backend/src/utils/logging.py
- [X] T009 Setup API routing and middleware structure in backend/src/api/main.py
- [X] T010 [P] Implement API key authentication middleware in backend/src/middleware/auth.py
- [X] T011 Setup connection pooling for Neon Postgres in backend/src/db/postgres_client.py
- [X] T012 Create embedding utility functions for Cohere integration in backend/src/utils/embedding_utils.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Query Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable users to ask questions about book content and receive accurate answers based on the book's text

**Independent Test**: Can be fully tested by loading book content into the system, asking specific questions about the content, and verifying that responses are accurate and based on the provided text.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Contract test for POST /query endpoint in backend/tests/contract/test_query_endpoint.py
- [X] T014 [P] [US1] Integration test for RAG flow with book content in backend/tests/integration/test_rag_flow.py
- [X] T015 [P] [US1] Unit test for Cohere service integration in backend/tests/unit/test_cohere_service.py
- [X] T016 [US1] Accuracy benchmark test with 50+ sample queries in backend/tests/accuracy/test_accuracy.py

### Implementation for User Story 1

- [X] T017 [P] [US1] Create BookContent model in backend/src/models/book_content.py
- [X] T018 [P] [US1] Create UserQuery model in backend/src/models/user_query.py
- [X] T019 [P] [US1] Create RetrievedContext model in backend/src/models/retrieved_context.py
- [X] T020 [P] [US1] Create GeneratedResponse model in backend/src/models/generated_response.py
- [X] T021 [US1] Implement BookContentService in backend/src/services/book_content_service.py
- [X] T022 [US1] Implement CohereService for text generation in backend/src/services/cohere_service.py
- [X] T023 [US1] Implement QdrantService for vector search in backend/src/services/qdrant_service.py
- [X] T024 [US1] Implement PostgresService for metadata storage in backend/src/services/postgres_service.py
- [X] T025 [US1] Implement RAGService orchestrating the RAG flow in backend/src/services/rag_service.py
- [X] T026 [US1] Implement book management endpoints (POST /books, GET /books, GET /books/{book_id}) in backend/src/api/book_routes.py
- [X] T027 [US1] Implement query endpoint (POST /query) in backend/src/api/query_routes.py
- [X] T028 [US1] Add validation and error handling for book content queries in backend/src/api/query_routes.py
- [X] T029 [US1] Add logging for user story 1 operations in backend/src/utils/logging.py
- [X] T030 [US1] Implement paragraph-level text chunking with overlap in backend/src/utils/text_chunker.py
- [X] T031 [US1] Implement book ingestion pipeline to process and index content in backend/src/pipeline/book_ingestion.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Query User-Selected Text (Priority: P2)

**Goal**: Allow users to select specific text within the book and ask questions about only that selected text

**Independent Test**: Can be tested by allowing users to select text, asking questions about the selection, and ensuring responses are limited to the selected content without external context leakage.

### Tests for User Story 2 ⚠️

- [ ] T032 [P] [US2] Contract test for POST /query with selected_text parameter in backend/tests/contract/test_selected_text_query.py
- [ ] T033 [P] [US2] Integration test for selected-text mode without external context leakage in backend/tests/integration/test_selected_text_mode.py
- [ ] T034 [US2] Unit test for selected-text handling logic in backend/tests/unit/test_selected_text.py

### Implementation for User Story 2

- [X] T035 [P] [US2] Create UserSelection model in backend/src/models/user_selection.py
- [X] T036 [US2] Enhance RAGService to support selected-text queries in backend/src/services/rag_service.py
- [X] T037 [US2] Implement on-the-fly embedding for selected text with caching in backend/src/services/cohere_service.py
- [X] T038 [US2] Update query endpoint to handle selected_text parameter in backend/src/api/query_routes.py
- [X] T039 [US2] Add validation to ensure selected text is part of the referenced book content in backend/src/api/query_routes.py
- [X] T040 [US2] Implement hallucination prevention for selected-text mode in backend/src/services/rag_service.py
- [X] T041 [US2] Add logging for selected-text operations in backend/src/utils/logging.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Seamless Book Integration (Priority: P3)

**Goal**: Embed the chatbot interface seamlessly in book format (HTML/JS) so users can interact without leaving the reading experience

**Independent Test**: Can be tested by embedding the chatbot in a digital book format and verifying that users can access and use it without disrupting the reading experience.

### Tests for User Story 3 ⚠️

- [ ] T042 [P] [US3] Contract test for frontend integration endpoints in backend/tests/contract/test_frontend_integration.py
- [ ] T043 [P] [US3] Integration test for HTML/JS widget functionality in backend/tests/integration/test_frontend_widget.py
- [ ] T044 [US3] Performance test for response time under 3 seconds in backend/tests/performance/test_response_time.py

### Implementation for User Story 3

- [X] T045 [P] [US3] Create QueryHistory model in backend/src/models/query_history.py
- [X] T046 [US3] Implement query history endpoints (GET /history) in backend/src/api/history_routes.py
- [X] T047 [US3] Implement feedback endpoint (POST /history/{query_id}/feedback) in backend/src/api/history_routes.py
- [X] T048 [US3] Implement health check endpoint (GET /health) in backend/src/api/health_routes.py
- [X] T049 [US3] Create JavaScript widget for book integration in backend/src/frontend/chat_widget.js
- [X] T050 [US3] Create HTML/CSS components for chat interface in backend/src/frontend/chat_widget.css
- [X] T051 [US3] Implement streaming response endpoint (POST /query/stream) in backend/src/api/query_routes.py
- [X] T052 [US3] Add CORS support for frontend integration in backend/src/api/main.py
- [X] T053 [US3] Add latency monitoring and performance optimization in backend/src/utils/performance.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T054 [P] Documentation updates based on quickstart.md in backend/docs/
- [ ] T055 Code cleanup and refactoring across all modules
- [ ] T056 Performance optimization across all stories to ensure <3s response time
- [ ] T057 [P] Additional unit tests to achieve 80%+ coverage in backend/tests/unit/
- [X] T058 Security hardening including API key validation and rate limiting
- [X] T059 Run quickstart.md validation and update any discrepancies
- [X] T060 Implement comprehensive error handling and graceful degradation as per research.md
- [X] T061 Add comprehensive logging for observability as per constitution requirements
- [X] T062 Create demo book integration example in backend/demo/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 models and services
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1/US2 components

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for POST /query endpoint in backend/tests/contract/test_query_endpoint.py"
Task: "Integration test for RAG flow with book content in backend/tests/integration/test_rag_flow.py"

# Launch all models for User Story 1 together:
Task: "Create BookContent model in backend/src/models/book_content.py"
Task: "Create UserQuery model in backend/src/models/user_query.py"
Task: "Create RetrievedContext model in backend/src/models/retrieved_context.py"
Task: "Create GeneratedResponse model in backend/src/models/generated_response.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence