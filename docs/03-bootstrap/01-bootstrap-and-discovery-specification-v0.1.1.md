# AICF-001R1 --- Bootstrap & Discovery Specification

**Status:** Draft for review\
**Version:** 0.1.1\
**Parent Specification:** AICF-001 --- Bootstrap & Discovery\
**Scope:** Cross-cutting AICF Bootstrap, Discovery, Repository
Detection, and Agent/Editor Integration\
**Implementation Status:** Specification only

------------------------------------------------------------------------

## 1. Purpose

This specification defines the cross-cutting capabilities required for
AICF to become usable across repositories and AI-assisted development
environments.

The goal is to make AICF low-friction for developers:

-   An existing `.aicf/` installation can be discovered automatically.
-   A repository without AICF can be identified as uninitialized.
-   Repository characteristics can be inspected without modifying or
    executing project code.
-   An appropriate AICF profile/template can be proposed.
-   A new `.aicf/` instance can eventually be generated safely.
-   The resulting AICF installation can be validated.
-   AI editors and agents can consume AICF through a vendor-neutral
    capability model.

This document defines the required behaviour and boundaries. It does
**not** implement the CLI, repository detector, schemas, or editor
adapters.

------------------------------------------------------------------------

# 2. Scope

This specification covers:

1.  AICF discovery
2.  Repository detection
3.  AICF initialization
4.  Template/profile selection
5.  Machine-readable project metadata
6.  Validation and conformance
7.  AICF lifecycle state
8.  Monorepo and nested-project behaviour
9.  Agent/editor integration boundaries
10. Safety, failure, and recovery behaviour

The following are explicitly deferred to subsequent implementation
phases:

-   Manifest JSON Schema
-   CLI implementation
-   Repository detection implementation
-   Template engine implementation
-   Editor-specific adapters
-   Automatic context-loading implementation

------------------------------------------------------------------------

# 3. Design Principles

Bootstrap and Discovery SHALL extend the existing AICF principles rather
than introduce a competing model.

## 3.1 Non-destructive

AICF bootstrap tooling MUST NOT overwrite, truncate, delete, or corrupt
existing source files or existing AICF artifacts without explicit
developer authorization.

## 3.2 Deterministic detection

Repository detection and profile selection MUST be deterministic.

Given the same repository state and the same detection rules, the same
repository characteristics and profile selection MUST be produced.

Generated project identity, timestamps, and other lifecycle metadata MAY
be non-deterministic, but once created they MUST remain stable unless
explicitly changed.

## 3.3 Passive inspection

Repository detection MUST use passive filesystem and configuration
inspection.

Detection MUST NOT:

-   execute arbitrary project code;
-   install dependencies;
-   invoke package lifecycle scripts;
-   modify the repository;
-   require network access.

## 3.4 Human authority

Initialization is an explicit developer-controlled operation.

Detection MAY be automatic.

Generation MUST be reviewable.

AICF MUST provide a dry-run or equivalent preview before destructive or
ambiguous changes.

## 3.5 Vendor neutrality

The AICF core specification MUST NOT depend on Cursor, Claude, Gemini,
Antigravity, or any other specific editor or agent.

Vendor-specific integration belongs to the adapter layer.

## 3.6 Minimal context

Discovery and initialization MUST not require loading the entire
repository into an AI context.

Machine-readable metadata and targeted artifact inspection SHOULD be
preferred.

------------------------------------------------------------------------

# 4. Core Conceptual Separation

The following concepts MUST remain distinct:

``` text
Discovery
    ↓
Where is AICF?

Detection
    ↓
What is this repository?

Profile Selection
    ↓
Which AICF profile applies?

Bootstrap
    ↓
What AICF project instance should be created?

Validation
    ↓
Is the resulting AICF installation conformant?

Agent/Editor Integration
    ↓
How does a development environment consume AICF?
```

These are related capabilities but are not interchangeable.

------------------------------------------------------------------------

# 5. AICF Discovery Model

## 5.1 AICF boundary

The canonical AICF boundary is:

``` text
.aicf/
```

AICF discovery begins from an arbitrary workspace/file location and
searches toward an applicable repository/project boundary.

## 5.2 Repository-root AICF

A repository-root `.aicf/` represents the project-level AICF instance.

Example:

``` text
repository/
├── .aicf/
├── src/
├── tests/
└── package.json
```

## 5.3 Nested and monorepo projects

A monorepo MAY contain:

``` text
repository/
├── .aicf/
├── packages/
│   ├── billing/
│   │   └── .aicf/
│   └── checkout/
│       └── .aicf/
└── services/
```

The root AICF instance represents repository-wide rules and conventions.

A nested AICF instance represents localized project context.

## 5.4 Precedence

When operating within a nested AICF project:

1.  Local project context takes precedence for local requirements and
    runtime/task state.
2.  Root safety invariants MUST remain authoritative.
3.  Local rules MAY add stricter requirements.
4.  Local rules MUST NOT weaken root-level safety invariants.
5.  Conflicting rules that cannot be resolved through precedence MUST be
    surfaced as validation issues rather than silently resolved.

A future specification SHALL define the formal artifact merge/precedence
model.

------------------------------------------------------------------------

# 6. AICF Installation Qualification

The presence of `.aicf/` alone MUST NOT imply that the installation is
valid.

An installation SHOULD be classified as one of:

### UNINITIALIZED

No applicable `.aicf/` instance exists.

### PARTIAL

An `.aicf/` directory exists but required foundational artifacts are
missing.

### INITIALIZED

AICF has been created but has not yet passed complete validation.

### VALID

The AICF installation satisfies the applicable structural and semantic
validation requirements.

### INVALID

The AICF installation contains structural or semantic errors that
prevent safe operation.

### OUTDATED

The installation is valid for an older AICF version but requires
migration or upgrade.

### MIGRATION_REQUIRED

The installation cannot safely be used by the current tooling until a
defined migration is performed.

The distinction between legacy installations and version migration MUST
be handled through explicit versioning rather than relying solely on
file presence.

------------------------------------------------------------------------

# 7. Machine-Readable Manifest

AICF SHOULD provide a canonical machine-readable manifest at:

``` text
.aicf/manifest.json
```

The manifest is the machine/tooling descriptor of the AICF project
instance.

It MUST NOT replace human-readable AICF artifacts.

## 7.1 Responsibilities

The manifest SHOULD provide:

-   AICF version
-   project identity
-   project name
-   project mode
-   selected profile/template
-   detected technology characteristics
-   relevant artifact locations
-   compatibility information

## 7.2 Project identity

A project identity MAY be generated during initialization.

Once generated, it MUST remain stable across repeated discovery and
validation operations.

## 7.3 Generated metadata

Fields such as:

-   project ID
-   creation timestamp
-   modification timestamp

are lifecycle metadata and are not part of deterministic repository
detection.

## 7.4 Adapter information

The core manifest MUST NOT require hard-coded vendor-specific adapter
configuration such as:

``` json
{
  "cursor": true,
  "claude": true,
  "gemini": true
}
```

Adapter-specific configuration SHOULD be represented through an
extension mechanism defined by the future adapter specification.

This keeps the AICF core vendor-neutral.

------------------------------------------------------------------------

# 8. Repository Detection Model

Repository detection is a passive inspection process.

## 8.1 Required characteristics

The detector SHOULD attempt to identify:

-   repository/project root
-   repository type
-   languages
-   frameworks
-   runtime
-   package manager
-   build system
-   test framework
-   workspace/monorepo characteristics
-   relevant existing project configuration

## 8.2 Optional characteristics

The detector MAY identify:

-   linting tools
-   formatting tools
-   deployment configuration
-   CI/CD systems
-   infrastructure configuration
-   existing AI/editor configuration

## 8.3 Confidence

Detection SHOULD support confidence or evidence levels where heuristics
may be ambiguous.

For example:

``` text
TypeScript
  Evidence: tsconfig.json
  Confidence: HIGH

Angular
  Evidence: angular.json
  Confidence: HIGH

Jest
  Evidence: package.json dependency
  Confidence: MEDIUM
```

Ambiguous results MUST NOT silently become authoritative project truth.

------------------------------------------------------------------------

# 9. Template/Profile Selection

Repository detection and template selection are separate operations.

Example:

``` text
Detection
    ↓
Angular + TypeScript + npm + workspace
    ↓
Profile matching
    ↓
web-application
```

The initial AICF template model SHOULD support a small number of
profiles such as:

``` text
default
web-application
service
monorepo
```

The final profile taxonomy SHALL be driven by actual AICF requirements
and repository evidence rather than by assumptions about specific
organizations.

## 9.1 Selection requirements

Profile selection MUST:

-   be deterministic;
-   expose the selected profile;
-   explain significant selection evidence;
-   allow developer review;
-   support explicit override when detection is ambiguous.

------------------------------------------------------------------------

# 10. Initialization Model

Conceptually, initialization is:

``` text
Discover
   ↓
Detect
   ↓
Select Profile
   ↓
Preview
   ↓
Generate
   ↓
Validate
   ↓
Report
```

## 10.1 Initialization preconditions

Before generation, the implementation MUST:

1.  determine the applicable repository/project boundary;
2.  inspect any existing `.aicf/`;
3.  determine repository characteristics;
4.  determine the proposed profile;
5.  identify files that would be created or changed;
6.  identify ambiguous or unsafe conditions.

## 10.2 Preview

Initialization SHOULD provide a dry-run mode.

The preview SHOULD show:

-   selected profile;
-   target directory;
-   files to create;
-   files to preserve;
-   files requiring merge or review;
-   generated manifest metadata;
-   expected validation result.

## 10.3 Generation

Generation SHOULD be staged/atomic where practical.

If validation of a newly generated installation fails, the
implementation SHOULD roll back the staged changes.

------------------------------------------------------------------------

# 11. Existing or Partial `.aicf/`

Initialization MUST distinguish:

``` text
No .aicf/
```

from:

``` text
Partial .aicf/
```

If `.aicf/` already exists:

-   existing artifacts MUST be inspected;
-   existing content MUST be preserved by default;
-   missing required artifacts MAY be generated;
-   conflicting content MUST be reported;
-   overwriting existing content MUST require explicit authorization.

A future repair/migration capability MAY extend this model.

------------------------------------------------------------------------

# 12. Git and Version Control Boundary

AICF SHOULD be VCS-aware but MUST NOT own version-control
initialization.

For example, AICF MAY:

-   detect Git;
-   detect repository root using VCS metadata;
-   recommend committing generated `.aicf/` artifacts.

AICF MUST NOT automatically execute:

``` text
git init
```

as part of AICF initialization.

The responsibility of initializing or configuring a version-control
system remains outside the AICF core.

------------------------------------------------------------------------

# 13. Validation & Conformance

Validation determines whether an AICF installation is safe and
structurally conformant.

Validation SHOULD operate at multiple levels.

## 13.1 Structural validation

Examples:

-   required files exist;
-   required directories exist;
-   manifest is parseable;
-   artifact paths resolve;
-   naming conventions are satisfied.

## 13.2 Semantic validation

Examples:

-   project identity is consistent;
-   manifest version is supported;
-   artifacts do not contradict required structure;
-   referenced artifacts exist;
-   lifecycle state is coherent.

## 13.3 Validation severity

Issues SHOULD use:

``` text
ERROR
WARNING
INFORMATION
```

### ERROR

Prevents an installation from being considered valid.

### WARNING

Does not prevent operation but requires attention.

### INFORMATION

Provides useful context without indicating a defect.

------------------------------------------------------------------------

# 14. Lifecycle

The conceptual lifecycle is:

``` text
UNINITIALIZED
      │
      ▼
INITIALIZED
      │
      ▼
VALID
```

Additional states:

``` text
VALID ───────────────► OUTDATED
  │                       │
  │                       ▼
  │               MIGRATION_REQUIRED
  │                       │
  └───────────────────────┘

INITIALIZED ───────────► INVALID
```

State transitions MUST have explicit validation guards.

The state of an AICF installation MUST be derivable from repository
state and AICF metadata rather than depending solely on an external
service.

------------------------------------------------------------------------

# 15. Agent and Editor Integration Boundary

AICF remains independent of the AI development environment.

An AICF-aware environment SHOULD be capable of the following
capabilities:

### Discover

Locate and identify the applicable AICF instance.

### Initialize

Offer or invoke AICF initialization through an explicit developer
action.

### Validate

Determine whether the AICF installation is conformant.

### Load Context

Retrieve relevant AICF artifacts according to task and scope.

### Refresh

Detect changes to relevant AICF artifacts and refresh applicable
context.

### Report Status

Present AICF state, version, profile, and validation status.

These are **capabilities**, not yet a concrete universal API.

The formal adapter contract is deferred to the AICF Integration
specification.

------------------------------------------------------------------------

# 16. Security Considerations

Bootstrap and Discovery MUST be designed with the assumption that
repositories may contain untrusted content.

Implementations MUST:

-   avoid executing arbitrary repository scripts during detection;
-   avoid automatic dependency installation;
-   avoid network calls unless explicitly requested by a future
    capability;
-   prevent path traversal outside the intended repository boundary;
-   detect cyclic symlinks;
-   avoid overwriting user-controlled artifacts;
-   clearly surface generated changes.

Repository content MUST be treated as data during detection.

------------------------------------------------------------------------

# 17. Failure and Recovery

Bootstrap MUST fail safely.

Examples:

### Ambiguous repository

``` text
Detection result:
Multiple possible project roots detected.

Action:
Stop and request developer selection.
```

### Existing conflicting `.aicf/`

``` text
Existing AICF artifacts conflict with selected profile.

Action:
Do not overwrite.
Report conflict.
Request explicit resolution.
```

### Validation failure

``` text
Generated AICF failed conformance validation.

Action:
Rollback staged generation.
Report validation errors.
Leave existing repository unchanged.
```

------------------------------------------------------------------------

# 18. Non-Goals

This specification does NOT define:

-   the final JSON Schema;
-   CLI implementation;
-   editor-specific integration;
-   agent-specific prompt files;
-   repository detection implementation language;
-   template rendering implementation;
-   cloud services;
-   remote AICF registries;
-   automatic Git initialization;
-   automatic dependency installation.

These are subsequent implementation/specification concerns.

------------------------------------------------------------------------

# 19. Future Implementation Mapping

The specification is intended to lead to the following implementation
sequence:

``` text
AICF-001R1
Bootstrap & Discovery Specification
        │
        ▼
AICF-002
Manifest & Artifact Schemas
        │
        ▼
AICF-003
Repository Detection
        │
        ▼
AICF-004
Bootstrap / Initialization Engine
        │
        ▼
AICF-005
Validation Engine
        │
        ▼
AICF-006
CLI
        │
        ▼
AICF-007
Adapter Contract
        │
        ▼
AICF-008+
Editor/Agent Adapters
```

This sequence intentionally separates specification from implementation.

------------------------------------------------------------------------

# 20. Open Questions

The following should remain explicitly open until the relevant design
phase:

1.  Exact manifest JSON Schema.
2.  Exact artifact inheritance/merge semantics for monorepos.
3.  Final AICF profile taxonomy.
4.  Repository detection evidence/confidence model.
5.  Exact adapter protocol.
6.  Context-loading and task-scoping algorithm.
7.  Migration strategy between AICF versions.
8.  Whether project identity should be UUID-based or use another stable
    identifier.
9.  Which generated metadata belongs in the manifest versus project
    artifacts.

------------------------------------------------------------------------

# 21. Acceptance Criteria for Implementation

An implementation based on this specification should eventually
demonstrate:

-   Existing `.aicf/` can be discovered from arbitrary workspace
    locations.
-   A repository without `.aicf/` is correctly identified as
    uninitialized.
-   Repository detection is passive and deterministic.
-   Profile selection is explainable and deterministic.
-   Initialization is previewable before writing.
-   Existing AICF content is preserved by default.
-   Generated AICF is validated immediately.
-   Failed generation does not corrupt the repository.
-   Core AICF behaviour does not depend on a specific AI vendor.
-   Editor/agent integrations can be implemented independently of the
    AICF core.

------------------------------------------------------------------------

# 22. Specification Status

This document defines the design baseline for the AICF Bootstrap &
Discovery workstream.

No implementation is implied by this specification.

Implementation SHOULD begin only after this specification and its
dependent AICF foundation/architecture documents have been reviewed and
accepted.
