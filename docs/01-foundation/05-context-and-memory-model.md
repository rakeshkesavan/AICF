# AICF Framework Definition v0.1

## 5. Context & Memory Model

### 5.1 Purpose

The AICF Context & Memory Model defines how project knowledge is created, organized, retrieved, presented, and preserved for AI-assisted software development.

The objective is to provide an AI agent with:

> **The minimum sufficient context required to make a correct decision or perform a task safely.**

AICF does not equate more context with better results.

Instead:

```text
Relevant Context
+
Correct Context
+
Timely Context
=
Effective Context
```

---

# 5.2 The Context Problem

AI-assisted development creates two opposing problems.

### Insufficient Context

The agent may:

* misunderstand requirements
* duplicate existing functionality
* violate architectural decisions
* invent APIs
* introduce inconsistent patterns
* make incorrect assumptions

### Excessive Context

The agent may:

* consume unnecessary tokens
* lose important information in noise
* encounter conflicting instructions
* spend time processing irrelevant information
* reduce available context for actual code
* become less precise

AICF therefore optimizes for:

> **Minimum sufficient context, not minimum context.**

---

# 5.3 The Repository as Persistent Memory

AICF treats the repository as the primary persistent memory of the development process.

The AI conversation is considered:

```text id="s9n7qm"
Temporary Working Memory
```

while the project artifacts provide:

```text id="f3qv8s"
Persistent Project Memory
```

Conceptually:

```text id="a4zq5y"
                PROJECT
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
     Context    Decisions    State
        │          │          │
        └──────────┼──────────┘
                   ↓
              AI SESSION
                   ↓
             Temporary Work
                   ↓
              Persist useful
               knowledge
                   ↓
                PROJECT
```

The project should not depend on an AI platform's proprietary memory mechanism for essential engineering knowledge.

---

# 5.4 Context Hierarchy

AICF organizes context into hierarchical levels.

```text id="i6v4yl"
LEVEL 0 — GLOBAL
     ↓
LEVEL 1 — PROJECT
     ↓
LEVEL 2 — DOMAIN
     ↓
LEVEL 3 — FEATURE
     ↓
LEVEL 4 — TASK
     ↓
LEVEL 5 — SOURCE
```

Each level has a distinct responsibility.

---

# 5.5 Level 0 — Global Context

Global context contains rules that apply across projects using AICF.

Examples:

* AICF operating principles
* AI behaviour expectations
* general engineering rules
* truth and uncertainty handling
* safety expectations
* validation philosophy

Global context should remain small.

It should not contain project-specific requirements.

### Example

```text id="t8u9fy"
AICF Principles
AI Behaviour Contract
General Safety Rules
```

---

# 5.6 Level 1 — Project Context

Project context describes the specific application.

It may include:

* project purpose
* product description
* technology stack
* architecture
* major components
* engineering conventions
* repository structure
* deployment model
* external systems
* project-level constraints

Example:

```text id="7c6d8j"
Project:
Employee Management Platform

Frontend:
React + TypeScript

Backend:
Node.js

Database:
PostgreSQL

Architecture:
...

Authentication:
...

Deployment:
...
```

Project context should describe relatively stable information.

---

# 5.7 Level 2 — Domain Context

Domain context captures business or technical knowledge relevant to a specific area of the system.

Examples:

```text id="8jy0n2"
Employee Management
Payroll
Leave
Recruitment
Billing
Inventory
Orders
Authentication
Reporting
```

A domain may contain:

* business rules
* terminology
* workflows
* domain entities
* constraints
* domain-specific decisions

This prevents unrelated business knowledge from being loaded into every task.

---

# 5.8 Level 3 — Feature Context

Feature context describes a particular capability.

For example:

```text id="1g5rj6"
Employee Profile
```

may contain:

* purpose
* user flow
* functional requirements
* business rules
* related APIs
* dependencies
* UX decisions
* acceptance criteria
* feature-specific decisions

Feature context should be loaded when working on that feature.

---

# 5.9 Level 4 — Task Context

Task context defines the immediate unit of work.

It should contain only information necessary to execute the task safely.

A task may specify:

```text id="o3bq1g"
Objective
Scope
Non-goals
Acceptance Criteria
Constraints
Expected Change Surface
Dependencies
Validation Requirements
```

Task context is the most operational level of the documentation hierarchy.

---

# 5.10 Level 5 — Source Context

Source context is the actual implementation relevant to the task.

This includes:

* source files
* tests
* configurations
* schemas
* API definitions
* infrastructure definitions
* generated artifacts where relevant

The agent should discover source context rather than assuming that documentation completely represents implementation.

### Principle

> **Documentation explains the system. Source code demonstrates the system.**

Where they conflict, the discrepancy must be identified.

---

# 5.11 Progressive Context Loading

The agent should load context progressively.

The preferred model is:

```text id="v3ujc7"
START
  ↓
Global rules
  ↓
Project context
  ↓
Current state
  ↓
Task
  ↓
Relevant feature/domain context
  ↓
Relevant source
```

The agent should stop loading context when it has sufficient information to perform the task safely.

This avoids the anti-pattern:

```text id="whv5te"
Load everything
        ↓
Find something relevant somewhere
        ↓
Hope nothing conflicts
```

---

# 5.12 Context Selection

Context selection should be based on relevance.

AICF defines four primary questions:

```text id="7slw6e"
1. Is this information relevant?
2. Is it authoritative?
3. Is it current?
4. Does the agent need it now?
```

Information that fails these tests should generally not be included in the active task context.

---

# 5.13 Context Priority

When multiple pieces of context are available, the agent should prioritize:

```text id="0h3n3w"
1. Current task requirements
2. Explicit project rules
3. Current project state
4. Relevant architectural decisions
5. Relevant domain / feature context
6. Existing implementation
7. Tests and observed behaviour
8. General technical knowledge
```

This ordering may be refined by the Truth & Uncertainty Model.

---

# 5.14 Context Authority

Not every document has equal authority.

AICF distinguishes:

### Normative Context

Defines what should be true.

Examples:

* requirements
* architecture decisions
* project rules
* approved specifications

### Descriptive Context

Describes what currently exists.

Examples:

* architecture documentation
* current state
* system documentation

### Observational Context

Provides evidence about actual behaviour.

Examples:

* source code
* tests
* logs
* runtime observations

### Advisory Context

Provides recommendations rather than established facts.

Examples:

* AI recommendations
* design alternatives
* proposed architecture

The agent must distinguish these categories.

---

# 5.15 Context Freshness

Project context can become stale.

AICF therefore treats context as having a freshness dimension.

Information may be:

```text id="cl0u5c"
CURRENT
RECENT
STALE
UNKNOWN
```

When documentation conflicts with recent implementation, the agent should investigate rather than blindly trusting either source.

### Example

Documentation:

```text
Authentication uses Auth Provider A.
```

Current implementation:

```text
Authentication uses Provider B.
```

The agent should not silently select one.

It should identify the inconsistency and determine which represents the intended current state.

---

# 5.16 Single Source of Truth

AICF avoids unnecessary duplication of information.

A piece of knowledge should ideally have one authoritative location.

For example:

```text id="vl4hzm"
Authentication decision
        ↓
DECISIONS / ADR
```

rather than copying the same decision into:

```text id="7gk9th"
Project context
Feature context
Task
Agent instructions
README
```

Repeated information increases:

* maintenance cost
* token usage
* risk of contradiction

AICF therefore follows:

> **Reference knowledge; do not duplicate it unnecessarily.**

---

# 5.17 Context Inheritance

Lower-level contexts inherit relevant information from higher levels.

Conceptually:

```text id="p7xv4n"
GLOBAL
  ↓
PROJECT
  ↓
DOMAIN
  ↓
FEATURE
  ↓
TASK
```

A task should not repeat project-level rules unless there is a specific reason.

For example:

```text id="5r8u3g"
Project:
TypeScript is mandatory.

Task:
Implement employee profile.

```

The task does not need to repeat:

> "Use TypeScript."

unless the task requires an exception.

---

# 5.18 Context Override

Lower-level context may refine or override higher-level context only when explicitly authorized.

Example:

```text id="b8q8tq"
Project:
All APIs use REST.

Feature:
This integration uses GraphQL because the external
platform requires it.
```

This is a legitimate scoped exception.

The exception should be explicit.

The agent must not infer overrides merely because a different approach appears convenient.

---

# 5.19 Context Compression

Long-lived projects accumulate knowledge.

AICF therefore requires periodic compression of context.

Compression means:

```text id="f9xq1e"
Conversation history
        ↓
Important discoveries
        ↓
Persistent project knowledge
```

not:

```text id="c0l0rj"
Entire conversation
        ↓
Huge permanent transcript
```

Only information with future engineering value should survive into persistent context.

---

# 5.20 Session Handoff

AICF must support interruption and continuation.

At the end of a meaningful development session, the project should retain enough state to allow another agent to continue.

The handoff should communicate:

```text id="4uvv8r"
Current objective
Completed work
Current work
Unresolved issues
Decisions made
Assumptions
Validation status
Next recommended action
```

This becomes particularly important when:

```text id="2gn7k1"
Agent A
    ↓
Agent B
```

or:

```text id="y44n6w"
Session A
    ↓
Session B
```

---

# 5.21 Context Recovery

When starting a new session, the agent should not attempt to reconstruct the entire previous conversation.

Instead it should recover from persistent project state.

Preferred sequence:

```text id="t0t9wo"
Read project rules
      ↓
Read current state
      ↓
Read relevant task
      ↓
Read relevant feature/domain context
      ↓
Inspect source
      ↓
Continue
```

This is one of AICF's primary mechanisms for conversation independence.

---

# 5.22 Context Budget

AICF introduces the concept of a **Context Budget**.

A task should have a practical limit on how much context is loaded before execution.

The budget is not necessarily a fixed number of tokens.

It represents the principle:

> **Do not load information that does not materially improve the current engineering decision.**

Context should be evaluated based on:

* relevance
* importance
* dependency
* authority
* freshness

---

# 5.23 Context Escalation

If the agent cannot safely complete a task using the current context, it may escalate context.

For example:

```text id="j38myj"
Task context insufficient
        ↓
Load feature context
        ↓
Still insufficient
        ↓
Load domain context
        ↓
Still insufficient
        ↓
Inspect related architecture
```

This is preferable to loading the entire repository from the beginning.

---

# 5.24 Context Graph

Although the hierarchy is useful for organization, real projects are not purely hierarchical.

A feature may depend on:

```text id="h6hxwb"
Employee Profile
      │
      ├── Authentication
      ├── Employee API
      ├── Permissions
      ├── File Storage
      └── Audit Logging
```

AICF therefore treats project context conceptually as a **context graph**.

The hierarchy organizes knowledge.

The graph describes relationships.

```text id="9uyh2c"
Hierarchy = organization
Graph     = dependency
```

This distinction becomes important when building tooling around AICF.

---

# 5.25 Context Loading Decision

Before loading a context artifact, the agent should consider:

```text id="l2s1s7"
Does this affect the current task?
        ↓
YES → Is it authoritative/current?
        ↓
YES → Load
NO  → Investigate
        ↓
NO → Do not load
```

This creates a deliberate retrieval strategy rather than indiscriminate context consumption.

---

# 5.26 Context Lifecycle

AICF treats context as having a lifecycle:

```text id="8r1p5h"
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
ARCHIVE / DEPRECATE
```

Context should evolve with the project.

Old decisions and obsolete documentation should not remain indefinitely indistinguishable from current knowledge.

---

# 5.27 Context Integrity

AICF requires the framework to detect potential contradictions.

Examples:

```text id="h3r3d0"
Requirement says A
Architecture says B
Implementation does C
```

or:

```text id="9q6f5g"
Current State says feature complete
Tests indicate feature incomplete
```

The agent should surface these inconsistencies.

It must not arbitrarily choose one source without assessing authority and freshness.

---

# 5.28 Context and Token Efficiency

AICF treats token efficiency as an engineering optimization problem.

The objective is not:

> Use the fewest tokens possible.

The objective is:

> **Maximize engineering value per unit of context.**

Therefore:

```text id="f3ql71"
High-value context
        ↓
Keep
```

```text id="44ad0c"
Low-value context
        ↓
Exclude
```

```text id="n5zyx2"
Repeated context
        ↓
Reference
```

```text id="k8f0p1"
Historical context with no current relevance
        ↓
Archive
```

---

# 5.29 Context Anti-Patterns

AICF explicitly discourages:

### The Giant Prompt

Putting the entire project specification into every request.

### The Giant Context File

Maintaining one enormous document containing every project detail.

### Conversation Dependence

Assuming previous conversation history is required for future work.

### Documentation Duplication

Copying the same rules across multiple files.

### Stale Context

Leaving obsolete decisions indistinguishable from current decisions.

### Context Dumping

Providing the agent with large quantities of information without establishing relevance.

### Context Starvation

Providing so little information that the agent must guess.

---

# 5.30 Context Quality Model

Good context should be:

```text id="3q2j3a"
Relevant
Authoritative
Current
Concise
Discoverable
Structured
Non-duplicative
Traceable
```

The quality of AI output is therefore influenced not only by the model but by the quality of the context supplied to it.

---

# 5.31 Context Model Summary

AICF's context strategy can be summarized as:

```text id="8k9g0r"
                 PROJECT KNOWLEDGE
                        │
              ┌─────────┴─────────┐
              │                   │
          PERSISTENT           TEMPORARY
           CONTEXT              CONTEXT
              │                   │
        ┌─────┼─────┐             │
        ↓     ↓     ↓             ↓
     Rules  State  Knowledge    AI Session
        │     │      │             │
        └─────┼──────┘             │
              ↓                    │
        Relevant Context ←─────────┘
              ↓
             TASK
              ↓
         SOURCE CODE
              ↓
           OUTPUT
              ↓
      Important knowledge
       persisted back
```

---

# 5.32 Core Context Principle

The AICF Context & Memory Model can be summarized as:

> **Persist what matters. Load what is relevant. Trust according to authority. Verify what conflicts. Compress what is temporary. Never depend on conversation history for essential project knowledge.**

---

# 5.33 Relationship to Other Sections

The Context & Memory Model provides the information architecture for AICF.

It connects:

```text id="9bb0m5"
Core Principles
       ↓
AI Behaviour
       ↓
Context & Memory
       ↓
Truth / Uncertainty / Decisions
       ↓
Change / Validation
```

The next section will define **how the agent determines what is true, what is inferred, what is assumed, and what is unknown**, and how decisions are made and persisted when information is incomplete.

This will form AICF's primary **hallucination-control model**.
