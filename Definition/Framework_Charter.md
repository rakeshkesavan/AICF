# AICF Framework Definition v0.1

## 1. Framework Charter

### 1.1 Framework Name

**AICF — AI Coding Framework**

A tool-agnostic engineering framework for developing, modifying, migrating, testing, and maintaining software with the assistance of AI coding agents.

> **Working principle:** The AI tool may change. The engineering system should not.

---

## 1.2 Problem Statement

AI coding agents have significantly reduced the effort required to generate software. However, generating code is only one part of software engineering.

As AI-assisted development becomes more capable, several problems emerge:

* AI agents operate with incomplete context.
* Long conversations suffer from context loss and drift.
* Agents may infer requirements that were never explicitly defined.
* AI-generated assumptions can become indistinguishable from established facts.
* Agents may modify code outside the intended scope.
* Large prompts consume unnecessary tokens and reduce signal-to-noise ratio.
* Architectural and business decisions can be lost between conversations.
* Different AI tools maintain different forms of memory and project context.
* A new agent or new conversation may not understand why previous decisions were made.
* Generated code may be considered "complete" without adequate validation.
* Vibe coding can encourage implementation before requirements and architecture are sufficiently understood.
* Existing applications, migrations, and legacy systems require substantially different discovery processes from greenfield development.
* Human developers may spend significant effort correcting AI-generated work rather than directing it.

Therefore, the primary challenge is no longer simply:

> **How do we make AI generate code?**

The larger challenge is:

> **How do we make AI participate in software engineering reliably, efficiently, consistently, and safely?**

AICF addresses this problem by introducing a persistent, structured engineering methodology around AI-assisted development.

---

## 1.3 Vision

To establish a universal engineering framework in which AI coding agents can participate in software development as capable, context-aware, controlled engineering collaborators, independent of the underlying AI platform.

AICF aims to make it possible to move between AI tools without losing the project's:

* context
* architecture
* requirements
* decisions
* state
* constraints
* validation criteria
* development history

The project itself should remain the source of truth.

---

## 1.4 Mission

AICF provides the structure required to transform AI-assisted coding from an unstructured conversational activity into a repeatable engineering process.

It achieves this through:

1. Persistent project context
2. Progressive context loading
3. Explicit requirements
4. Bounded tasks
5. Defined engineering rules
6. Persistent architectural decisions
7. Explicit uncertainty handling
8. Controlled AI autonomy
9. Change boundaries
10. Mandatory validation
11. Persistent project state
12. Tool-independent agent instructions

---

## 1.5 Core Objective

The primary objective of AICF is:

> **Enable AI agents to produce high-quality software while minimizing hallucination, context drift, unnecessary token consumption, uncontrolled scope expansion, architectural inconsistency, and unvalidated changes.**

---

## 1.6 Secondary Objectives

AICF should:

### O1 — Reduce Hallucination

Ensure that agents distinguish between:

* known information
* documented information
* observed behaviour
* inference
* assumptions
* unknown information

The framework should make it difficult for an AI agent to silently convert an assumption into a fact.

### O2 — Improve Context Efficiency

Provide only the context required for the current task rather than repeatedly loading the entire project knowledge base.

### O3 — Preserve Continuity

Allow development to continue across:

* different conversations
* different AI models
* different AI tools
* different developers
* different development sessions

without requiring the complete history of previous conversations.

### O4 — Control Scope

Prevent agents from silently expanding the scope of a task or introducing unrelated architectural changes.

### O5 — Improve Requirement Fidelity

Ensure that implementation remains traceable to explicit requirements and acceptance criteria.

### O6 — Improve Engineering Quality

Make validation a mandatory part of AI-assisted development rather than an optional final step.

### O7 — Support Different Project Types

Provide a consistent engineering model for:

* greenfield development
* existing applications
* feature development
* bug fixing
* refactoring
* migration
* modernization
* integration
* performance optimization
* maintenance

### O8 — Remain Tool Independent

The methodology must not depend on:

* Claude
* Gemini
* Antigravity
* Cursor
* Codex
* GitHub Copilot
* or any other individual AI coding product.

Tools are execution environments. AICF is the engineering methodology.

---

## 1.7 Scope

AICF covers the AI-assisted software development lifecycle from understanding a requirement through validated implementation and persistent state update.

### Included

* Project discovery
* Requirement interpretation
* Context management
* Architecture understanding
* Technical planning
* Task decomposition
* AI execution rules
* Code generation and modification
* Refactoring
* Migration planning
* Testing
* Validation
* Security considerations
* Performance considerations
* Decision recording
* Project state management
* Change management
* Agent handoff
* Context recovery
* AI tool interoperability

### Not Included

AICF does not attempt to replace:

* product management
* UX research
* human architectural ownership
* engineering leadership
* code review by humans where required
* organizational governance
* deployment infrastructure
* source control
* project management systems

AICF can integrate with these disciplines and tools but does not attempt to become a replacement for them.

---

## 1.8 Target Users

AICF is intended for:

### Individual Developers

Developers using AI coding assistants to accelerate implementation while retaining engineering discipline.

### Engineering Teams

Teams using AI agents across multiple developers and projects.

### Engineering Managers

Leaders who need consistency, traceability, quality controls, and predictable AI-assisted development.

### Product Engineers

Engineers working across product requirements, architecture, implementation, and validation.

### AI-Assisted Development Teams

Teams where multiple AI agents or AI platforms participate in the same project.

### Technical Consultants

Engineers working across different client codebases, technology stacks, and development environments.

---

## 1.9 Supported Development Scenarios

AICF must support the following primary scenarios.

### Greenfield

A completely new application or product.

```text
Discovery
→ Requirements
→ Architecture
→ Foundation
→ Feature Development
→ Validation
→ Release
```

### Existing Application

Development within an existing codebase.

```text
Repository Discovery
→ Architecture Reconstruction
→ Current-State Understanding
→ Change Definition
→ Implementation
→ Regression Validation
```

### Migration

Moving from an existing technology, architecture, or platform to another.

```text
Source Analysis
→ Target Definition
→ Gap Analysis
→ Migration Strategy
→ Incremental Migration
→ Parity Validation
→ Decommission
```

### Feature Development

Adding functionality to an existing system.

```text
Requirement
→ Context
→ Plan
→ Implementation
→ Validation
```

### Bug Fix

Resolving an existing defect.

```text
Reproduce
→ Investigate
→ Identify Root Cause
→ Implement Minimal Fix
→ Regression Test
→ Validate
```

### Refactoring

Improving internal implementation without intentionally changing externally observable behaviour.

```text
Current Behaviour
→ Refactoring Plan
→ Controlled Change
→ Behaviour Validation
```

### Optimization

Improving measurable characteristics such as:

* performance
* bundle size
* infrastructure cost
* database efficiency
* accessibility
* maintainability

Optimization must remain evidence-driven rather than assumption-driven.

---

## 1.10 Fundamental AICF Principle

AICF establishes the following fundamental principle:

> **The AI agent is not the system of record. The repository and its structured engineering artifacts are the system of record.**

The AI agent may:

* interpret
* analyze
* plan
* implement
* test
* recommend
* identify risks

But persistent project knowledge must exist independently of the agent's conversation.

This allows:

```text
Agent A
   ↓
Project State
   ↓
Agent B
   ↓
Project State
   ↓
Agent C
```

without requiring the agents to share conversational memory.

---

## 1.11 AI as an Engineering Executor

AICF does not treat an AI agent as a passive code generator.

The agent may perform meaningful engineering work, but within defined boundaries.

The agent should:

* understand before modifying
* inspect before assuming
* plan before complex implementation
* identify uncertainty
* respect project rules
* respect task scope
* use existing architecture where appropriate
* validate its work
* record important changes
* stop when required information is unavailable

The agent should not:

* invent requirements
* silently change architecture
* silently expand scope
* overwrite established decisions without justification
* claim validation that was not performed
* treat assumptions as facts
* conceal uncertainty
* optimize unrelated areas merely because they are discoverable

---

## 1.12 Success Criteria

AICF will be considered successful if a development team can:

### SC01 — Start a New Project

Give an AI agent a structured project context and progressively build the application without relying on a long conversational history.

### SC02 — Resume Development

Terminate an AI session and start a new session that can correctly understand the current project state and continue development.

### SC03 — Change AI Tools

Move development between different AI coding agents without losing essential project context.

### SC04 — Control Scope

Prevent an agent from making unrelated changes without explicit authorization.

### SC05 — Handle Uncertainty

Cause the agent to identify missing information rather than confidently inventing an implementation.

### SC06 — Reduce Context Cost

Avoid repeatedly supplying unnecessary project information to the AI.

### SC07 — Preserve Decisions

Ensure architectural and product decisions remain available to future agents.

### SC08 — Validate Output

Ensure generated or modified code is validated against appropriate quality gates.

### SC09 — Support Multiple Project Types

Apply the same framework to greenfield, existing, migration, bugfix, and other engineering scenarios.

### SC10 — Remain Tool Independent

The same AICF project structure should remain useful regardless of which AI coding agent executes the work.

---

## 1.13 Guiding Statement

AICF can be summarized as:

> **Structure the context. Bound the work. Expose uncertainty. Control the change. Validate the result. Preserve the state.**

This statement represents the intended behaviour of the framework and will serve as the foundation for the subsequent AICF specifications.

---

## 1.14 Relationship to Subsequent Phases

This charter defines **what AICF is and why it exists**.

It does not yet define the actual Markdown implementation.

The subsequent phases will translate this charter into an executable framework:

```text
Phase 1
Framework Definition
        ↓
Phase 2
Markdown Architecture
        ↓
Phase 3
Project Templates
        ↓
Phase 4
AI Tool Adapters
        ↓
Phase 5
Benchmark Project
        ↓
Phase 6+
Framework Iteration
```

Phase 1 will remain the authoritative conceptual foundation unless explicitly revised through a documented framework decision.
