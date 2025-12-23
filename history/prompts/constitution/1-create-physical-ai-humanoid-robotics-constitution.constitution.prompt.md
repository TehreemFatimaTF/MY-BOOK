---
id: 1
title: Create-Physical-AI-Humanoid-Robotics-Constitution
stage: constitution
date: 2025-12-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, physical-ai, humanoid-robotics, textbook]
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

Title: Physical AI & Humanoid Robotics Textbook Project Constitution

Purpose:
This constitution establishes the rules, goals, workflows, constraints, and standards for building the Hackathon I project: "Physical AI & Humanoid Robotics Textbook" using Spec-Kit Plus + Claude Code.

Core Deliverables:
1. Create a full textbook using Docusaurus.
2. Deploy the book on GitHub Pages.
3. Build an integrated RAG Chatbot (FastAPI + Qdrant + Neon Postgres + OpenAI Agents).
4. Add reusable intelligence via Claude Code Subagents and Skills.
5. Implement Better-Auth signup/signin with user background questions.
6. Implement per-user personalized content.
7. Implement Urdu translation button per chapter.
8. Ensure all code files include comments explaining their purpose.
9. Keep file count minimal — only essential files.
10. Connect two MCPs: context7 for Docusaurus docs + GitHub MCP for deployment.

Overall Workflow:
The project must be created in 7 tasks:
Task 1: Build book, folder structure, landing pages, chapters, cards for module chapters.
Task 2: Build backend (RAG chatbot + required APIs).
Task 3: Base functionality (100 pts).
Task 4: Reusable Intelligence (50 pts bonus).
Task 5: Better-auth Signup/Signin + personalization (50 pts bonus).
Task 6: Personalized content button per chapter (50 pts bonus).
Task 7: Translation to Urdu button per chapter (50 pts bonus).

Project Philosophy:
- Architecture must be clean, minimal, and well-documented.
- Avoid unnecessary files; only required components allowed.
- Each module must link correctly to chapter pages.
- All code must be production-ready.
- The chatbot must respond ONLY using book content.
- UI must include landing page, "Why Choose This Book?" page, Module cards page, and "Ready to Build the Future?" section.
- GitHub deployment must be configured using provided MCP.

Strict Rules:
- No extra dependencies unless necessary.
- Textbook content must follow the course outline exactly.
- All workflows must be deterministic, step-by-step, repeatable.
- The system must treat the textbook as the single-source-of-truth.
- Subagents must be used only where beneficial.
- API keys must be environment-based.
- Avoid large unstructured files.

Definition of Done:
The project is considered complete when:
- Book is built, deployed, and browsable.
- Backend chatbot is functional with retrieval.
- Better-auth login works.
- Personalization works.
- Urdu translation button works.
- GitHub deployment works.
- All tasks executed in correct sequence and validated.

## Response snapshot

Created the Physical AI & Humanoid Robotics Textbook Constitution with the following elements:

Core Principles:
1. Minimalist Architecture - Components must serve essential purposes with no unnecessary complexity
2. Deterministic Workflows - Step-by-step, repeatable processes with version control
3. Single-Source-of-Truth - Textbook content as definitive source for all information
4. Production-Ready Code - Code must meet production standards with proper error handling
5. Modular Component Design - Components must be modular and loosely coupled
6. Environment-Based Configuration - All sensitive configs must be environment-based

Additional Constraints:
- Technology stack requirements (Docusaurus, FastAPI, Neon Postgres, Qdrant, Better-Auth)
- Performance standards (response times, load times)
- Security requirements (encryption, rate limiting, input validation)

Development Workflow:
- 7-task development process with specific deliverables
- Quality gates and review processes
- Compliance verification requirements

Governance:
- Constitution supersedes all other practices
- Amendment procedures and compliance verification

## Outcome

- ✅ Impact: Created foundational constitution document that defines project principles and governance
- 🧪 Tests: Not applicable for constitution creation
- 📁 Files: Modified .specify/memory/constitution.md with comprehensive constitution
- 🔁 Next prompts: Proceed with project planning and implementation phases
- 🧠 Reflection: Constitution provides clear framework for all subsequent development activities

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution properly created with all required elements
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin with Task 1 - Building book structure and landing pages