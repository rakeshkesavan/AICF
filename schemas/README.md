# AICF Schemas (Planned)

## Overview

This directory will house formal machine-readable schemas (JSON Schema / YAML) defining the structural contracts for AICF projects.

## Structure

- **`manifest/`**: Schemas for project configuration and manifest files (e.g., framework version declaration, enabled domains, active rulesets).
- **`artifacts/`**: Schemas for canonical and extended markdown artifacts (`rules.md`, `project.md`, `state.md`, `task.md`, requirements, domains, features, validation).
- **`validation/`**: Schemas and validation rule sets used by automated linters, CLI tools, and CI pipelines to enforce artifact integrity.

---

> [!NOTE]
> **Status: Planned**  
> Formal schema specifications will be implemented in sync with the CLI and validation tooling phase. Conceptual schemas are currently documented in [docs/02-architecture/04-canonical-artifact-schemas.md](../docs/02-architecture/04-canonical-artifact-schemas.md) and [docs/02-architecture/05-extended-artifacts.md](../docs/02-architecture/05-extended-artifacts.md).
