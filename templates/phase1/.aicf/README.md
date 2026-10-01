# AICF Local Context

This `.aicf/` directory provides repository-local engineering context for
human developers and AI coding companions.

## Purpose

AICF (AI Coding Framework) context files establish shared architectural
understanding, engineering rules, and operating environment constraints.

## Canonical Phase 1 Artifacts

- `rules.md` — Repository-specific engineering constraints, coding conventions,
  and non-negotiable rules.
- `project.md` — Project purpose, high-level architecture, technology stack,
  and repository structure.
- `environment.md` — Development, build, test, and runtime environment
  information (no secrets).
- `state.md` — Current milestone, active objectives, and known constraints.

## Governance Principles

1. Read `rules.md` and `project.md` before planning or modifying code.
2. Always follow rules defined in `rules.md`; surface conflicts explicitly.
3. Keep context files accurate, concise, and evidence-based.
4. Never store credentials, tokens, or workstation-specific paths here.
