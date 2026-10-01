# AICF Framework Definition v0.1

## 2. Core Principles

The following principles define the fundamental operating philosophy of AICF.

These principles are **tool-independent** and apply regardless of whether the project is being developed using Claude, Gemini, Antigravity, Cursor, Codex, or another AI coding agent.

They are intentionally expressed as principles rather than implementation instructions. Detailed rules and procedures will be defined in later sections of the framework.

---

## P01 — The Repository Is the Memory

### Principle

> **Persistent project knowledge must live within the project, not inside an AI conversation.**

AI conversations are temporary execution environments.

The repository and its structured engineering artifacts are the persistent source of project knowledge.

The project should contain sufficient information for an appropriately configured AI agent to understand and continue the work without access to previous conversations.

### Implications

Important information should be persisted when it affects future development, including:

* requirements
* architecture
* business rules
* technical constraints
* decisions
* assumptions
* current state
* known issues
* task status
* validation results

### Anti-pattern

```text
"We discussed this earlier in Claude."
```

### AICF approach

```text
"We documented this decision in the project."
```

---

# P02 — Context Before Code

### Principle

> **An AI agent must understand the relevant context before making meaningful changes.**

Code generation is not the first step of engineering.

The agent should first establish:

* what is being changed
* why it is being changed
* how the existing system works
* what constraints apply
* what already exists
* what is unknown

### Default sequence

```text
Understand
    ↓
Inspect
    ↓
Define
    ↓
Plan
    ↓
Implement
```

The complexity of the task determines how much planning and inspection is required.

A trivial change should not require an unnecessary planning ceremony, while a significant architectural change must not bypass discovery.

### Anti-pattern

```text
User:
"Add authentication."

AI:
"Sure, I'll implement JWT..."
```

### AICF approach

```text
Understand authentication requirements
        ↓
Inspect existing authentication
        ↓
Identify architecture
        ↓
Identify unknowns
        ↓
Define implementation
        ↓
Implement
```

---

# P03 — AI Is an Executor, Not the Source of Truth

### Principle

> **AI agents execute within the project's established context; they do not become the authority for requirements, architecture, or business decisions.**

An AI agent may:

* analyze
* recommend
* reason
* challenge
* implement
* validate

But it must distinguish between:

```text
Established decision
Recommended approach
Inference
Assumption
Unknown
```

The agent must not silently convert its recommendation into an established project decision.

### Important distinction

AICF does not require AI to be passive.

An agent should be capable of saying:

> "The requested approach conflicts with the current architecture. Here is the conflict and two alternatives."

But the agent should not silently replace the architecture.

---

# P04 — Unknown Is Better Than Wrong

### Principle

> **When reliable information is unavailable, uncertainty must be exposed rather than hidden through invention.**

AI systems naturally attempt to produce an answer even when information is incomplete.

AICF explicitly rejects this behaviour for engineering-critical decisions.

The agent must distinguish:

```text
KNOWN
INFERRED
ASSUMED
UNKNOWN
```

### Required behaviour

If information is missing, the agent should:

1. Identify what is missing.
2. Determine whether the missing information affects implementation.
3. Determine the risk of proceeding.
4. Make a reversible assumption only when appropriate.
5. Record material assumptions.
6. Stop and request clarification when the risk is significant.

### Core rule

> **A plausible implementation is not evidence that the requirement was understood correctly.**

---

# P05 — Work Must Be Bounded

### Principle

> **Every meaningful AI operation must have a defined scope.**

AI agents are capable of discovering problems beyond the original task.

That does not automatically authorize them to fix those problems.

Every task should establish boundaries such as:

* objective
* scope
* allowed changes
* restricted areas
* non-goals
* dependencies
* acceptance criteria

### Example

A task to update an employee profile page does not automatically authorize:

```text
Authentication refactoring
Database redesign
Global component rewrite
Navigation redesign
Dependency upgrades
```

unless those changes are explicitly brought into scope.

---

# P06 — No Silent Scope Expansion

### Principle

> **An agent must not expand a task's scope without making the expansion visible.**

During implementation, an agent may discover that additional work is required.

The correct behaviour is:

```text
Discover dependency
      ↓
Explain dependency
      ↓
Assess impact
      ↓
Request approval OR create additional task
```

Not:

```text
Discover dependency
      ↓
Modify everything
      ↓
Report completion
```

### Exception

Minor changes that are clearly necessary to complete the approved task and fall within its defined change boundary may proceed without additional approval.

The distinction between **necessary implementation change** and **scope expansion** will be formalized in the Change Model.

---

# P07 — Prefer Existing Patterns Over New Invention

### Principle

> **When an existing project pattern satisfies the requirement, reuse it before introducing a new pattern.**

AI agents often produce technically valid but architecturally inconsistent implementations.

Before creating something new, the agent should inspect whether the project already has:

* components
* utilities
* services
* hooks
* API patterns
* state-management patterns
* validation patterns
* testing patterns
* styling conventions
* error-handling mechanisms

### Desired behaviour

```text
Existing pattern
      ↓
Evaluate suitability
      ↓
Reuse / extend
```

rather than:

```text
New requirement
      ↓
Invent new implementation
```

### Important qualification

"Reuse existing patterns" does not mean preserving poor architecture indefinitely.

If an existing pattern is demonstrably unsuitable, the agent should identify the problem and propose the appropriate change rather than silently introducing a competing pattern.

---

# P08 — Minimize Change Surface

### Principle

> **Make the smallest change that correctly satisfies the requirement.**

AI-generated changes should be proportionate to the task.

A task requiring two files should not routinely result in changes to twenty files.

This principle supports:

* lower regression risk
* easier review
* lower token consumption
* easier debugging
* clearer attribution of failures
* easier rollback

### Desired behaviour

```text
Requirement
    ↓
Minimal sufficient change
    ↓
Validation
```

rather than:

```text
Requirement
    ↓
Broad refactoring
    ↓
Unrelated improvements
    ↓
Dependency changes
    ↓
Large regression surface
```

This principle will later connect directly to the **Change Budget** mechanism.

---

# P09 — Plan Proportionally to Risk

### Principle

> **The amount of planning required must be proportional to the complexity and risk of the change.**

AICF must not turn every one-line change into a bureaucratic process.

At the same time, complex changes must not bypass planning.

### Example

#### Low complexity

```text
Fix typo
↓
Implement
↓
Validate
```

#### Medium complexity

```text
Inspect
↓
Plan
↓
Implement
↓
Validate
```

#### High complexity

```text
Discover
↓
Architecture analysis
↓
Options
↓
Risk assessment
↓
Plan approval
↓
Incremental implementation
↓
Validation
```

AICF therefore follows:

> **Minimum sufficient process, not maximum process.**

---

# P10 — Validation Defines Completion

### Principle

> **Generated code is not complete merely because it compiles or appears correct.**

A task is complete only when its appropriate acceptance and quality criteria have been satisfied.

Depending on the task, validation may include:

```text
Syntax
Type safety
Lint
Unit tests
Integration tests
Functional validation
Regression validation
Security validation
Performance validation
Accessibility validation
Architecture compliance
```

Not every task requires every gate.

Validation must be **risk and task appropriate**.

### Core equation

```text
DONE =
Implementation
+
Acceptance
+
Validation
+
State Update
```

---

# P11 — Decisions Must Be Persistent

### Principle

> **Important decisions must survive the conversation that created them.**

An architectural or business decision made during development should not depend on the AI remembering it later.

Material decisions should become persistent project knowledge.

Examples:

```text
Why PostgreSQL was selected
Why authentication uses a particular provider
Why an API follows a specific pattern
Why a migration is being performed incrementally
Why a particular library was rejected
Why a business rule behaves differently from the obvious implementation
```

### Desired lifecycle

```text
Question
   ↓
Analysis
   ↓
Decision
   ↓
Reason
   ↓
Persistent record
```

This prevents future agents from repeatedly reopening settled decisions without reason.

---

# P12 — State Must Be Recoverable

### Principle

> **At any meaningful point in development, another agent should be able to determine what has happened, what is happening, and what should happen next.**

AICF therefore treats project state as a first-class engineering artifact.

A recoverable state should answer:

```text
What are we building?
Where are we?
What has been completed?
What is currently in progress?
What is blocked?
What decisions were made?
What remains?
What should happen next?
```

This enables:

```text
Session A
    ↓
Persist state
    ↓
Session B
    ↓
Continue
```

and:

```text
Claude
    ↓
Persist state
    ↓
Cursor
    ↓
Persist state
    ↓
Gemini
```

---

# P13 — Context Must Be Progressive

### Principle

> **Load the minimum sufficient context required to perform the current task correctly.**

More context does not automatically produce better results.

Excessive context can:

* consume tokens
* dilute important information
* increase conflicting instructions
* make relevant information harder to identify
* increase processing cost

AICF therefore structures context hierarchically:

```text
Global
  ↓
Project
  ↓
Domain
  ↓
Feature
  ↓
Task
  ↓
Relevant source
```

The agent should progressively load context rather than indiscriminately consuming the entire project knowledge base.

---

# P14 — Traceability Over Conversation

### Principle

> **Important implementation decisions should be traceable from requirement to implementation to validation.**

AICF should enable a chain such as:

```text
Requirement
    ↓
Feature
    ↓
Task
    ↓
Implementation
    ↓
Validation
```

Where applicable, decisions and risks should also be connected:

```text
Requirement
    ↓
Decision
    ↓
Task
    ↓
Implementation
    ↓
Validation
```

This provides engineering traceability without requiring the preservation of a long AI conversation.

---

# P15 — Human Authority Remains Explicit

### Principle

> **AI autonomy must have defined boundaries, particularly for high-impact decisions.**

AICF is designed to increase AI autonomy safely, not to remove human accountability.

Human approval may be required for areas such as:

* significant architecture changes
* security architecture
* authentication changes
* authorization changes
* data deletion
* destructive migrations
* payment behaviour
* major API contract changes
* significant infrastructure changes
* material business-rule changes

The exact approval matrix will be defined later.

---

# P16 — Failure Must Be Recoverable

### Principle

> **AI failure should result in a recoverable project state rather than uncontrolled degradation.**

AI agents will make mistakes.

AICF therefore assumes failure is possible and designs for recovery.

When an implementation fails, the agent should preserve:

* what was attempted
* what failed
* why it failed, if known
* what remains valid
* what remains unresolved
* what should be attempted next

The agent should not repeatedly generate increasingly complex fixes without reassessing the underlying problem.

### Failure loop

```text
Attempt
  ↓
Validate
  ↓
Failure
  ↓
Diagnose
  ↓
Reassess
  ↓
Corrective plan
  ↓
Attempt again
```

---

# P17 — Evidence Over Confidence

### Principle

> **Engineering conclusions should be based on observable evidence whenever possible.**

AI confidence is not evidence.

Examples:

Instead of:

> "This API should return 200."

Prefer:

> "The existing API convention returns 200 for successful mutations."

Instead of:

> "This optimization will improve performance."

Prefer:

> "The current bundle analysis shows X; the proposed change targets X. Performance must be re-measured after implementation."

AICF therefore favors:

```text
Evidence
→ Reasoning
→ Decision
```

over:

```text
Confidence
→ Assertion
→ Implementation
```

---

# P18 — The Framework Must Remain Lightweight

### Principle

> **AICF must reduce engineering friction, not create a new form of bureaucracy.**

The framework itself must be subject to the same principles it imposes on AI-assisted development.

AICF should avoid:

* unnecessary documentation
* duplicate context
* excessive ceremony
* mandatory artifacts for trivial changes
* repeated information
* unnecessarily large prompts
* process that does not improve engineering outcomes

### Core rule

> **Create structure only when the structure provides value.**

This principle is essential because an over-engineered AI framework could become worse than the problem it attempts to solve.

---

# 2.1 Principle Hierarchy

Not all principles have equal operational priority.

When principles appear to conflict, the following hierarchy applies:

```text
Safety & Correctness
        ↓
Requirement Fidelity
        ↓
Architectural Integrity
        ↓
Scope Control
        ↓
Validation
        ↓
Efficiency
        ↓
Convenience
```

For example:

If completing a task efficiently requires guessing an unknown security requirement:

```text
Efficiency
    VS
Safety / Correctness
```

AICF prioritizes safety and correctness.

---

# 2.2 The AICF Principle Set

The principles can be summarized as:

```text
P01  Repository is the Memory
P02  Context Before Code
P03  AI Is an Executor
P04  Unknown Is Better Than Wrong
P05  Work Must Be Bounded
P06  No Silent Scope Expansion
P07  Prefer Existing Patterns
P08  Minimize Change Surface
P09  Plan Proportionally to Risk
P10  Validation Defines Completion
P11  Decisions Must Be Persistent
P12  State Must Be Recoverable
P13  Context Must Be Progressive
P14  Traceability Over Conversation
P15  Human Authority Remains Explicit
P16  Failure Must Be Recoverable
P17  Evidence Over Confidence
P18  Framework Must Remain Lightweight
```

---

# 2.3 Core Principle Statement

The AICF philosophy can therefore be expressed as:

> **Understand before changing.
> Know before assuming.
> Bound before executing.
> Reuse before reinventing.
> Change minimally.
> Validate before declaring done.
> Record before forgetting.
> Recover before continuing blindly.**

These principles form the foundation for the AICF AI Behaviour Contract, Operating Model, Context Model, and Change & Validation Model that follow.
