<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.0.0 (initial creation)
Modified principles: N/A (first version)
Added sections: All sections (initial creation)
Removed sections: N/A
Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Updated to align with principles
- ✅ .specify/templates/spec-template.md - Updated to align with principles
- ✅ .specify/templates/tasks-template.md - Updated to align with principles
- ✅ .specify/templates/commands/*.md - Verified no outdated references
- ⚠️ README.md - May need updates to reflect new constitution (pending)
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Minimalist Architecture
Every component must serve a specific, essential purpose; avoid feature creep and unnecessary complexity; only essential files and dependencies allowed with clear justification required for additions.

### II. Deterministic Workflows
All development workflows must be step-by-step, repeatable, and deterministic; processes must be documented and consistently executable; version control required for all changes.

### III. Single-Source-of-Truth (NON-NEGOTIABLE)
The textbook content serves as the definitive source for all information; chatbot responses must derive solely from book content; content consistency across all platforms maintained.

### IV. Production-Ready Code
All code must meet production standards from inception; comprehensive error handling, security considerations, and performance optimization required; testing and validation mandatory before deployment.

### V. Modular Component Design
System components must be modular and loosely coupled; each module should have clear interfaces and responsibilities; reusability and maintainability prioritized in all implementations.

### VI. Environment-Based Configuration
All API keys and sensitive configurations must be environment-based; no hardcoded credentials allowed; secure handling of all sensitive data required across all components.

## Additional Constraints

Technology Stack Requirements:
- Frontend: Docusaurus for textbook generation and documentation
- Backend: FastAPI for API services
- Database: Neon Postgres for data storage
- Vector Storage: Qdrant for RAG implementation
- Authentication: Better-Auth for user management
- Deployment: GitHub Pages for static content, MCP for automated deployment

Performance Standards:
- API response times under 2 seconds
- Page load times under 3 seconds
- Chatbot response times under 5 seconds
- System must handle concurrent users appropriately

Security Requirements:
- All user data encrypted in transit and at rest
- Authentication required for personalized features
- Rate limiting implemented on all public endpoints
- Input validation on all user-facing interfaces

## Development Workflow

Task-Based Development:
- Project divided into 7 sequential tasks with specific deliverables
- Each task must be completed and validated before proceeding
- Task 1: Book structure, landing pages, chapters, module cards
- Task 2: Backend implementation (RAG chatbot + APIs)
- Task 3: Base functionality (100 pts)
- Task 4: Reusable Intelligence (50 pts bonus)
- Task 5: Better-auth Signup/Signin + personalization (50 pts bonus)
- Task 6: Personalized content features (50 pts bonus)
- Task 7: Urdu translation capability (50 pts bonus)

Quality Gates:
- All code must include explanatory comments
- File count kept minimal with only essential files
- All modules must link correctly to chapter pages
- UI must include required pages: landing, "Why Choose This Book?", module cards, "Ready to Build the Future?"

Review Process:
- All PRs must verify constitution compliance
- Architecture reviews required for significant changes
- User experience validation for all UI components
- Security review for authentication and data handling

## Governance

This constitution supersedes all other development practices; all team members must comply with these principles; amendments require formal documentation and approval process; all implementations must align with stated philosophy of clean, minimal, well-documented architecture.

All PRs and code reviews must verify compliance with constitutional principles; complexity must be justified with clear benefits; use this constitution document as the primary runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12