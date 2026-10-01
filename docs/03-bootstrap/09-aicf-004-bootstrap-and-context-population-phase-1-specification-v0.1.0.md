# AICF-004 — Bootstrap & Context Population — Phase 1 Specification

**Status:** Draft  
**Version:** 0.1.0  
**Phase:** Phase 1 — Way pilot  
**Implementation:** Antigravity after specification acceptance

---

## 1. Purpose

AICF-004 defines the first practical AICF workflow for piloting AICF across Way repositories.

The goal is deliberately narrow:

> Allow a developer to initialize AICF in a repository, have an agent analyze the repository, let the user choose which AICF context artifacts to populate, and then use those artifacts as repository-local engineering context for future agent work.

Phase 1 prioritizes adoption speed and practical validation over complete automation or formal repository intelligence.

---

## 2. Phase 1 Principle

The first AICF workflow is:

```text
init
  ↓
analyze
  ↓
select
  ↓
populate
  ↓
govern
```

The workflow should be simple enough to use across Way repositories without requiring a complete AICF platform.

---

## 3. Scope

Phase 1 covers:

1. detecting whether `.aicf/` exists;
2. initializing a standard `.aicf/` structure when it does not;
3. allowing an agent to analyze the repository;
4. producing proposed repository context;
5. allowing the user to choose which AICF artifacts to populate;
6. updating only the selected artifacts;
7. making existing `.aicf/` artifacts part of future agent context;
8. ensuring future agent changes conform to applicable AICF rules and project context.

---

## 4. Explicitly Out of Scope

The following are intentionally deferred:

- complete repository classification;
- sophisticated profile selection;
- formal agent confidence models;
- automatic characterization schemas;
- automatic synchronization of all AICF artifacts;
- multi-agent adapter architecture;
- editor-native UI beyond what is required for the pilot;
- AICF CLI as a separate product;
- advanced state management;
- automated task and decision management;
- full repository architectural reverse engineering;
- automatic modification of every `.aicf/` file.

These capabilities may use the architecture defined by AICF-003A through AICF-003D in later phases.

---

## 5. Phase 1 User Journey

### 5.1 New Repository

```text
Repository
    ↓
.aicf/ not found
    ↓
AICF Init
    ↓
Template .aicf/
    ↓
Repository Analysis
    ↓
Proposed Context
    ↓
User Selects Artifacts
    ↓
Populate Selected Artifacts
    ↓
AICF Ready
```

### 5.2 Existing AICF Repository

If `.aicf/` already exists:

```text
Repository
    ↓
.aicf/ found
    ↓
Read existing AICF context
    ↓
Use it during agent work
```

`init` MUST NOT overwrite an existing `.aicf/` installation.

---

## 6. Initial AICF Template

The Phase 1 template SHOULD be:

```text
.aicf/
├── README.md
├── rules.md
├── project.md
├── environment.md
└── state.md
```

Additional directories and artifacts may be introduced in later phases.

The initial template should remain small.

---

## 7. Artifact Responsibilities

### `README.md`

Describes the local AICF installation, its artifacts, and how agents should use them.

### `rules.md`

Contains repository-specific engineering rules and constraints, including coding conventions, architectural constraints, testing expectations, dependency rules, security requirements, and repository-specific practices.

The agent MUST treat applicable rules as constraints during future work.

### `project.md`

Contains repository/project context such as project purpose, technology stack, major application areas, repository structure, important modules, development conventions, and high-level architecture.

### `environment.md`

Contains development environment information such as runtime versions, package manager, build/test/development commands, required local services, and environment assumptions.

### `state.md`

Contains current AICF/project state such as work in progress, active constraints, and important unresolved items.

Phase 1 SHOULD avoid aggressive automatic population of `state.md`.

---

## 8. Initialization

Initialization creates the template only when `.aicf/` does not exist.

```text
aicf init
    ↓
.aicf/
├── README.md
├── rules.md
├── project.md
├── environment.md
└── state.md
```

Initialization MUST NOT overwrite an existing `.aicf/`, modify files outside `.aicf/`, or perform unrelated repository changes.

---

## 9. Repository Analysis

After initialization, the agent may analyze the repository.

The initial goal is to populate useful AICF context rather than reverse-engineer the entire application.

The agent SHOULD identify, where applicable:

```text
language
framework
runtime
package manager
workspace structure
major application areas
repository structure
build/test/development conventions
important engineering rules
```

The analysis MUST be evidence-based.

---

## 10. Analysis Does Not Equal Immediate Write

The agent SHOULD first produce proposed changes:

```text
Repository
    ↓
Agent Analysis
    ↓
Proposed AICF Content
    ↓
User Selection
    ↓
Write Selected Artifacts
```

The user controls which artifacts are populated.

---

## 11. User Selection

Phase 1 SHOULD allow artifact-level selection.

Example:

```text
AICF Repository Analysis

Detected:
✓ Angular
✓ TypeScript
✓ Nx
✓ npm
✓ Jest

Populate:

☑ rules.md
☑ project.md
☐ environment.md
☐ state.md

[Apply]
[Cancel]
```

The exact UI is implementation-specific.

---

## 12. Populate Operation

When the user confirms selection:

```text
Selected artifact
    ↓
Agent-generated content
    ↓
Validation
    ↓
Write/update artifact
```

Only selected artifacts may be changed by the populate operation.

---

## 13. Existing Artifact Handling

If an artifact already contains meaningful content, the system MUST NOT blindly replace it.

The agent SHOULD:

1. read the existing artifact;
2. identify relevant existing information;
3. propose additions or changes;
4. preserve valid existing content;
5. require confirmation for material destructive changes.

Phase 1 should favor additive and conservative updates.

---

## 14. User-Owned Context

AICF artifacts are repository-local engineering context.

Once a user has manually modified `rules.md`, `project.md`, or `environment.md`, the agent SHOULD treat those modifications as authoritative unless they are clearly obsolete or contradictory.

The agent MUST NOT silently rewrite user-maintained rules.

---

## 15. `rules.md` Priority

For future agent work:

```text
Agent Task
    ↓
Read .aicf/rules.md
    ↓
Read relevant .aicf/project.md
    ↓
Understand repository
    ↓
Plan implementation
    ↓
Implement
    ↓
Validate against rules
```

Repository-specific rules should influence implementation decisions.

---

## 16. Existing AICF Governance

When `.aicf/` already exists, future agent workflows SHOULD begin by reading applicable AICF artifacts.

At minimum:

```text
.aicf/README.md
.aicf/rules.md
.aicf/project.md
```

Other artifacts SHOULD be read when relevant.

For example, `environment.md` should be consulted when build/test/environment operations are involved.

---

## 17. AICF as Repository Context

Phase 1 establishes:

> `.aicf/` is repository-local engineering context for AI-assisted development.

Its purpose is not merely documentation. It is intended to influence future agent behavior.

---

## 18. Conformance During Future Work

When implementing changes in an AICF-enabled repository, the agent SHOULD:

1. discover `.aicf/`;
2. read applicable context;
3. identify relevant rules;
4. plan within those constraints;
5. implement the requested change;
6. validate the change against the AICF context.

The agent SHOULD call out conflicts between the requested task and existing AICF rules rather than silently ignoring them.

---

## 19. Rule Conflicts

If a user request conflicts with `rules.md`, the agent should surface the conflict.

Example:

```text
AICF rule:
Do not introduce new state-management libraries.

User request:
Add Redux for this feature.
```

The agent should state:

```text
This conflicts with .aicf/rules.md.
```

Phase 1 does not define a formal conflict-resolution engine.

---

## 20. Generated Content Quality

Generated AICF content SHOULD be:

- concise;
- repository-specific;
- evidence-based;
- maintainable;
- useful to future agents;
- free of local machine paths;
- free of temporary analysis artifacts;
- free of unsupported assumptions.

---

## 21. No Machine-Specific References

Generated AICF content MUST NOT contain local workstation references such as:

```text
D:\Work\web-ui\
file:///d:/Work/web-ui/
C:\Users\...
```

Repository references should be relative:

```text
apps/web/
src/components/
package.json
```

---

## 22. No Sensitive Information

Generated AICF artifacts MUST NOT contain:

```text
API keys
passwords
tokens
private keys
certificates
credentials
secrets
```

Environment documentation should describe required variables without exposing values.

---

## 23. Git Workflow

Generated `.aicf/` content is intended to be repository content.

The Phase 1 workflow SHOULD allow developers to review:

```text
git diff
```

before committing generated changes.

AICF SHOULD NOT automatically commit changes in Phase 1.

---

## 24. Validation

Phase 1 validation SHOULD include:

```text
.aicf/ exists
required template files exist
generated Markdown is valid
no obvious machine-specific paths
no obvious secrets
selected artifacts were updated
unselected artifacts were not modified
```

Formal manifest/schema validation remains a later phase unless already available and applicable.

---

## 25. Minimal Bootstrap Contract

The Phase 1 implementation can be understood as three logical operations:

### Init

```text
Ensure .aicf/ template exists.
```

### Analyze

```text
Inspect repository and propose AICF context.
```

### Apply

```text
Apply user-selected proposed context to selected artifacts.
```

The user-facing workflow can remain:

```text
Init → Analyze → Select → Apply
```

---

## 26. Existing AICF Workflow

For an existing repository:

```text
Open repository
    ↓
Discover .aicf/
    ↓
Read AICF context
    ↓
Perform requested task
    ↓
Conform to rules/project context
```

No initialization is required.

---

## 27. New Repository Workflow

For a repository without AICF:

```text
Open repository
    ↓
No .aicf/
    ↓
Init
    ↓
Analyze
    ↓
Select artifacts
    ↓
Apply
    ↓
Review diff
    ↓
Commit
```

---

## 28. Recommended Phase 1 Artifact Priority

### Tier 1

```text
rules.md
project.md
```

These provide the greatest immediate value for agent-assisted development.

### Tier 2

```text
environment.md
```

Useful for consistent development/build/test workflows.

### Tier 3

```text
state.md
```

Useful later, but lower priority because state changes frequently.

---

## 29. Why `rules.md` and `project.md` First

The pilot should prove two fundamental behaviors:

### Context understanding

```text
project.md
    ↓
Agent understands what the repository is
```

### Behavioral governance

```text
rules.md
    ↓
Agent understands how changes should be made
```

Together they establish the core AICF value proposition.

---

## 30. Phase 1 Success Criteria

The pilot is successful if a developer can:

1. open a repository without `.aicf/`;
2. initialize the standard AICF structure;
3. ask the agent to analyze the repository;
4. review the proposed context;
5. choose `rules.md` and/or `project.md`;
6. populate those artifacts;
7. review the resulting diff;
8. commit the AICF context;
9. start a subsequent development task;
10. observe the agent using the AICF context during implementation.

---

## 31. Way Pilot Success Metric

The most important pilot question is:

> **Does having AICF context materially improve the consistency and quality of subsequent agent-assisted development?**

Potential observations include:

```text
fewer repeated prompts
better adherence to conventions
fewer architectural violations
less repository rediscovery
more consistent implementation
better agent output
```

Formal measurement can be introduced later.

---

## 32. Relationship to Existing Specifications

AICF-004 does not invalidate AICF-003A through AICF-003D.

Those documents remain longer-term architecture and formalization work.

Phase 1 uses only the subset needed to deliver the bootstrap workflow.

```text
AICF-003A/003B/003C/003D
        │
        │ future formalization
        ▼
AICF mature detection/characterization
        ▲
        │
AICF-004 Phase 1
        │
        ▼
Practical Way pilot
```

---

## 33. Implementation Strategy

Implementation should begin only after this specification is accepted.

The implementation should be prompt-driven through Antigravity, consistent with the project's chosen workflow.

The implementation should initially target:

```text
AICF template
+
repository analysis
+
artifact selection
+
artifact population
+
future AICF context usage
```

Implementation should avoid building infrastructure that Phase 1 does not require.

---

## 34. Suggested Implementation Sequence

After specification acceptance:

1. Define the canonical Phase 1 `.aicf/` template.
2. Define the repository analysis prompt/workflow.
3. Define proposed artifact output.
4. Define artifact selection behavior.
5. Define safe update/merge behavior.
6. Define the future-task AICF reading/governance workflow.
7. Run the workflow against one representative Way repository.
8. Test against a second repository with different characteristics.
9. Capture lessons and update the specification.
10. Only then consider formalizing underlying schemas and automation.

---

## 35. Phase 1 Non-Goals

The pilot should not attempt to prove:

```text
perfect repository detection
perfect architectural understanding
universal agent compatibility
fully automatic bootstrap
automatic AICF maintenance
formal compliance enforcement
```

Those are later objectives.

The pilot proves the basic loop:

```text
Repository
    ↓
AICF context
    ↓
Agent uses context
    ↓
Better implementation behavior
```

---

## 36. Final Phase 1 Architecture

```text
                         Repository
                              │
                              ▼
                     ┌────────────────┐
                     │ .aicf exists?  │
                     └───────┬────────┘
                         NO  │  YES
                             │
               ┌─────────────┘
               ▼
          AICF Init
               │
               ▼
        Standard Template
               │
               └──────────────┐
                              ▼
                     Agent Repository
                         Analysis
                              │
                              ▼
                     Proposed Context
                              │
                              ▼
                       User Selection
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
              rules.md    project.md   environment.md
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                       Review / Validate
                              │
                              ▼
                         Commit AICF
                              │
                              ▼
                    Future Agent Work
                              │
                              ▼
                     Read .aicf context
                              │
                              ▼
                    Follow applicable rules
                              │
                              ▼
                         Implement
```

---

## 37. Status

**Draft — AICF-004 v0.1.0**

This specification intentionally reduces Phase 1 to a practical pilot workflow.

The next step after acceptance is **not another architecture specification**.

The next step is to create the **Antigravity implementation prompt** for AICF-004 and execute the implementation against the AICF repository.

The implementation should be evaluated against the Phase 1 success criteria before expanding the scope.
