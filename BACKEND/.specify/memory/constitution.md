<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles:
  - PRINCIPLE_1_NAME: Accuracy in Responses
  - PRINCIPLE_2_NAME: Efficiency and Cost Optimization
  - PRINCIPLE_3_NAME: User-Centric Design
  - PRINCIPLE_4_NAME: Modularity and Scalability
  - PRINCIPLE_5_NAME: Security and Data Protection
  - PRINCIPLE_6_NAME: Code Quality and Testing Standards
- Added sections: Key Standards, Development Workflow, Success Criteria
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/*.md: ⚠ pending
- Follow-up TODOs: None
-->
# Integrated RAG Chatbot Development Constitution

## Core Principles

### I. Accuracy in Responses
All responses must be strictly grounded in book content or user-selected text. The system must avoid hallucinations and ensure factual accuracy by referencing specific passages from the source material.

### II. Efficiency and Cost Optimization
Use free-tier services and optimized APIs for low latency and cost. The system must adhere to free-tier limits for Qdrant and Neon, while maintaining performance standards.

### III. User-Centric Design
Design for seamless embedding and intuitive interactions within the book. The interface must be intuitive and enhance the reading experience without disruption.

### IV. Modularity and Scalability
Build with modular components that allow for easy maintenance and scalability. The system must support swapping AI providers if needed and be easily extensible.

### V. Security and Data Protection
Ensure secure handling of API keys (stored in environment variables) and no storage of user data beyond sessions. All data transmission must be secure.

### VI. Code Quality and Testing Standards
Maintain PEP 8 compliant Python code with comprehensive documentation. Implement minimum 80% unit test coverage and integration tests for the RAG pipeline.

## Key Standards

- All responses must be generated using Cohere API (no OpenAI); integrate via official SDK
- Retrieval must use Qdrant for vector search; database operations via Neon Postgres for metadata
- Backend built with FastAPI; development workflow incorporating SpecifyKit Plus for prompt specification and Qwen CLI for local testing
- Handle user-selected text by dynamically scoping retrieval to selections only
- API keys stored securely (e.g., environment variables); no storage of user data beyond sessions
- Code quality: PEP 8 compliant Python; include docstrings and comments for all functions
- Testing: Minimum 80% unit test coverage; integration tests for RAG pipeline

## Development Workflow

- Development tools: Must use SpecifyKit Plus or Qwen CLI for prototyping and refinement
- Timeline: Assume iterative development; no strict deadline but aim for MVP in 2-4 weeks
- Budget: Zero-cost beyond free tiers; no paid upgrades
- Book embedding: Compatible with digital formats (e.g., HTML/PDF with JS); no native app development
- API usage: Cohere API key only; adhere to free-tier limits for Qdrant and Neon

## Success Criteria

- Chatbot accurately answers 95% of book-related queries in tests (evaluated via manual review or benchmarks)
- Supports user-selected text mode without hallucinations (responses limited to provided context)
- Successfully embedded in a sample published book (e.g., demo e-book) with functional interactions
- Passes code review for quality, security, and efficiency
- Zero critical bugs in deployment; positive feedback on "boht hi acha or behtreen" usability

## Governance

This constitution supersedes all other practices in the project. All development, testing, and deployment activities must comply with these principles. Amendments require documentation, approval from project stakeholders, and a migration plan if applicable. All PRs/reviews must verify compliance with these principles and standards.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-12-24
