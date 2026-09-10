# AICF Canonical Artifact Schemas

## 1. Purpose

This specification defines the canonical Markdown structure for the foundational AICF artifacts.

The schemas provide:

* predictable structure
* machine-readable organization
* human readability
* consistent terminology
* traceability
* context retrieval
* project recovery

The schemas are intentionally lightweight.

> **A field should exist only when it provides persistent engineering value.**

---

# 2. Schema Design Rules

## 2.1 Markdown First

AICF artifacts use Markdown as the canonical representation.

The format should remain:

* portable
* human-readable
* version-control friendly
* tool independent
* easy for AI agents to parse

---

## 2.2 Stable Structure

The major headings of an artifact should remain predictable.

Projects may add project-specific sections where necessary, but should avoid arbitrary restructuring.

---

## 2.3 Required vs Optional

Every schema distinguishes between:

**Required**

Information necessary for the artifact to fulfil its purpose.

**Optional**

Information that may improve usefulness but is not universally necessary.

A small project should be able to use AICF without populating large amounts of metadata.

---

## 2.4 References

Artifacts should reference related artifacts using stable IDs rather than relying only on filenames.

Example:

```text
REQ-004
TASK-012
DEC-007
VAL-018
```

This allows files to be renamed without destroying conceptual relationships.

---

# 3. `rules.md`

## 3.1 Schema

```markdown
# AICF Project Rules

## Purpose

<!-- Short description of the project's engineering rules -->

## Engineering Principles

- ...

## Architecture Rules

- ...

## Coding Rules

- ...

## Testing Rules

- ...

## Security Rules

- ...

## Dependency Rules

- ...

## AI Operating Rules

- ...

## Protected Areas

- ...

## Required Validation

- ...

## Exceptions

- ...
```

---

## 3.2 Required Sections

### Purpose

Briefly describe what the rules govern.

### Engineering Principles

Stable engineering expectations.

### Architecture Rules

Important architectural constraints.

### AI Operating Rules

Rules specifically affecting AI-assisted engineering.

### Protected Areas

Areas requiring additional authority or validation.

---

## 3.3 Optional Sections

* Coding Rules
* Testing Rules
* Security Rules
* Dependency Rules
* Required Validation
* Exceptions

These should be included only where relevant.

---

# 4. `project.md`

## 4.1 Schema

```markdown
# Project

## Identity

**Name:** ...
**Purpose:** ...

## Product / System

### Users

- ...

### Capabilities

- ...

### Terminology

- ...

## Technology

**Language:** ...
**Framework:** ...
**Database:** ...
**Infrastructure:** ...

## Architecture

### Overview

...

### Major Components

- ...

### Repository Structure

- ...

## External Systems

- ...

## Constraints

- ...

## Non-Functional Requirements

- ...

## Related Decisions

- DEC-...
```

---

## 4.2 Required Sections

### Identity

Defines project name and purpose.

### Product / System

Provides enough business/system context to understand the project.

### Technology

Defines the major technical stack.

### Architecture

Provides high-level architecture.

### Constraints

Defines important limitations.

---

## 4.3 Optional Sections

* Users
* Capabilities
* Terminology
* Repository Structure
* External Systems
* Non-Functional Requirements
* Related Decisions

---

## 4.4 Design Rule

`project.md` should remain relatively stable.

If a section changes frequently, it probably belongs somewhere else.

---

# 5. `state.md`

## 5.1 Schema

```markdown
# Project State

## Current Objective

...

## Current Milestone

...

## Active Work

- TASK-...

## Recently Completed

- TASK-...

## Known Issues

- ...

## Open Unknowns

- ...

## Open Decisions

- DEC-...

## Validation Status

- ...

## Blocked Work

- ...

## Recent Material Changes

- ...

## Next Actions

1. ...
2. ...
3. ...
```

---

# 5.2 Required Sections

### Current Objective

The most important current project objective.

### Active Work

Tasks currently in progress.

### Known Issues

Material unresolved problems.

### Open Unknowns

Material unanswered questions.

### Next Actions

What should happen next.

---

## 5.3 Optional Sections

* Current Milestone
* Recently Completed
* Open Decisions
* Validation Status
* Blocked Work
* Recent Material Changes

---

# 5.4 State Update Rule

`state.md` should describe **current project truth**, not every event.

Bad:

```text
Monday:
AI changed service.

Tuesday:
AI ran tests.

Wednesday:
AI changed service again.
```

Good:

```text
Authentication migration is in progress.

Current stage:
Token compatibility layer.

Known issue:
Legacy refresh tokens fail for migrated accounts.

Next action:
Resolve compatibility issue before proceeding to cutover.
```

---

# 6. `task.md`

## 6.1 Schema

```markdown
# TASK-XXX — Task Title

## Status

PROPOSED

## Objective

...

## Mode

...

## Scope

### Included

- ...

### Excluded

- ...

## Requirements

- REQ-...

## Constraints

- ...

## Dependencies

- ...

## Expected Change Surface

- ...

## Change Budget

...

## Risk

R2 — Moderate

## Plan

1. ...
2. ...
3. ...

## Acceptance Criteria

- [ ] ...
- [ ] ...

## Validation Requirements

- V1 ...
- V4 ...
- V7 ...

## Related Decisions

- DEC-...

## Notes / Findings

...

## Result

...

## Final Status

...
```

---

# 6.2 Required Sections

### Identity

Task ID and title.

### Status

Current task state.

### Objective

What the task must accomplish.

### Scope

What is included and excluded.

### Requirements

Relevant requirement IDs.

### Constraints

Relevant restrictions.

### Acceptance Criteria

Conditions for success.

### Validation Requirements

Required verification.

---

# 6.3 Optional Sections

* Mode
* Dependencies
* Expected Change Surface
* Change Budget
* Risk
* Plan
* Related Decisions
* Notes / Findings
* Result
* Final Status

---

# 6.4 Task Status

Recommended states:

```text
PROPOSED
DEFINED
PLANNED
IN_PROGRESS
VERIFYING
COMPLETED
PARTIALLY_COMPLETED
BLOCKED
FAILED
CANCELLED
```

Projects may simplify this list.

The important requirement is that status must communicate the task's actual state.

---

# 6.5 Task Result

The task should end with a concise result describing:

* what was implemented
* what was not implemented
* validation performed
* known limitations
* follow-up work

---

# 7. `decision.md`

## 7.1 Schema

```markdown
# DEC-XXX — Decision Title

## Status

PROPOSED

## Decision Type

Architecture

## Problem

...

## Context

...

## Evidence

- ...

## Constraints

- ...

## Options

### Option A

...

### Option B

...

## Trade-offs

| Option | Advantages | Disadvantages |
|---|---|---|
| A | ... | ... |
| B | ... | ... |

## Decision

...

## Rationale

...

## Consequences

### Positive

- ...

### Negative

- ...

### Risks

- ...

## Related Requirements

- REQ-...

## Related Tasks

- TASK-...

## Supersedes

- DEC-...

## Superseded By

- DEC-...
```

---

# 7.2 Required Sections

### Identity

Decision ID and title.

### Status

Current decision state.

### Problem

What required a decision.

### Context

Relevant situation.

### Decision

What was selected.

### Rationale

Why it was selected.

### Consequences

Important implications.

---

# 7.3 Optional Sections

* Decision Type
* Evidence
* Constraints
* Options
* Trade-offs
* Related Requirements
* Related Tasks
* Supersedes
* Superseded By

---

# 7.4 Decision Principle

The amount of detail should be proportional to the importance of the decision.

A minor technical choice might require:

```markdown
## Decision

Use the existing HTTP client because the project already standardizes on it.

## Rationale

Avoid introducing another dependency.
```

A major architectural decision may require a complete options and trade-off analysis.

---

# 8. Common Metadata

AICF artifacts may use lightweight metadata.

Recommended metadata:

```markdown
---
id: TASK-012
type: task
status: IN_PROGRESS
created: 2026-09-10
updated: 2026-09-10
---
```

However, metadata should not become mandatory everywhere unless tooling demonstrates a need for it.

The semantic ID should always remain visible in the document.

---

# 9. IDs

IDs provide stable identity independent of filenames.

Recommended formats:

```text
REQ-001
DEC-001
TASK-001
VAL-001
```

IDs should be:

* unique within the project
* stable
* human-readable
* never reused

If an artifact is deprecated or deleted, its ID should not be reassigned.

---

# 10. Filenames

Recommended:

```text
REQ-001-user-registration.md
DEC-001-authentication-strategy.md
TASK-001-registration-api.md
VAL-001-registration-api.md
```

Filenames should be descriptive.

The ID provides identity.

The descriptive portion provides usability.

---

# 11. Status Rules

Status must describe actual state rather than intention.

For example:

Incorrect:

```text
Status: COMPLETED
```

when implementation exists but tests have not run.

Correct:

```text
Status: VERIFYING
```

Similarly:

```text
Status: COMPLETED
```

should imply the task's required validation has been satisfied.

---

# 12. Cross-Reference Rules

References should use IDs.

Example:

```markdown
Related Requirement: REQ-012
Related Task: TASK-023
Related Decision: DEC-008
Validation: VAL-031
```

Where useful, references may also include relative links:

```markdown
[REQ-012](../requirements/REQ-012-search.md)
```

The ID remains the authoritative identity.

---

# 13. Artifact Dependency Model

The foundational relationships are:

```text
PROJECT
   │
   ├── RULES
   │
   ├── DOMAIN / FEATURE
   │
   ├── REQUIREMENT
   │       │
   │       └── TASK
   │              │
   │              ├── DECISION
   │              │
   │              └── VALIDATION
   │
   └── STATE
```

A task does not require a decision.

A task does not require a feature artifact.

A decision does not require a task.

Artifacts should exist only when their information is materially useful.

---

# 14. Minimum Artifact Principle

The minimum AICF project should be able to operate with:

```text
.aicf/
├── rules.md
├── project.md
└── state.md
```

A task is added when meaningful work begins.

A decision is added when a material decision occurs.

Additional artifacts are added when project complexity justifies them.

Therefore AICF should scale:

```text
Small Project
    ↓
3 core files

Medium Project
    ↓
Core + Tasks + Decisions

Large Project
    ↓
Core + Domains + Features + Requirements
+ Tasks + Decisions + Validation + Environment
```

This keeps AICF lightweight.

---

# 15. Schema Evolution

Schemas may evolve between AICF versions.

Projects should not be required to rewrite historical artifacts merely because the framework schema changes.

AICF tooling should favour:

* backward compatibility
* optional fields
* graceful handling of missing fields
* explicit migration when structural changes are necessary

---

# 16. Canonical Principle

The schemas exist to make AICF operational, not bureaucratic.

> **Structure enough to preserve engineering knowledge. Do not structure information merely because it can be structured.**

The quality of AICF is determined not by the number of Markdown files, but by whether an AI agent can reliably understand, execute, validate, and recover engineering work.
