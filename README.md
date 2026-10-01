# AICF — AI Companion Framework

> **A vendor-neutral framework for structured, predictable, and repeatable AI-assisted software development.**

[![Status: Specification Phase](https://img.shields.io/badge/status-specification%20phase-blue.svg)](docs/01-foundation/)
[![Specification: v0.1-draft](https://img.shields.io/badge/spec-v0.1--draft-orange.svg)](docs/01-foundation/01-framework-charter.md)
[![License: TBD](https://img.shields.io/badge/license-pending%20selection-lightgrey.svg)](CONTRIBUTING.md#governance--licensing-notes)

---

## What is AICF?

**AICF (AI Companion Framework)** provides a standard context model, behavioral contract, operational lifecycle, and artifact system for AI coding assistants.

Today, AI-assisted software development suffers from fragmented prompting, loss of architectural intent across sessions, hallucinations, and unverified changes. AICF solves this by moving engineering context, requirements, decisions, and runtime state out of transient chat windows and into **structured, repository-owned markdown artifacts**.

AICF is strictly **vendor-neutral** and designed to work across diverse AI tools—including **Cursor**, **Anthropic Claude**, **Google Gemini**, **Google Antigravity**, **GitHub Copilot**, and future autonomous engineering agents.

---

## Why AICF?

Without a structured framework, AI coding workflows encounter recurring failure modes:

| Failure Mode | Impact | How AICF Solves It |
| :--- | :--- | :--- |
| **Context Bloat & Token Waste** | Re-pasting entire documents, overflowing context windows, slow inference. | **Tiered Context Model:** Minimal viable context loaded progressively per task. |
| **Hallucination & Speculation** | Agents guessing APIs, architecture, or project standards. | **Truth Hierarchy:** Explicit truth precedence; inspect before assuming. |
| **Amnesia Across Sessions** | Context lost when switching threads, editors, or team members. | **Durable Project Memory:** State and decisions tracked directly in repository artifacts. |
| **Silent Scope Expansion** | Agent refactoring unrelated files or changing architectural boundaries. | **Behavior Contract & Gates:** Strict blast radius containment and task validation gates. |
| **Tool Lock-in** | Prompts and rules tied to a single editor or vendor syntax. | **Universal Core Layer:** Decoupled methodology from editor-specific adapters. |

---

## Core Concepts

AICF decouples the software engineering process into three distinct layers:

```text
┌────────────────────────────────────────────────────────┐
│                      AICF Core                         │
│  Universal Methodology, Principles, & Safety Invariants│
└──────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
┌───────────────────┐              ┌───────────────────┐
│   Project Layer   │              │   Tool Adapters   │
│     (.aicf/)      │              │    (Execution)    │
├───────────────────┤              ├───────────────────┤
│ • Rules & Context │              │ • Cursor Adapter  │
│ • State & Tasks   │              │ • Claude Adapter  │
│ • Decisions (ADR) │              │ • Gemini Adapter  │
│ • Requirements    │              │ • Antigravity     │
│ • Validation Logs │              │ • CLI Tooling     │
└───────────────────┘              └───────────────────┘
```

### 1. Artifacts Over Working Memory
Fleeting conversational memory is treated as volatile scratch space. Project knowledge, operational state, and architectural decisions are persisted in canonical markdown files inside `.aicf/`:
- `rules.md`: Invariant project principles, boundaries, and conventions.
- `project.md`: Project purpose, architecture, and technology stack.
- `state.md`: Active operational milestone and current objective.
- `tasks/`: Atomic units of change with bounded scopes.
- `decisions/`: Immutable records of architectural choices (ADRs).
- `validation/`: Concrete verification evidence and test results.

### 2. The Task Operating Lifecycle
Engineering requests progress through structured lifecycle gates:
$$\text{Discovery} \longrightarrow \text{Definition Gate} \longrightarrow \text{Implementation} \longrightarrow \text{Validation Gate} \longrightarrow \text{Completion}$$

- **Discovery:** Assess project context, locate files, identify existing patterns.
- **Definition Gate:** Clarify intent, state assumptions, bound blast radius.
- **Implementation:** Execute scoped changes strictly aligned with the task contract.
- **Validation Gate:** Run verification commands; never claim untested work as complete.
- **Completion:** Record state transitions and update project memory.

### 3. Agent Safety Invariants
AICF agents adhere to universal behavioral axioms:
- **Inspect before assuming:** Always verify file contents and project state before modifying code.
- **Human authority:** Critical decisions, trade-offs, and boundary expansions require human consent.
- **Never claim unverified results:** Testing and validation claims must be backed by executed commands.

---

## Repository Structure

```text
aicf/
├── README.md               # Repository overview and getting started
├── CONTRIBUTING.md         # Contribution guidelines and community process
├── SECURITY.md             # Responsible vulnerability reporting policy
├── CODE_OF_CONDUCT.md      # Contributor Covenant Code of Conduct
├── CHANGELOG.md            # Release and modification history
│
├── docs/                   # Framework documentation & specifications
│   ├── 01-foundation/      # Core framework specifications (v0.1-draft)
│   ├── 02-architecture/    # Operational architecture & artifact schemas
│   ├── 03-bootstrap/       # Discovery & initialization specification (Planned)
│   ├── 04-integrations/    # Tool adapter contracts (Planned)
│   └── 05-guides/          # Adopter and developer guides (Planned)
│
├── schemas/                # Machine-readable schemas (Planned)
│   ├── manifest/           # Project configuration schemas
│   ├── artifacts/          # Canonical markdown artifact schemas
│   └── validation/         # Validation rules and constraints
│
├── templates/              # Starter templates
│   └── default/            # Canonical starter template
│       └── .aicf/          # Standard .aicf project layout
│
├── tooling/                # Developer tooling & utilities (Planned)
│   └── cli/                # AICF CLI (aicf init, validate, status)
│
├── adapters/               # Agent & editor adapters (Planned)
│   ├── cursor/             # Cursor integration (.cursorrules)
│   ├── claude/             # Claude Code / Workspaces adapter
│   ├── gemini/             # Google Gemini CLI / extensions adapter
│   └── antigravity/        # Google Antigravity custom skills & rules
│
├── examples/               # Multi-stack reference projects (Planned)
│   ├── minimal/            # Lightweight script repository
│   ├── angular-java/       # Angular frontend + Java/Spring backend
│   ├── react-node/         # React / Next.js + Node.js application
│   └── monorepo/           # Multi-package monorepo structure
│
├── pilots/                 # Enterprise & team adoption case studies
│   └── way/                # Adoption pilot evaluation artifacts
│
└── .github/                # GitHub workflows, templates, and owners
    ├── workflows/          # Continuous integration workflows
    ├── ISSUE_TEMPLATE/     # Bug report and feature request templates
    ├── PULL_REQUEST_TEMPLATE.md
    └── CODEOWNERS          # Repository maintainer mappings
```

---

## Specification Map

### 1. Foundation (`docs/01-foundation/`)
- [01-framework-charter.md](docs/01-foundation/01-framework-charter.md): Framework mission, objectives (O1–O8), and boundaries.
- [02-core-principles.md](docs/01-foundation/02-core-principles.md): Core design philosophy and tenets.
- [03-ai-behaviour-contract.md](docs/01-foundation/03-ai-behaviour-contract.md): Agent behavioral rules, constraints, and obligations.
- [04-operating-model.md](docs/01-foundation/04-operating-model.md): Lifecycle phases, gate checks, and human escalation.
- [05-context-and-memory-model.md](docs/01-foundation/05-context-and-memory-model.md): Memory tiering and token budget efficiency.
- [06-truth-uncertainty-and-decision-model.md](docs/01-foundation/06-truth-uncertainty-and-decision-model.md): Truth hierarchy and decision recording.
- [07-change-and-validation-model.md](docs/01-foundation/07-change-and-validation-model.md): Blast radius control, change classification, and validation.
- [08-project-mode-model.md](docs/01-foundation/08-project-mode-model.md): Execution across greenfield, brownfield, migration, and spikes.

### 2. Operational Architecture (`docs/02-architecture/`)
- [01-operational-architecture.md](docs/02-architecture/01-operational-architecture.md): Translating conceptual definitions to directory structure.
- [02-foundational-artifacts.md](docs/02-architecture/02-foundational-artifacts.md): Detailed specification of the five foundational artifacts.
- [03-artifact-stress-test.md](docs/02-architecture/03-artifact-stress-test.md): Stress testing artifacts against real-world engineering situations.
- [04-canonical-artifact-schemas.md](docs/02-architecture/04-canonical-artifact-schemas.md): Structural Markdown schemas for foundational artifacts.
- [05-extended-artifacts.md](docs/02-architecture/05-extended-artifacts.md): Extended schemas for requirements, features, domains, and validation.
- [06-artifact-lifecycle-and-ai-interaction-protocol.md](docs/02-architecture/06-artifact-lifecycle-and-ai-interaction-protocol.md): Agent read/write/update protocols.
- [07-agent-protocol.md](docs/02-architecture/07-agent-protocol.md): Tool-agnostic agent operating protocol.
- [08-task-lifecycle-and-runtime-model.md](docs/02-architecture/08-task-lifecycle-and-runtime-model.md): Execution state machine and transitions.
- [09-cross-artifact-conventions.md](docs/02-architecture/09-cross-artifact-conventions.md): Identifier formats, cross-references, and metadata.
- [10-core-project-and-tool-layer.md](docs/02-architecture/10-core-project-and-tool-layer.md): Architectural boundaries and adapter constraints.

---

## Current Status & Roadmap

| Capability Area | Status | Deliverable / Reference |
| :--- | :--- | :--- |
| **Conceptual Foundation** | :white_check_mark: Complete | [docs/01-foundation/](docs/01-foundation/) |
| **Operational Architecture** | :white_check_mark: Complete | [docs/02-architecture/](docs/02-architecture/) |
| **Canonical Starter Template** | :white_check_mark: Available | [templates/default/.aicf/](templates/default/.aicf/) |
| **Repository Reorganization** | :white_check_mark: Complete | Standard GitHub layout |
| **Bootstrap & Discovery** | :white_check_mark: Specified | [AICF-001](docs/03-bootstrap/01-bootstrap-and-discovery-specification.md) |
| **Machine Schemas** | :hourglass_flowing_sand: Planned | `schemas/` (Manifest & Artifact validation) |
| **Developer CLI Tooling** | :hourglass_flowing_sand: Planned | `tooling/cli/` (`aicf init`, `validate`, `status`) |
| **Agent / Editor Adapters** | :hourglass_flowing_sand: Planned | Cursor, Claude, Gemini, Antigravity |
| **Reference Implementations** | :hourglass_flowing_sand: Planned | Full-stack & monorepo examples |

---

## How the Framework Evolves

AICF is engineered to remain stable and backward-compatible:
1. **Explicit Version Pinning:** Projects specify the AICF version they target (e.g., `AICF Version: 0.1` in `project.md`).
2. **Decoupled Evolution:** Updating AICF Core or adding tool adapters does not modify existing project artifacts.
3. **Migration as a Task:** Future migrations between major AICF versions are executed as standard AICF tasks using automated diffing and validation.
4. **Community RFCs:** Architectural extensions, schema modifications, and adapter proposals are developed openly via GitHub Discussions and Issues.

---

## Contributing

We welcome community feedback, use cases, and contributions!

Please see our [CONTRIBUTING.md](CONTRIBUTING.md) guide for details on how to propose changes, submit pull requests, and contribute to upcoming specifications.

---

*AICF is an open-source initiative dedicated to advancing the state of structured, reliable AI software engineering.*
