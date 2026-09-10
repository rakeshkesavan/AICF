# AICF Operational Architecture

## 1. Purpose

The AICF Operational Architecture translates the AICF Framework Definition into a practical repository structure that an AI coding agent can use during software development.

The architecture defines:

* persistent engineering knowledge
* project context
* domain and feature context
* requirements
* decisions
* tasks
* project state
* task state
* validation records
* environment information
* relationships between artifacts
* how information is created, retrieved, updated, and deprecated

The objective is not to create a large documentation system.

The objective is to create the **minimum persistent engineering structure required for reliable AI-assisted development**.

---

# 2. Operational Design Principle

The repository must contain enough structured information for an AI agent to:

1. understand the project
2. understand the current state
3. understand the current objective
4. identify relevant constraints
5. determine what is known and unknown
6. plan a bounded change
7. implement the change
8. validate the result
9. record material knowledge
10. allow another AI agent to continue later

The operational architecture therefore follows:

> **Persistent Knowledge → Relevant Context → Controlled Work → Verified Change → Recoverable State**

---

# 3. Repository as the System of Record

AICF artifacts live inside or alongside the project repository.

The exact physical location may vary by project, but the conceptual structure remains stable.

A recommended initial structure is:

```text
project/
│
├── .aicf/
│   │
│   ├── README.md
│   ├── rules.md
│   ├── project.md
│   ├── state.md
│   ├── environment.md
│   │
│   ├── decisions/
│   │   └── ...
│   │
│   ├── domains/
│   │   └── ...
│   │
│   ├── features/
│   │   └── ...
│   │
│   ├── requirements/
│   │   └── ...
│   │
│   ├── tasks/
│   │   └── ...
│   │
│   └── validation/
│       └── ...
│
├── src/
├── tests/
├── config/
└── ...
```

This is a **reference architecture**, not a mandatory directory layout.

Projects may adapt naming and placement where necessary.

The semantic responsibilities must remain intact.

---

# 4. AICF Artifact Categories

AICF artifacts are divided into six categories.

## 4.1 Governance

Defines how AI operates.

Examples:

* `rules.md`

---

## 4.2 Project Knowledge

Defines relatively stable information about the system.

Examples:

* `project.md`
* `environment.md`

---

## 4.3 Engineering State

Defines what is happening now.

Examples:

* `state.md`
* task artifacts

---

## 4.4 Domain Knowledge

Defines business or technical areas of the system.

Examples:

* domain artifacts
* feature artifacts

---

## 4.5 Decision & Requirement Knowledge

Defines why the system behaves or is expected to behave in particular ways.

Examples:

* requirements
* decisions

---

## 4.6 Execution & Validation

Defines individual engineering work and evidence of its outcome.

Examples:

* tasks
* validation records

---

# 5. Artifact Hierarchy

The artifacts form a hierarchy of decreasing scope and increasing specificity.

```text
                    AICF
                     │
                  Project
                     │
          ┌──────────┴──────────┐
          │                     │
       Domains              Decisions
          │
       Features
          │
     Requirements
          │
        Tasks
          │
     Implementation
          │
      Validation
```

Project state exists across this hierarchy and provides the current operational view.

---

# 6. Core Artifact Set

The initial AICF implementation should contain the following core artifacts.

| Artifact         | Purpose                     | Typical Change Frequency |
| ---------------- | --------------------------- | ------------------------ |
| `rules.md`       | AI/project operating rules  | Low                      |
| `project.md`     | Stable project context      | Low                      |
| `state.md`       | Current project state       | High                     |
| `environment.md` | Environment awareness       | Medium                   |
| `decisions/`     | Material decisions          | Medium                   |
| `domains/`       | Domain context              | Medium                   |
| `features/`      | Feature context             | Medium                   |
| `requirements/`  | Explicit requirements       | Medium                   |
| `tasks/`         | Bounded engineering work    | High                     |
| `validation/`    | Validation evidence/results | High                     |

This is the **minimum proposed operational set**.

We should resist adding more artifacts until a concrete need is demonstrated.

---

# 7. `rules.md`

## Purpose

Defines the rules that govern AI behaviour within the project.

It contains project-specific rules that complement the universal AICF framework.

Examples:

* coding conventions
* architectural constraints
* security rules
* testing requirements
* prohibited technologies
* required patterns
* naming conventions
* dependency policies
* approval requirements

The file should answer:

> **“What rules must the AI follow when working on this project?”**

It should not contain:

* current task information
* temporary implementation notes
* long architectural descriptions
* conversation history
* general AICF philosophy already defined by the framework

---

# 8. `project.md`

## Purpose

Provides stable project-level context.

It should answer:

> **“What is this system and how is it structured?”**

Typical contents:

* product/system purpose
* primary users
* technology stack
* repository structure
* high-level architecture
* major components
* major external systems
* important constraints
* terminology
* deployment model
* major non-functional requirements

It should describe the project without becoming a complete technical manual.

---

# 9. `state.md`

## Purpose

Provides the current recoverable project state.

It should answer:

> **“Where is the project right now?”**

Typical contents:

```text
Current Objective
Current Milestone
Active Work
Completed Work
Known Issues
Open Unknowns
Open Decisions
Recent Material Changes
Validation Status
Blocked Items
Next Recommended Actions
```

`state.md` represents **current truth**, not project history.

It should remain concise.

An AI beginning a new session should be able to read this file and understand the project's current position without reading previous conversations.

---

# 10. `environment.md`

## Purpose

Defines environments and their relevant characteristics.

Example:

```text
Local
Development
QA
Staging
Production
```

For each environment, where appropriate:

* purpose
* availability
* configuration differences
* data characteristics
* external integrations
* deployment status
* validation restrictions
* operational constraints

Sensitive credentials must never be stored in AICF artifacts.

The purpose is to establish **environment awareness**, not secrets management.

---

# 11. Decisions

Decisions capture material choices that explain why the system is designed or implemented in a particular way.

Example:

```text
.aicf/
└── decisions/
    ├── DEC-001-authentication-strategy.md
    ├── DEC-002-database-selection.md
    └── DEC-003-api-versioning.md
```

Each decision should contain enough information to answer:

* What problem required a decision?
* What evidence existed?
* What options were considered?
* What constraints mattered?
* What was decided?
* Why?
* What are the consequences?
* Is the decision still active?

Decision records prevent the AI from repeatedly reconsidering settled architectural choices.

---

# 12. Domains

Domains represent meaningful business or technical areas.

Examples:

```text
domains/
├── identity.md
├── billing.md
├── catalog.md
├── reporting.md
└── notifications.md
```

A domain artifact should explain:

* domain purpose
* terminology
* important entities
* business/technical rules
* workflows
* dependencies
* relevant constraints
* important decisions

Domains should be created only when they provide useful contextual boundaries.

A small project may not require many domain artifacts.

---

# 13. Features

Features represent meaningful capabilities or workflows.

Example:

```text
features/
├── user-registration.md
├── product-search.md
└── invoice-generation.md
```

A feature artifact may contain:

* feature purpose
* user/business outcome
* workflow
* requirements
* business rules
* dependencies
* APIs
* relevant domain
* UX decisions
* feature-specific decisions
* current status

Feature context should be smaller and more focused than project context.

---

# 14. Requirements

Requirements represent explicit desired behaviour.

Example:

```text
requirements/
├── REQ-001-user-registration.md
├── REQ-002-search-filtering.md
└── REQ-003-invoice-export.md
```

A requirement should be:

* explicit
* testable where possible
* traceable
* appropriately scoped
* independent of implementation where practical

A requirement may link to:

* feature
* decision
* task
* validation

This establishes traceability.

---

# 15. Tasks

Tasks represent bounded units of engineering work.

Example:

```text
tasks/
├── TASK-001-registration-api.md
├── TASK-002-search-filter.md
└── TASK-003-export-validation.md
```

A task should define:

```text
Objective
Scope
Non-goals
Requirements
Constraints
Dependencies
Expected Change Surface
Acceptance Criteria
Validation Requirements
Risk
Status
```

A task is the primary execution boundary for an AI agent.

The task should contain enough information to execute safely when combined with relevant project context.

---

# 16. Validation

Validation artifacts capture evidence that a meaningful change was tested or otherwise verified.

Example:

```text
validation/
├── VAL-001-registration-api.md
├── VAL-002-search-filter.md
└── VAL-003-migration-check.md
```

A validation record may contain:

* change/task reference
* validation level
* validation performed
* command/action
* result
* evidence
* failures
* known limitations
* timestamp where useful

Validation artifacts should record what actually happened.

They must never become a mechanism for claiming successful validation that was not performed.

---

# 17. Artifact Relationships

The artifacts form a traceability graph.

```text
Project
   │
   ├── Domain
   │     │
   │     └── Feature
   │            │
   │            └── Requirement
   │                   │
   │                   └── Task
   │                          │
   │                          ├── Decision
   │                          │
   │                          └── Validation
   │
   └── Project-level Decisions
```

Not every artifact must connect to every other artifact.

Relationships should exist where they provide meaningful traceability.

---

# 18. Current State vs Historical Knowledge

AICF makes an explicit distinction between current state and historical records.

### Current state

Stored primarily in:

`state.md`

Answers:

> What is true now?

### Historical rationale

Stored primarily in:

`decisions/`

Answers:

> Why did we choose this?

### Execution history

Stored primarily in:

`tasks/` and `validation/`

Answers:

> What work was performed and what evidence resulted?

This prevents `state.md` from becoming a chronological project diary.

---

# 19. Artifact Authority

Different artifacts have different authority depending on the information being requested.

A simplified model is:

```text
Rules
   ↓
Requirements / Accepted Decisions
   ↓
Current Project State
   ↓
Domain / Feature Context
   ↓
Task Context
   ↓
Implementation
   ↓
Validation Evidence
```

However, authority is **question-dependent**.

For example:

* Requirements determine intended behaviour.
* Source code determines current implementation.
* Tests provide behavioural evidence.
* Validation records provide evidence of a performed validation.
* Decisions explain accepted choices.
* State describes the current project position.

The AI must resolve conflicts using the AICF Truth & Decision Model rather than blindly trusting file hierarchy.

---

# 20. Artifact Lifecycle

Every artifact follows a lightweight lifecycle:

```text
CREATE
  ↓
CLASSIFY
  ↓
STORE
  ↓
RETRIEVE
  ↓
USE
  ↓
VALIDATE
  ↓
UPDATE
  ↓
DEPRECATE / ARCHIVE
```

Not every artifact requires every lifecycle stage explicitly.

The lifecycle exists to prevent stale or forgotten project knowledge.

---

# 21. Progressive Context Loading

The AI should not load the entire `.aicf/` directory for every task.

Default retrieval sequence:

```text
1. AICF rules
2. Project context
3. Current project state
4. Current task
5. Relevant domain
6. Relevant feature
7. Relevant requirements
8. Relevant decisions
9. Relevant source
```

The AI stops loading context when it has the **minimum sufficient context** required to proceed safely.

Additional context is loaded when:

* uncertainty remains
* dependencies are discovered
* sources conflict
* architecture is affected
* validation requires additional information
* the task scope expands legitimately

---

# 22. Context Must Not Become Documentation for Documentation's Sake

An artifact should exist only when it provides persistent value.

Before creating a new artifact, ask:

1. Will this knowledge matter beyond the current conversation?
2. Will another agent need it later?
3. Does it have a clear scope?
4. Is there already an authoritative place for it?
5. Will maintaining it cost less than repeatedly rediscovering the knowledge?

If the answer is generally no, the information should remain temporary working context.

---

# 23. The Minimal Agent Startup Path

A new AI agent should be able to recover a project using a predictable sequence.

### Step 1

Read AICF rules.

### Step 2

Read project context.

### Step 3

Read current project state.

### Step 4

Identify the active task.

### Step 5

Load relevant domain/feature/requirements/decisions.

### Step 6

Inspect source and tests.

### Step 7

Determine whether sufficient context exists.

### Step 8

Continue through the AICF operating cycle.

Conceptually:

```text
NEW SESSION
     ↓
RULES
     ↓
PROJECT
     ↓
STATE
     ↓
TASK
     ↓
RELEVANT CONTEXT
     ↓
SOURCE
     ↓
ORIENTED AGENT
```

This is one of the most important properties that the benchmark project must eventually test.

---

# 24. Artifact Ownership

AICF does not require that every artifact be written manually by a human.

AI agents may create and update artifacts when authorized.

However:

> **The AI may maintain project knowledge, but it does not acquire authority merely by writing it.**

For example:

* AI may propose a decision.
* AI may record an accepted decision.
* AI should not mark an architectural decision as accepted without appropriate authority.

Similarly:

* AI may update task state based on actual work.
* AI must not mark validation as passed without evidence.

---

# 25. Artifact Quality Rules

Every AICF artifact should be:

### Relevant

Contains information useful for its intended scope.

### Authoritative

Its role and authority are clear.

### Current

Stale information is identified or removed.

### Concise

Avoids unnecessary explanation.

### Traceable

Links to related artifacts where useful.

### Recoverable

Useful to a new AI session without conversation history.

### Machine-readable

Uses predictable structure and terminology.

### Human-readable

A human engineer should be able to understand it quickly.

---

# 26. What AICF Artifacts Are Not

AICF artifacts are not:

* conversation transcripts
* AI scratchpads
* giant prompts
* copies of source code
* task-management replacements
* complete product specifications by default
* generic documentation repositories
* logs of every AI action
* places to store secrets

They are **persistent engineering knowledge and state**.

---

# 27. Operational Architecture Summary

The initial AICF architecture can therefore be reduced to:

```text
.aicf/
│
├── rules.md          → How AI must operate
├── project.md        → What the project is
├── state.md          → Where the project is now
├── environment.md    → Where the system operates
│
├── decisions/        → Why important choices were made
├── domains/          → Business/technical context
├── features/         → Capability context
├── requirements/     → What must be true
├── tasks/            → What needs to be done
└── validation/       → Evidence that it worked
```

The system then connects these artifacts through traceability:

```text
REQUIREMENT
     ↓
DECISION
     ↓
TASK
     ↓
IMPLEMENTATION
     ↓
VALIDATION
     ↓
STATE
```

Not every path requires every artifact, but the relationships provide a consistent engineering backbone.

---

# 28. Design Principle

> **The AICF repository should contain the minimum persistent structure necessary for an AI agent to understand, execute, validate, and recover engineering work without depending on conversation history.**

The operational architecture should remain deliberately small.

If a future artifact cannot demonstrate a clear improvement in correctness, context recovery, traceability, scope control, validation, or engineering efficiency, it should not be added.
