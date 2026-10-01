# Project Rules

Repository-specific engineering rules and constraints governing human and
AI-assisted development.

## Core Principles

- Adhere to existing patterns and conventions found in this repository.
- Avoid introducing speculative dependencies or unapproved architecture.
- Keep modifications minimal, reviewable, and focused on the requested task.
- Treat unknown requirements or ambiguous designs explicitly rather than guessing.

## Coding Conventions

<!-- Observable coding conventions, style rules, and language standards. -->

## Architecture & Boundaries

<!-- Module boundaries, dependency flow rules, and forbidden patterns. -->

## Testing Expectations

<!-- Test frameworks used, coverage or test-writing rules, and required checks. -->

## Security & Privacy Rules

<!-- Sensitive areas, secret handling rules, input validation requirements. -->

## AI Operating Invariants

- Inspect relevant `.aicf/` context files (`rules.md`, `project.md`) before planning.
- If a requested task conflicts with any rule in this document, surface the conflict.
- Do not commit changes automatically without human review.
- Never write credentials, tokens, or absolute workstation paths into this repository.
