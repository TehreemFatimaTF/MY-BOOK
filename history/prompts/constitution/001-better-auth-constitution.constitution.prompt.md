---
id: 001
title: "Better Auth Constitution"
stage: "constitution"
date_iso: "2025-12-31"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "001-book-rag-chatbot"
user: "user"
command: "/sp.constitution"
labels: ["authentication", "better-auth", "security", "user-profile"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Better Auth Constitution

## User Input (PROMPT_TEXT)
```
/sp.constitution
Project: Implement Signup and Signin with Better Auth for bonus points
Core principles:

Security first: Use secure practices for authentication, password handling, and sessions
Comprehensive implementation: Full signup and signin flows with email/password (and optionally OAuth if feasible)
User profiling: Collect software and hardware background during signup for content personalization
Best practices: Follow Better Auth documentation, TypeScript type safety, and modern web standards (likely Next.js)
Clean and maintainable code: Well-structured, commented, and error-handled

Key standards:

Use https://www.better-auth.com/ for authentication setup
Implement custom fields or multi-step signup to ask questions about user's software (e.g., programming languages, frameworks experience) and hardware background (e.g., GPU, CPU, devices)
Store background information in user profile (extend Drizzle schema if needed) for future personalization
Secure session management and proper redirects after signin/signup
Responsive and user-friendly UI for auth forms

Constraints:

Must integrate Better Auth correctly with database (e.g., Drizzle ORM)
Signup flow must include questions beyond basic email/password/name
No hard-coded secrets; use environment variables
Compatible with framework (e.g., Next.js App Router)

Success criteria:

Working signup: User can register, answers background questions, data saved correctly
Working signin: User can login and access protected routes
Bonus points eligible: Full implementation as described in task
No vulnerabilities in auth flow
Code is production-ready quality
```

## Assistant Response (RESPONSE_TEXT)
```
Created and updated the project constitution to include Better Auth implementation details. Added a new core principle "Security-First Authentication", updated technology stack requirements to include user profiling, and added detailed security and user profiling requirements to ensure proper implementation of the authentication system with user background collection.
```

## Outcome
Successfully updated the project constitution to include requirements for Better Auth implementation with user profiling capabilities. The constitution now includes specific security requirements, user profiling requirements, and technology stack updates to support the signup/signin feature with background question collection.

## Evaluation
The constitution has been properly updated to reflect the requirements for implementing Better Auth with user profiling. All security and user experience requirements are documented and aligned with the project goals.