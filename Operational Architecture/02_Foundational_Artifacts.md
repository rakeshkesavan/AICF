# AICF Artifact Specification — Foundational Artifacts

## 1. Purpose

This specification defines the five foundational artifacts required by the AICF operational architecture:

1. `rules.md`
2. `project.md`
3. `state.md`
4. `task.md`
5. `decision.md`

These artifacts form the minimum persistent structure required for an AI agent to operate safely and recoverably within an AICF-enabled project.

They answer five fundamental questions:

| Artifact      | Question                          |
| ------------- | --------------------------------- |
| `rules.md`    | How must the AI operate?          |
| `project.md`  | What is this project?             |
| `state.md`    | Where is the project now?         |
| `task.md`     | What are we doing now?            |
| `decision.md` | Why was an important choice made? |

---

# 2. General Artifact Rules

All AICF artifacts should follow these principles:

### 2.1 Single responsibility

Each artifact has a clearly defined purpose.

### 2.2 Minimal sufficient information

An artifact should contain enough information to perform its purpose, but not become a general documentation repository.

### 2.3 Persistent value

Information should be stored only when it is likely to remain useful beyond the current interaction.

### 2.4 Explicit authority

The artifact's role and authority must be clear.

### 2.5 Current over historical

Current state belongs in current-state artifacts.

Historical rationale belongs in decision records.

### 2.6 Human-readable and AI-readable

Artifacts should use predictable structure while remaining easy for engineers to understand.

### 2.7 No conversation dependency

Essential information must not exist only in the AI conversation.

### 2.8 No secrets

Credentials, tokens, private keys, passwords, and sensitive secrets must never be stored in AICF artifacts.

---

# 3. `rules.md`

## 3.1 Purpose

`rules.md` defines project-specific rules governing AI-assisted engineering.

It answers:

> **“What must the AI follow while working on this project?”**

It complements the universal AICF framework.

It should contain only rules that are relevant to this specific project.

---

## 3.2 When It Exists

Every AICF-enabled project should have `rules.md`.

For a newly initialized project, it may begin with a minimal rule set and evolve as stable project conventions emerge.

---

## 3.3 Authority

`rules.md` has high authority for project-specific engineering behaviour.

However, it cannot override:

* explicit higher-level AICF principles
* approved requirements
* human authority boundaries
* security or platform constraints

---

## 3.4 Ownership

Rules may be:

* established by project owners
* proposed by AI
* accepted by authorized humans
* updated as project conventions evolve

AI may recommend a rule but should not silently establish important project policy.

---

## 3.5 Required Information

### Project Engineering Rules

Rules concerning:

* architecture
* coding
* testing
* dependencies
* security
* naming
* error handling
* API design
* data handling

### AI Operating Rules

Project-specific instructions such as:

* required validation
* approval requirements
* prohibited changes
* protected areas
* preferred implementation patterns

### Architectural Constraints

Important constraints the AI must respect.

---

## 3.6 Optional Information

* tooling conventions
* branch conventions
* commit conventions
* documentation conventions
* performance requirements
* deployment restrictions

Only include these if they materially affect AI-assisted engineering.

---

## 3.7 Anti-Patterns

Do not use `rules.md` for:

* current task instructions
* temporary decisions
* project status
* conversation history
* complete architecture documentation
* generic AICF principles already defined by the framework

---

# 4. `project.md`

## 4.1 Purpose

`project.md` provides stable project-level context.

It answers:

> **“What is this system, what does it do, and how is it broadly structured?”**

---

## 4.2 When It Exists

Every AICF-enabled project should have a `project.md`.

It should be established early during project initialization.

---

## 4.3 Authority

`project.md` is authoritative for **declared project context**, but actual implementation may provide evidence that the documented state is outdated.

Therefore:

> Project documentation describes intended/current project context; source and runtime evidence must be consulted when implementation truth matters.

---

## 4.4 Ownership

The project team owns the meaning of the project.

AI may update project context when:

* a material architectural change occurs
* project scope changes
* a stable project fact is discovered
* an existing statement becomes outdated

Material changes should be traceable where appropriate.

---

## 4.5 Required Information

### Project Identity

* project name
* purpose
* primary objective

### Product/System Context

* primary users
* major capabilities
* important domain terminology

### Technical Context

* technology stack
* major frameworks
* major components
* repository structure

### Architecture

A concise high-level architectural description.

### External Systems

Major external services or dependencies.

### Constraints

Important technical, business, security, or operational constraints.

---

## 4.6 Optional Information

* deployment model
* non-functional requirements
* scalability expectations
* supported platforms
* development conventions
* high-level roadmap

Only stable information should live here.

---

## 4.7 Anti-Patterns

Do not turn `project.md` into:

* complete technical documentation
* API reference
* source-code explanation
* task list
* changelog
* decision history

---

# 5. `state.md`

## 5.1 Purpose

`state.md` represents the current recoverable state of the project.

It answers:

> **“Where are we now?”**

This is one of the most important AICF artifacts.

---

## 5.2 When It Exists

Every AICF-enabled project should have a `state.md`.

It should be maintained throughout the project lifecycle.

---

## 5.3 Authority

`state.md` is authoritative for **declared project state**.

However, the AI should verify claims against source, tests, validation evidence, or other authoritative artifacts where necessary.

---

## 5.4 Ownership

The state may be maintained by AI and humans.

AI should update it when meaningful work changes project state.

It should not be updated for every trivial action.

---

## 5.5 Required Information

### Current Objective

What the project is currently trying to accomplish.

### Current Milestone

Current meaningful project stage, where applicable.

### Active Work

Tasks currently in progress.

### Completed Work

Recent/material completed work relevant to current context.

### Known Issues

Known unresolved problems.

### Open Unknowns

Material unanswered questions.

### Open Decisions

Decisions requiring resolution.

### Validation State

Current meaningful validation status.

### Blocked Work

Work that cannot currently proceed.

### Next Actions

The most relevant next engineering actions.

---

## 5.6 State Characteristics

`state.md` should be:

* concise
* current
* operational
* recoverable

A new AI agent should be able to read it quickly and understand the project's current position.

---

## 5.7 What Does Not Belong

Do not use `state.md` as:

* a chronological diary
* an AI conversation transcript
* a detailed task tracker
* a complete changelog
* a dump of every discovery

---

## 5.8 State Update Principle

The AI should update project state when an event materially changes:

* what is being worked on
* what has been completed
* what is blocked
* what is known
* what remains unknown
* what decisions are pending
* validation status
* project direction

---

# 6. `task.md`

## 6.1 Purpose

A task defines a bounded unit of engineering work.

It answers:

> **“What exactly are we trying to accomplish, and what is the AI allowed to change?”**

The task is the primary execution boundary for an AI agent.

---

## 6.2 When It Exists

A task artifact should exist for meaningful engineering work.

Trivial changes may not require a persistent task artifact if the project rules permit lightweight execution.

---

## 6.3 Authority

The task defines the authorized scope of the work.

It does not override:

* project rules
* approved requirements
* architectural decisions
* human approval requirements
* protected boundaries

---

## 6.4 Required Information

### Identity

* task ID
* title
* status

### Objective

The intended engineering outcome.

### Scope

What the task includes.

### Non-goals

What the task explicitly does not include.

### Requirements

Relevant requirement references.

### Constraints

Relevant rules, technical limitations, or compatibility requirements.

### Dependencies

Other work, systems, decisions, or components required.

### Expected Change Surface

Expected areas affected.

### Acceptance Criteria

Conditions that determine whether the task satisfies its intended outcome.

### Validation Requirements

What must be validated before completion.

### Risk

Risk classification and relevant risk factors.

---

## 6.5 Optional Information

* project mode
* task mode
* change budget
* autonomy level
* implementation plan
* rollback strategy
* linked decisions
* linked features/domains

---

## 6.6 Task Lifecycle

A task may move through:

```text
PROPOSED
   ↓
DEFINED
   ↓
PLANNED
   ↓
IN PROGRESS
   ↓
VERIFYING
   ↓
COMPLETED
```

Alternative terminal states include:

```text
BLOCKED
FAILED
CANCELLED
PARTIALLY COMPLETED
```

The exact status vocabulary may be simplified in implementation if necessary.

---

## 6.7 Task Scope Rule

A task must clearly distinguish:

### Required work

Necessary to satisfy the objective.

### Supporting work

Necessary to safely implement the objective.

### Opportunistic work

Useful but unrelated improvement.

Opportunistic work should normally become a separate task.

---

## 6.8 Task Change Rule

If implementation reveals legitimate additional work, the task may be updated.

If the newly discovered work materially changes:

* objective
* scope
* risk
* architecture
* change surface
* validation requirements

the AI should reassess the task rather than silently expanding it.

---

# 7. `decision.md`

## 7.1 Purpose

A decision record captures a material engineering decision and its rationale.

It answers:

> **“Why did we choose this approach?”**

---

## 7.2 When It Exists

Create a decision record when changing the decision later would create meaningful:

* rework
* architectural impact
* compatibility impact
* security impact
* data impact
* integration impact
* future development consequences

Not every implementation choice requires a decision record.

---

## 7.3 Authority

Decision authority depends on the decision type and project governance.

An AI-generated recommendation is not automatically an accepted decision.

Decision states:

```text
PROPOSED
ACCEPTED
REJECTED
SUPERSEDED
DEPRECATED
```

---

## 7.4 Required Information

### Decision Identity

* decision ID
* title
* status

### Problem

What required a decision?

### Context

Relevant facts, constraints, and evidence.

### Options

Meaningful alternatives considered.

### Trade-offs

Important advantages and disadvantages.

### Decision

What was selected?

### Rationale

Why was it selected?

### Consequences

What follows from the decision?

---

## 7.5 Optional Information

* rejected alternatives
* related requirements
* related tasks
* related architecture
* implementation notes
* review/approval information

---

## 7.6 Decision Lifecycle

```text
PROPOSED
   ↓
REVIEWED
   ↓
ACCEPTED
```

or:

```text
PROPOSED
   ↓
REJECTED
```

An accepted decision may later become:

```text
SUPERSEDED
DEPRECATED
```

The original record should normally remain available for historical traceability.

---

# 8. Relationships Between the Five Artifacts

The five artifacts form the core operational loop.

```text
             rules.md
                 │
                 ↓
             project.md
                 │
                 ↓
              state.md
                 │
                 ↓
              task.md
                 │
          ┌──────┴──────┐
          ↓             ↓
     decision.md    implementation
          │             │
          └──────┬──────┘
                 ↓
             validation
                 ↓
              state.md
```

This is not a strict linear dependency.

The artifacts form a connected knowledge system.

---

# 9. Retrieval Order

For a new AI session, the default retrieval order should be:

```text
1. rules.md
2. project.md
3. state.md
4. active task
5. relevant decisions
6. relevant domain/feature/requirements
7. relevant source
```

The agent should stop when sufficient context has been established.

It should retrieve additional artifacts when required by uncertainty, dependencies, scope, risk, or validation.

---

# 10. Update Rules

### `rules.md`

Update only when stable project rules change.

### `project.md`

Update when stable project context changes.

### `state.md`

Update whenever material current project state changes.

### `task.md`

Update when task scope, status, plan, findings, or outcome materially changes.

### `decision.md`

Create when a material decision is made; update status when that decision changes.

---

# 11. The Five-Artifacts Test

Before adding another artifact to AICF, ask:

> **Can this information clearly belong in one of the existing five artifacts?**

If yes, do not create another artifact.

If no, determine whether the information represents:

* reusable project knowledge
* domain/feature context
* requirement
* validation evidence
* another genuinely distinct information class

Only then should another artifact type be introduced.

---

# 12. Minimal Recovery Test

AICF should pass the following test:

> A new AI agent with no access to previous conversations should be able to read `rules.md`, `project.md`, `state.md`, and the active task and understand what is happening, what is expected, what constraints exist, and what it should do next.

Additional artifacts should be necessary only when deeper context is required.

---

# 13. Foundational Design Principle

The five artifacts collectively answer:

```text
RULES
  → How must I behave?

PROJECT
  → What am I working on?

STATE
  → Where are we now?

TASK
  → What am I doing?

DECISION
  → Why are we doing it this way?
```

Everything else in the AICF operational architecture exists to provide additional context, evidence, or specialization when these five are insufficient.

> **Start with the minimum context required to act safely. Expand only when the work requires it.**
