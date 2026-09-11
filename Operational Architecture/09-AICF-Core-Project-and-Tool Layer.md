# AICF Core, Project, and Tool Layer

## 1. Purpose

AICF consists of three distinct layers:

1. **AICF Core** — defines the universal engineering methodology.
2. **Project Layer** — defines how AICF applies to a specific software project.
3. **Tool Adapter Layer** — translates AICF into instructions and capabilities for a specific AI coding tool.

These layers must remain conceptually separate.

The AI tool may change.
The project may change.
The AICF engineering system remains stable.

---

# 2. Layer Model

```text
                    AICF CORE
             Universal Engineering Rules
                       │
                       ▼
                PROJECT LAYER
       Project-specific knowledge and rules
                       │
                       ▼
                TOOL ADAPTER
       Tool/model-specific execution format
                       │
                       ▼
                  AI AGENT
                       │
                       ▼
              Repository / System
```

Each layer has a different responsibility.

| Layer        | Owns                                   | Changes when        |
| ------------ | -------------------------------------- | ------------------- |
| AICF Core    | Engineering methodology                | AICF itself evolves |
| Project      | Project-specific context and decisions | The project evolves |
| Tool Adapter | Tool-specific execution instructions   | Tool/model changes  |
| Repository   | Actual implementation                  | Software changes    |

---

# 3. AICF Core

The AICF Core defines universal behaviour that should apply to every AICF project.

It contains:

* Framework principles
* Agent behaviour contract
* Engineering lifecycle
* Context model
* Truth and uncertainty model
* Change and validation model
* Project mode model
* Artifact schemas
* Cross-artifact conventions
* Lifecycle invariants
* Authority model

The Core is **not project-specific**.

For example:

> AI must not silently expand task scope.

is an AICF Core rule.

Whereas:

> The authentication module must use the existing `AuthService`.

is a project rule.

These must never be conflated.

---

# 4. Project Layer

The Project Layer contains information specific to one software project.

It includes:

```text
rules.md
project.md
state.md
environment.md

decisions/
domains/
features/
requirements/
tasks/
validation/
```

The Project Layer defines:

* what the system is
* who uses it
* how it is architected
* project-specific engineering rules
* current state
* environments
* requirements
* domain knowledge
* features
* decisions
* engineering tasks
* validation evidence

Project artifacts are therefore the **persistent operational context of the project**.

---

# 5. Tool Adapter Layer

The Tool Adapter translates AICF into the conventions of a particular AI coding environment.

Examples:

```text
AICF
 ├── Claude Adapter
 ├── Gemini Adapter
 ├── Cursor Adapter
 ├── Codex Adapter
 └── Other Tool Adapter
```

An adapter may define:

* where instructions are placed
* how context files are loaded
* how the agent is initialized
* how tasks are presented
* how tool-specific capabilities are used
* how outputs are structured
* how context limits are handled
* how repository operations are performed

The adapter **must not redefine AICF engineering principles**.

It translates them.

---

# 6. Ownership

Ownership is explicit.

### AICF Core owns

```text
Principles
Protocols
Lifecycle
Schemas
Conventions
Invariants
```

### Project owns

```text
Project rules
Project architecture
Requirements
Decisions
Domain knowledge
Feature knowledge
Tasks
State
Validation evidence
Environment information
```

### Tool Adapter owns

```text
Tool-specific execution mechanism
Tool-specific context loading
Tool-specific instruction format
Tool-specific capabilities
```

### Repository owns

```text
Actual implementation
Tests
Configuration
Schemas
Infrastructure
Executable behaviour
```

---

# 7. Authority and Precedence

The layers do not form a simple "higher layer always wins" hierarchy.

Instead, authority depends on **what is being decided**.

However, AICF Core establishes the boundaries within which project-specific decisions operate.

For example:

```text
AICF Core
    ↓
Defines: no silent scope expansion

Project Rules
    ↓
Defines: changes to billing require explicit approval

Task
    ↓
Defines: modify billing calculation for invoice rounding

Repository
    ↓
Contains: actual billing implementation
```

A project cannot silently disable an AICF safety invariant.

For example, a project rule cannot legitimately say:

> "AI agents may modify production data without validation."

Project-specific rules may impose **stricter** requirements than AICF, but should not weaken fundamental safety, truthfulness, authority, or validation constraints.

---

# 8. Project Rules vs AICF Rules

This distinction is critical.

### AICF Rule

Universal:

> Inspect before assuming.

### Project Rule

Specific:

> All API changes must preserve backward compatibility with v2 clients.

### AICF Rule

Universal:

> Never claim validation that was not performed.

### Project Rule

Specific:

> Every API change requires contract-test validation.

### AICF Rule

Universal:

> Prefer existing patterns where appropriate.

### Project Rule

Specific:

> New React components must follow the existing component composition pattern.

The project applies AICF.

It does not redefine AICF.

---

# 9. What Belongs in `.aicf/`

The project repository should contain the **Project Layer**, not a full copy of the AICF framework specification.

Recommended structure:

```text
.aicf/
├── README.md
├── rules.md
├── project.md
├── state.md
├── environment.md
│
├── decisions/
├── domains/
├── features/
├── requirements/
├── tasks/
└── validation/
```

This keeps project context lightweight.

The project should reference the AICF version it follows rather than duplicating the complete framework definition.

For example:

```markdown
# AICF Project Configuration

AICF Version: 0.1

This project follows AICF Core v0.1.

Project-specific rules and artifacts in this directory
define how AICF is applied to this repository.
```

---

# 10. AICF Core Distribution

The AICF Core can exist independently from individual projects.

Conceptually:

```text
AICF Framework
├── core/
│   ├── principles
│   ├── protocol
│   ├── lifecycle
│   ├── context model
│   ├── truth model
│   ├── change model
│   ├── validation model
│   ├── modes
│   ├── schemas
│   └── conventions
│
├── adapters/
│   ├── claude
│   ├── gemini
│   ├── cursor
│   ├── codex
│   └── ...
│
└── templates/
    └── project
```

The exact distribution mechanism is intentionally left open at this stage.

It could eventually be:

* a Git repository
* a package
* a CLI
* a template generator
* a framework repository
* an organizational standard
* or another distribution mechanism.

AICF should not depend on the distribution mechanism.

---

# 11. Versioning

A project should explicitly identify the AICF version it follows.

For example:

```text
AICF Version: 0.1
```

This provides compatibility information without copying the framework into every project.

A project may later migrate:

```text
AICF 0.1
   ↓
AICF 0.2
```

The migration itself can be handled as an AICF migration task.

Project-specific artifacts remain project-owned.

---

# 12. Framework Evolution

AICF Core may evolve.

A change to AICF Core should not automatically rewrite project artifacts.

Instead:

```text
New AICF Version
       ↓
Compatibility Assessment
       ↓
Migration Required?
    /          \
  No            Yes
  ↓              ↓
Continue      AICF Migration Task
```

This prevents framework evolution from unexpectedly modifying project knowledge.

---

# 13. Tool Independence

The same project should be usable with different AI tools.

For example:

```text
Project Repository
       │
       └── .aicf/
             │
             ├── Project Context
             ├── State
             ├── Tasks
             ├── Decisions
             └── Validation
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Claude      Gemini      Codex
```

The tools consume the same underlying project context.

Switching tools therefore does not require reconstructing project knowledge from conversation history.

---

# 14. Tool Adapter Constraint

A tool adapter may optimize **how** AICF is executed.

It must not change **what AICF means**.

For example, a Claude adapter may say:

> Load `.aicf/rules.md` and `.aicf/state.md` before beginning implementation.

A Gemini adapter may express the same requirement using Gemini-specific instruction mechanisms.

Both represent the same AICF behaviour.

Therefore:

```text
AICF Core
    ≠
Claude Instructions
    ≠
Gemini Instructions
```

Instead:

```text
AICF Core
    ↓
Tool Adapter
    ↓
Tool-specific execution
```

---

# 15. Critical Boundary

The following distinction must always remain visible:

```text
AICF says:
    HOW an AI-assisted engineering process should operate.

Project says:
    WHAT is true and required for this project.

Repository says:
    WHAT the software actually contains and does.

Tool says:
    HOW the AI agent can interact with the project.
```

These are different sources of truth.

An AI agent must not use one as a substitute for another.

---

# 16. Recommended `.aicf/README.md`

The project-level README should explain this relationship briefly:

```text
This project uses AICF (AI Coding Framework).

AICF Core defines the universal engineering methodology.

This .aicf/ directory contains project-specific engineering
context, state, requirements, decisions, tasks, and validation
records.

Tool-specific instructions are maintained separately through
the appropriate AICF tool adapter.

The repository implementation remains the source of truth for
actual software behaviour.

AICF Version: <version>
```

---

# 17. Architectural Principle

The final architectural rule is:

> **Separate methodology, project knowledge, implementation, and tool execution.**

More specifically:

> **AICF Core defines the engineering contract. The Project Layer defines project reality. The Repository defines implementation reality. Tool Adapters define execution mechanics.**

This separation allows AICF to remain:

* tool-agnostic
* project-specific where necessary
* portable
* versionable
* recoverable
* maintainable
* lightweight
* independently evolvable

````

### One refinement I strongly recommend

We should **not** make the Core a huge runtime context that every AI agent loads every time.

Instead, think of it as **normative framework knowledge**, with the tool adapter exposing the relevant operational subset.

So the eventual runtime could look like:

```text
AICF Core
   │
   │ defines
   ▼
AICF Agent Protocol
   │
   │ instantiated for project
   ▼
.aicf/
   ├── rules.md
   ├── project.md
   ├── state.md
   └── ...
   │
   │ consumed progressively
   ▼
AI Agent
   │
   ▼
Repository
````

This is important for the **token-efficiency goal**. We don't want to solve context bloat by creating a framework that itself becomes context bloat.

With this decision, I think we can now **freeze the conceptual architecture and move to the actual `.aicf/` starter repository + templates**.
