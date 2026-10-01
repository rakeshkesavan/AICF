# AICF Schemas

## Overview

This directory will house formal machine-readable schemas (JSON Schema / YAML) defining the structural contracts for AICF projects.

## Structure

- **`manifest/`**:
  - `aicf-manifest.schema.json`: Formal JSON Schema (Draft 2020-12) for `.aicf/manifest.json` conforming to AICF-002 / AICF-002A v0.1.0.
  - `fixtures/`: Validation test fixtures covering minimal valid, fully populated valid, and all invalid failure modes.
  - `test_manifest_schema.py`: Standalone test runner for schema and fixture validation.
- **`characterization/`**:
  - `aicf-characterization-result.schema.json`: Agent-neutral characterization handoff for the Phase 1 AICF-004B workflow. Runtime validation also checks evidence path containment/existence and rejects detected secrets or workstation paths.
- **`artifacts/`**: Schemas for canonical and extended markdown artifacts (`rules.md`, `project.md`, `state.md`, `task.md`, requirements, domains, features, validation).
- **`validation/`**: Schemas and validation rule sets used by automated linters, CLI tools, and CI pipelines to enforce artifact integrity.

---

> [!NOTE]
> **Status: Active**  
> `schemas/manifest/aicf-manifest.schema.json` is implemented and verified. Conceptual schemas for artifacts are documented in [docs/02-architecture/04-canonical-artifact-schemas.md](../docs/02-architecture/04-canonical-artifact-schemas.md) and [docs/02-architecture/05-extended-artifacts.md](../docs/02-architecture/05-extended-artifacts.md).
