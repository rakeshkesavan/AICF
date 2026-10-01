# AICF-004B — Agent-Driven Repository Characterization & Context Generation

**Status:** Proposed  
**Version:** v0.1.0  
**Phase:** Phase 1 Pilot

## 1. Purpose

AICF-004B defines the Phase 1 workflow for using an AI agent to characterize a repository and generate candidate AICF context.

The workflow is intentionally small and designed for rapid adoption across Way applications.

> **Deterministic tooling collects repository evidence; the agent interprets that evidence and the repository; the user approves the resulting AICF context.**

## 2. Problem Statement

The deterministic Phase 1 bootstrap analyzer can identify a limited set of repository characteristics from known manifests, configuration files, and directory structures.

This provides useful baseline evidence, but is insufficient to reliably understand arbitrary repositories.

During the `web-agencyportal` pilot, the deterministic analyzer identified TypeScript, `src/`, and `tsconfig.json`, but did not identify the application's Angular, Nx, SSR, Vitest, Express, shared-library, API-proxy, or feature-module characteristics.

An agent-driven characterization step can inspect the repository more broadly and reason about its architecture, technology, conventions, and development workflow.

## 3. Goals

AICF-004B aims to:

1. Allow AICF to work with repositories without requiring repository-specific detectors.
2. Use the agent to characterize repository/project characteristics.
3. Generate candidate `project.md` and `rules.md` content.
4. Ground significant conclusions in repository evidence.
5. Prevent unsupported assumptions from automatically becoming AICF rules.
6. Allow the user to select which proposed artifacts should be created or updated.
7. Keep deterministic bootstrap tooling as a safe foundation.
8. Establish `.aicf/` as the context consumed by future agent-driven development.

## 4. Non-Goals

Phase 1 does not attempt to:

- build a universal framework/package-manager detector;
- automatically modify source code;
- automatically refactor repositories;
- automatically create commits;
- automatically accept all agent-generated rules;
- fully automate `environment.md` or `state.md`;
- replace human review of repository governance rules;
- solve editor integration/autoselection of `.aicf/`.

Editor integration is a separate cross-cutting capability that can consume this workflow later.

## 5. Core Principle

```text
Repository
    |
    v
Deterministic Evidence
    |
    v
Agent Characterization
    |
    v
Candidate AICF Context
    |
    v
User Selection & Review
    |
    v
Approved .aicf Context
```

Responsibilities are deliberately separated.

### Deterministic layer

Responsible for safe repository inspection, known evidence collection, `.aicf/` initialization, artifact application, and validation.

### Agent layer

Responsible for deeper repository inspection, semantic characterization, architectural interpretation, identifying conventions, and proposing context with evidence.

### User layer

Responsible for selecting artifacts, reviewing proposed context, approving repository-specific rules, and resolving ambiguity.

## 6. Phase 1 Workflow

### Step 1 — Init

If `.aicf/` does not exist, initialize the canonical AICF template:

```text
.aicf/
├── README.md
├── rules.md
├── project.md
├── environment.md
└── state.md
```

`init` must not overwrite existing AICF context without explicit user intent.

### Step 2 — Analyze

Run the deterministic repository analyzer, for example:

```text
python bootstrap/bootstrap_phase1.py analyze
```

The result provides baseline evidence such as languages, frameworks, package manager, key directories, and evidence items.

This output is evidence, not the final repository characterization.

### Step 3 — Characterize

The agent performs deeper repository analysis and determines:

- repository identity and purpose;
- application/project type;
- languages;
- frameworks;
- runtime;
- package manager;
- important dependencies;
- build tooling;
- testing tooling;
- repository structure;
- development workflow;
- engineering conventions;
- architectural boundaries;
- generated/vendor files;
- agent-specific constraints.

The agent must prefer actual repository evidence over assumptions.

## 7. Evidence Requirements

Every significant characterization should have supporting repository evidence.

Preferred format:

| Finding | Evidence |
|---|---|
| Angular application | `project.json`, `package.json` |
| Vitest test runner | `vite.config.mts` |
| SSR implementation | `src/server.ts` |
| Angular module architecture | `src/app/app-module.ts` |

Evidence paths must be repository-relative.

The characterization must not include absolute workstation paths, `file:///` references, credentials, tokens, or secrets.

## 8. Proposed Artifacts

Phase 1 focuses primarily on two artifacts.

### `project.md`

Should capture relatively stable project context:

- project identity;
- purpose;
- architecture;
- technology stack;
- repository structure;
- major subsystems;
- development/build conventions.

It answers:

> **What does an agent need to understand about this project before working on it?**

### `rules.md`

Should capture repository-specific engineering constraints and AI operating rules:

- coding conventions;
- architectural boundaries;
- shared-library expectations;
- testing expectations;
- security constraints;
- runtime constraints;
- prohibited or approval-required changes;
- AICF operating invariants.

It answers:

> **How should an agent make changes safely in this repository?**

## 9. Human Selection and Review

Agent-generated context is candidate context until approved.

The proposed interface should allow selection such as:

```text
AICF Repository Characterization Complete

Detected:
✓ Angular
✓ Nx
✓ TypeScript
✓ SSR
✓ Vitest
✓ Express

Proposed AICF artifacts:

[✓] project.md
[✓] rules.md
[ ] environment.md
[ ] state.md
```

The user should be able to review proposed content before it is written.

## 10. Apply

Only selected and approved artifacts are written to `.aicf/`.

```text
characterize
     |
     v
propose
     |
     v
select
     |
     v
review
     |
     v
apply
```

The apply step must not silently modify unrelated source files.

## 11. Existing AICF Repositories

If `.aicf/` already exists, characterization must treat existing AICF artifacts as authoritative context.

The agent should:

1. read existing `.aicf/` context;
2. characterize the current repository;
3. identify relevant differences or new information;
4. propose updates;
5. show proposed changes;
6. apply only after user approval.

> **Future agent changes conform to the approved `.aicf/` context.**

Existing rules must not be silently replaced by newly inferred rules.

## 12. Handling Conflicting Evidence

If repository evidence conflicts with an existing AICF rule:

```text
Existing AICF rule
        +
Current repository evidence
        |
        v
      Conflict
        |
        v
   User review
```

The agent must surface the conflict rather than silently changing the rule.

## 13. Quality Criteria

A successful characterization should be:

- **Evidence-backed** — important conclusions have identifiable repository evidence.
- **Repository-specific** — output reflects the actual repository rather than generic framework advice.
- **Actionable** — `rules.md` contains rules that can influence future coding behavior.
- **Stable** — `project.md` focuses on durable project context rather than temporary task details.
- **Conservative** — uncertain conclusions are identified as uncertain.
- **Reviewable** — the user can understand and approve proposed changes before application.

## 14. Pilot Acceptance Criteria

The Phase 1 pilot is successful when:

1. A new repository can run `init` and receive the canonical `.aicf/` structure.
2. The deterministic analyzer provides baseline evidence.
3. An agent performs deeper repository characterization.
4. The agent identifies important repository characteristics missed by deterministic detection.
5. The agent proposes useful `project.md` and `rules.md` content.
6. Significant conclusions include repository-relative evidence.
7. The user can select which artifacts to apply.
8. Proposed content can be reviewed before application.
9. Existing `.aicf/` context is preserved and treated as authoritative.
10. No unrelated source-code modifications occur during characterization.

## 15. Reference Flow

```text
                     New Repository
                           |
                           v
                         init
                           |
                           v
                    .aicf/ template
                           |
                           v
                       analyze
                           |
                           v
                Deterministic Evidence
                           |
                           v
                    characterize
                           |
                           v
                Agent Repository Model
                           |
                           v
                       propose
                           |
                 +---------+---------+
                 |                   |
                 v                   v
             project.md          rules.md
                 |                   |
                 +---------+---------+
                           |
                           v
                      User Review
                           |
                           v
                         apply
                           |
                           v
                    Approved .aicf/
                           |
                           v
                  Future Agent Work
                           |
                           v
              Conforms to AICF Context
```

## 16. Future Extensions

The following are intentionally deferred:

- editor auto-discovery and automatic `.aicf/` context selection;
- one-command agent orchestration;
- automated environment characterization;
- automated state management;
- incremental context refresh;
- drift detection;
- context validation against repository changes;
- adapters for Claude, Gemini, Cursor, Antigravity, and other agents.

These can build on the Phase 1 characterization workflow without changing its core separation of responsibilities.

## 17. Summary

AICF-004B establishes the first practical agent-driven repository intelligence workflow.

The key architectural decision is:

> **Do not continuously expand deterministic heuristics to understand every repository. Use deterministic tooling for reliable evidence and filesystem operations, and use the agent for semantic repository characterization.**

The approved AICF context then becomes the durable contract that future AI-assisted development must follow.
