# AICF Bootstrap & Discovery (Planned)

## Purpose

The **Bootstrap & Discovery** module defines how AICF is introduced to and maintained within a codebase. It establishes standard protocols for:

1. **Repository Discovery & Scanning:** Detecting project structure, build tools, languages, existing documentation, and conventions.
2. **Initialization Workflow:** Initializing the `.aicf/` folder (`aicf init`) and seeding foundational artifacts tailored to project archetype.
3. **Repository Detection & Profiling:** Identifying project modes (greenfield vs. brownfield, monorepo vs. standalone, library vs. service).
4. **Validation & Health Checks:** Validating repository conformity to AICF invariants, schemas, and references (`aicf validate` / `aicf doctor`).
5. **Lifecycle State Management:** Bootstrapping task runtime state, managing session context transitions, and snapshotting state.

---

## Specification

- [01-bootstrap-and-discovery-specification.md](01-bootstrap-and-discovery-specification.md): **AICF-001** Normative specification defining discovery traversal, static repository detection heuristics, initialization protocol (`aicf init`), manifest concept (`manifest.json`), conformance validation, framework lifecycle states, and client integration boundaries.

---

## Status

> [!NOTE]
> **Specification Milestone: AICF-001 Complete**  
> The normative specification is defined in [01-bootstrap-and-discovery-specification.md](01-bootstrap-and-discovery-specification.md).  
> Concrete CLI implementation and tooling code are scheduled for subsequent implementation phases.
