# AICF-002 --- Manifest & Artifact Schema Specification

**Status:** Draft\
**Version:** 0.1.0\
**Parent Specification:** AICF-001R1 --- Bootstrap & Discovery\
**Scope:** Machine-readable AICF project metadata and artifact
references\
**Implementation Status:** Specification only

------------------------------------------------------------------------

## 1. Purpose

This specification defines the semantic contract for the AICF manifest
and the relationship between machine-readable metadata and the
human-readable AICF artifact set.

The purpose of the manifest is to provide a stable, machine-readable
description of an AICF project instance so that AICF-aware tooling can:

-   identify an AICF installation;
-   determine its AICF version;
-   identify the project instance;
-   understand the selected profile;
-   locate relevant AICF artifacts;
-   determine compatibility;
-   validate the installation;
-   support future migration.

The manifest is not intended to become the primary store for project
rules, requirements, architecture, decisions, or task content.

------------------------------------------------------------------------

# 2. Scope

This specification defines:

1.  manifest responsibility;
2.  manifest location;
3.  core metadata;
4.  project identity;
5.  AICF versioning;
6.  profile/template identity;
7.  repository and stack metadata;
8.  artifact references;
9.  extension boundaries;
10. compatibility;
11. validation invariants;
12. migration considerations.

This specification does NOT define the final JSON Schema syntax. The
machine-readable JSON Schema is an implementation artifact derived from
this specification.

------------------------------------------------------------------------

# 3. Canonical Manifest

The canonical machine-readable manifest SHALL be:

``` text
.aicf/manifest.json
```

The manifest represents the **AICF project instance**, not the entire
software repository.

A repository MAY contain multiple applicable AICF instances in a
monorepo, subject to the discovery and inheritance rules defined by
AICF-001R1.

------------------------------------------------------------------------

# 4. Manifest Responsibilities

The manifest SHOULD answer the following questions without requiring an
AI agent to interpret the complete AICF artifact set:

1.  Is this an AICF project?
2.  Which AICF specification/version does it use?
3.  What project instance does this manifest describe?
4.  Which AICF profile is being used?
5.  Where are the principal AICF artifacts?
6.  What compatibility information is relevant to AICF tooling?
7.  Are there declared extensions?

The manifest MUST NOT become a duplicate representation of:

-   project requirements;
-   architectural decisions;
-   coding rules;
-   task descriptions;
-   feature definitions;
-   environment instructions;
-   agent prompts.

Those belong in the appropriate AICF artifacts.

------------------------------------------------------------------------

# 5. Separation of Machine Metadata and AICF Context

The AICF project is conceptually divided into:

``` text
.aicf/
│
├── manifest.json          ← machine/tooling metadata
│
├── project.md             ← project context
├── rules.md               ← project rules
├── state.md               ← current state
├── environment.md         ← environment context
│
├── requirements/          ← requirements
├── decisions/             ← decisions
├── features/              ← feature context
├── tasks/                 ← tasks
├── domains/               ← domain context
└── validation/            ← validation artifacts
```

The manifest SHOULD identify the structure of the AICF project without
absorbing the content of those artifacts.

------------------------------------------------------------------------

# 6. Required Core Information

The manifest MUST provide sufficient information to identify the AICF
installation and determine compatibility.

At minimum, the semantic model SHALL contain:

``` text
aicf.version
project.id
project.name
profile.id
```

Additional fields MAY be required by later specifications or profiles.

------------------------------------------------------------------------

# 7. AICF Version

The manifest MUST identify the AICF specification version it conforms
to.

Conceptually:

``` json
{
  "aicf": {
    "version": "0.1"
  }
}
```

The version identifies the AICF contract, not the version of an
individual editor adapter or implementation binary.

Tooling MUST NOT assume that every newer version is automatically
compatible.

Compatibility MUST be evaluated according to explicit versioning rules.

------------------------------------------------------------------------

# 8. Project Identity

Each initialized AICF project SHOULD have a stable project identity.

Conceptually:

``` json
{
  "project": {
    "id": "..."
  }
}
```

The identity:

-   MAY be generated during initialization;
-   MUST remain stable after initialization;
-   MUST NOT be regenerated during ordinary discovery or validation;
-   MUST NOT be derived solely from the current filesystem path.

This allows a repository to move without necessarily changing its AICF
identity.

The exact identifier format is intentionally deferred.

------------------------------------------------------------------------

# 9. Project Name

The manifest SHOULD contain a human-readable project name.

Example:

``` json
{
  "project": {
    "name": "example-web-app"
  }
}
```

The project name is descriptive metadata.

It MUST NOT be treated as the unique identity of the AICF project.

------------------------------------------------------------------------

# 10. Project Mode

The manifest MAY identify the project mode/profile class.

Examples may eventually include:

``` text
application
service
library
monorepo
```

The final taxonomy is intentionally deferred.

A project mode MUST NOT be inferred solely from its display name.

------------------------------------------------------------------------

# 11. Profile and Template Identity

The selected AICF profile MUST be identifiable.

Conceptually:

``` json
{
  "profile": {
    "id": "default"
  }
}
```

A profile represents the AICF structure and conventions appropriate to a
class of repository.

A profile is distinct from repository technology detection.

For example:

``` text
Detection:
Angular + TypeScript + npm

Profile:
web-application
```

Detection provides evidence.

The profile defines the AICF project model.

------------------------------------------------------------------------

# 12. Template Version

Where an implementation uses templates, the manifest SHOULD be able to
identify the template/profile version used to initialize the project.

This is important because a project created from one template version
MUST NOT silently be treated as if it had been created from a later
template.

The exact representation is deferred until the schema implementation
phase.

------------------------------------------------------------------------

# 13. Repository and Stack Metadata

The manifest MAY contain normalized repository metadata detected during
initialization.

Examples:

``` text
repository type
language
framework
runtime
package manager
build system
test framework
workspace/monorepo characteristics
```

This information is informational and tooling-oriented.

It MUST NOT automatically become authoritative project architecture.

For example, detecting React does not mean that AICF should
automatically create an architectural rule saying the application MUST
use React.

Detection evidence and project decisions remain separate.

------------------------------------------------------------------------

# 14. Detection Evidence

Where repository detection is heuristic, the manifest SHOULD be able to
preserve useful detection evidence without turning the manifest into a
full detection log.

Conceptually:

``` text
technology: TypeScript
evidence: tsconfig.json
confidence: high
```

The final representation is deferred to AICF-003 --- Repository
Detection.

The manifest SHOULD contain only stable metadata required by downstream
tooling.

Transient detector logs SHOULD remain outside the canonical manifest.

------------------------------------------------------------------------

# 15. Artifact References

AICF tooling needs to locate the artifacts that form the project
context.

The manifest MAY provide an artifact index or canonical paths.

For example:

``` json
{
  "artifacts": {
    "project": "project.md",
    "rules": "rules.md",
    "state": "state.md",
    "environment": "environment.md"
  }
}
```

Artifact references MUST:

-   remain relative to `.aicf/`;
-   not use absolute local filesystem paths;
-   not use machine-specific paths;
-   not escape the `.aicf/` boundary unless a future specification
    explicitly permits it.

This prevents manifests from containing paths such as:

``` text
file:///d:/Work/project/...
```

or:

``` text
C:\Users\...
```

------------------------------------------------------------------------

# 16. Artifact Identity

A referenced artifact is identified primarily by its canonical relative
path.

The manifest SHOULD NOT duplicate artifact contents.

For artifacts that require stronger identity guarantees in the future,
AICF MAY introduce:

-   artifact IDs;
-   schema versions;
-   content hashes;
-   dependency relationships.

Those mechanisms are deferred until the artifact schema model requires
them.

------------------------------------------------------------------------

# 17. Artifact Categories

The manifest model SHOULD remain compatible with the existing AICF
artifact categories.

At minimum, the following conceptual areas are recognized:

``` text
requirements/
decisions/
features/
tasks/
domains/
validation/
```

The manifest SHOULD describe the existence/location of these categories
rather than embedding their content.

------------------------------------------------------------------------

# 18. Extensions

The core manifest MUST remain extensible.

AICF-specific future capabilities MAY introduce extension namespaces.

Conceptually:

``` json
{
  "extensions": {
    "example-extension": {
      "...": "..."
    }
  }
}
```

Extensions MUST NOT redefine the semantics of required core fields.

Extensions SHOULD be independently versionable where necessary.

------------------------------------------------------------------------

# 19. Vendor-Neutrality

The manifest MUST NOT require knowledge of:

-   Cursor;
-   Claude;
-   Gemini;
-   Antigravity;
-   any specific editor;
-   any specific model provider.

Editor/agent configuration belongs to the adapter layer.

A future adapter MAY reference an AICF project or maintain
adapter-specific metadata through an extension mechanism, but the AICF
core manifest MUST remain valid without any vendor adapter.

------------------------------------------------------------------------

# 20. Compatibility

AICF tooling SHOULD be able to determine whether a manifest is:

``` text
SUPPORTED
SUPPORTED_WITH_WARNINGS
OUTDATED
UNSUPPORTED
INVALID
```

Compatibility depends primarily on:

-   AICF version;
-   manifest structure;
-   required artifact compatibility;
-   profile compatibility.

A newer implementation MUST NOT silently reinterpret an incompatible
manifest.

------------------------------------------------------------------------

# 21. Validation Invariants

The following invariants SHALL apply.

### V1 --- Manifest location

The canonical manifest is:

``` text
.aicf/manifest.json
```

### V2 --- Valid JSON

The manifest MUST be valid JSON.

### V3 --- Version present

AICF version MUST be present.

### V4 --- Stable project identity

An initialized project MUST have a stable project identity.

### V5 --- Profile identity

An initialized project MUST identify its AICF profile.

### V6 --- Relative artifact references

Artifact paths MUST be repository/environment independent and relative
to `.aicf/`.

### V7 --- No vendor dependency

The core manifest MUST NOT require an editor or AI vendor.

### V8 --- No duplicated artifact content

The manifest MUST NOT become a second storage location for project
rules, requirements, decisions, or task content.

### V9 --- No silent incompatibility

Unsupported versions or incompatible structures MUST be reported
explicitly.

### V10 --- Deterministic interpretation

The same valid manifest and repository state MUST produce the same
interpretation by conformant tooling.

------------------------------------------------------------------------

# 22. Generated Metadata and Determinism

AICF distinguishes between deterministic interpretation and generated
metadata.

## Deterministic

These SHOULD be deterministic:

-   repository detection;
-   profile selection;
-   artifact resolution;
-   validation result.

## Generated

These MAY be generated once:

-   project ID;
-   creation timestamp;
-   initialization metadata.

Generated values MUST NOT cause repeated discovery or validation to
produce a different project interpretation.

------------------------------------------------------------------------

# 23. Monorepo Considerations

The manifest MUST support the possibility of multiple AICF instances.

Example:

``` text
repository/
├── .aicf/
│   └── manifest.json
│
└── packages/
    ├── web/
    │   └── .aicf/
    │       └── manifest.json
    │
    └── api/
        └── .aicf/
            └── manifest.json
```

Each manifest identifies its own AICF project instance.

The exact inheritance and artifact merge model is governed by AICF-001R1
and remains subject to a future detailed artifact-composition
specification.

------------------------------------------------------------------------

# 24. Migration

The manifest SHALL support future migration between AICF versions.

Migration MUST be explicit.

A tool MUST NOT silently rewrite an existing manifest simply because it
encounters an older version.

A migration process SHOULD:

1.  detect the current version;
2.  determine whether migration is supported;
3.  preview changes;
4.  preserve existing artifacts;
5.  validate the migrated result;
6.  report the migration.

------------------------------------------------------------------------

# 25. What Does Not Belong in the Manifest

The following SHOULD remain outside the core manifest:

-   full project requirements;
-   architecture documents;
-   coding standards;
-   security policies;
-   task descriptions;
-   feature specifications;
-   decision records;
-   secrets;
-   API keys;
-   credentials;
-   machine-specific absolute paths;
-   editor-specific prompts;
-   model-specific instructions;
-   transient detector logs.

This boundary is essential to prevent `manifest.json` from becoming an
overloaded configuration file.

------------------------------------------------------------------------

# 26. Conceptual Manifest Example

The following illustrates the semantic model only. It is NOT the final
JSON Schema.

``` json
{
  "aicf": {
    "version": "0.1"
  },
  "project": {
    "id": "stable-project-id",
    "name": "example-web-app"
  },
  "profile": {
    "id": "web-application"
  },
  "repository": {
    "type": "git",
    "languages": ["typescript"],
    "frameworks": ["angular"],
    "packageManager": "npm"
  },
  "artifacts": {
    "project": "project.md",
    "rules": "rules.md",
    "state": "state.md",
    "environment": "environment.md"
  },
  "extensions": {}
}
```

This example demonstrates the conceptual boundary only.

It does not establish the final field names, data types, enums, or JSON
Schema.

------------------------------------------------------------------------

# 27. Relationship to AICF-001R1

AICF-001R1 establishes that:

-   `.aicf/` is the AICF boundary;
-   discovery and detection are distinct;
-   initialization is explicit;
-   generated identity is stable;
-   repository detection is deterministic;
-   AICF is vendor-neutral;
-   partial installations must be handled safely.

AICF-002 translates those principles into a machine-readable metadata
contract.

------------------------------------------------------------------------

# 28. Future Implementation Mapping

This specification should lead to:

``` text
AICF-002
Manifest & Artifact Schema Specification
        │
        ▼
AICF-002A
JSON Schema
        │
        ▼
AICF-003
Repository Detection Specification
        │
        ▼
AICF-004
Bootstrap / Initialization Specification
        │
        ▼
Implementation
```

The JSON Schema SHOULD NOT be implemented until this semantic
specification is accepted.

------------------------------------------------------------------------

# 29. Open Questions

The following remain intentionally unresolved:

1.  Exact project ID format.
2.  Exact AICF versioning scheme.
3.  Exact profile ID taxonomy.
4.  Exact template version representation.
5.  Whether repository metadata should be persisted in the manifest or
    derived dynamically.
6.  Exact artifact indexing model.
7.  Whether artifact content hashes are required.
8.  Formal monorepo artifact inheritance semantics.
9.  Extension namespace/versioning rules.
10. Final JSON Schema draft/version and validation tooling.

------------------------------------------------------------------------

# 30. Acceptance Criteria

This specification is ready for JSON Schema design when:

-   manifest responsibilities are clearly separated from artifact
    content;
-   required and optional semantic fields are agreed;
-   project identity semantics are agreed;
-   versioning semantics are agreed;
-   artifact path rules are agreed;
-   vendor-neutrality is preserved;
-   monorepo behaviour is sufficiently defined;
-   compatibility and migration expectations are understood;
-   no unresolved question changes the fundamental manifest model.

------------------------------------------------------------------------

# 31. Status

**Draft --- AICF-002**

This document defines the semantic contract only.

No implementation is implied.
