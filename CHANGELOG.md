# Changelog

All notable changes to the **AI Companion Framework (AICF)** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- **AICF-001**: Bootstrap & Discovery Specification (`docs/03-bootstrap/`).
- JSON/YAML schema definitions for manifest and canonical artifacts (`schemas/`).
- Initial CLI tooling architecture (`tooling/cli/`).
- Adapter contracts for Cursor, Claude, Gemini, and Antigravity (`adapters/`).

---

## [0.1.0-draft] - 2026-09-30

### Added
- **Foundation Specifications** (`docs/01-foundation/`):
  - `01-framework-charter.md`: Framework Charter, objectives, and boundaries.
  - `02-core-principles.md`: Fundamental operating philosophy.
  - `03-ai-behaviour-contract.md`: AI agent obligations, invariants, and constraints.
  - `04-operating-model.md`: Lifecycle phases, gates, and human authority.
  - `05-context-and-memory-model.md`: Working memory vs. persistent project memory.
  - `06-truth-uncertainty-and-decision-model.md`: Truth hierarchy and decision capture.
  - `07-change-and-validation-model.md`: Blast radius, change contracts, and definition of done.
  - `08-project-mode-model.md`: Execution modes across greenfield, brownfield, migration, and spikes.
- **Operational Architecture Specifications** (`docs/02-architecture/`):
  - `01-operational-architecture.md`: Mapping conceptual definition to repo structure.
  - `02-foundational-artifacts.md`: Five core artifacts (`rules`, `project`, `state`, `task`, `context`).
  - `03-artifact-stress-test.md`: Stress testing foundational artifacts across scenarios.
  - `04-canonical-artifact-schemas.md`: Canonical schema definition for foundational artifacts.
  - `05-extended-artifacts.md`: Extended schemas (`requirement`, `domain`, `feature`, `validation`).
  - `06-artifact-lifecycle-and-ai-interaction-protocol.md`: Read/create/update/validate lifecycle protocol.
  - `07-agent-protocol.md`: Tool-agnostic agent operating protocol.
  - `08-task-lifecycle-and-runtime-model.md`: Runtime task state machine.
  - `09-cross-artifact-conventions.md`: Identifiers, references, and linking standards.
  - `10-core-project-and-tool-layer.md`: Three-layer architecture and boundaries.
- **Canonical Default Template** (`templates/default/.aicf/`):
  - Pre-structured `.aicf` directory with foundational templates and folders for decisions, domains, features, requirements, tasks, and validation.
- **Repository Governance & Structure**:
  - Reorganized repository into a clean GitHub structure.
  - Added documentation placeholders for bootstrap, integrations, and guides.
  - Added community governance files (`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`).
  - Added GitHub issue templates, pull request template, and CODEOWNERS.
