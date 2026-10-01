# AICF Bootstrap & Discovery (Planned)

## Purpose

The **Bootstrap & Discovery** module defines how AICF is introduced to and maintained within a codebase. It establishes standard protocols for:

1. **Repository Discovery & Scanning:** Detecting project structure, build tools, languages, existing documentation, and conventions.
2. **Initialization Workflow:** Initializing the `.aicf/` folder (`aicf init`) and seeding foundational artifacts tailored to project archetype.
3. **Repository Detection & Profiling:** Identifying project modes (greenfield vs. brownfield, monorepo vs. standalone, library vs. service).
4. **Validation & Health Checks:** Validating repository conformity to AICF invariants, schemas, and references (`aicf validate` / `aicf doctor`).
5. **Lifecycle State Management:** Bootstrapping task runtime state, managing session context transitions, and snapshotting state.

---

## Status

> [!NOTE]
> **Specification Milestone: AICF-001 (Recommended Next Step)**  
> This capability is scheduled for detailed specification under **AICF-001 — Bootstrap & Discovery Specification**.  
> Detailed implementation and CLI commands are deliberately deferred until that specification is finalized.
