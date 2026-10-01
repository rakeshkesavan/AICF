# AICF-002A --- Manifest JSON Schema Specification

**Status:** Draft\
**Version:** 0.1.0\
**Parent Specification:** AICF-002 --- Manifest & Artifact Schema
Specification\
**Scope:** Concrete JSON Schema contract for `.aicf/manifest.json`\
**Implementation Status:** Specification only

------------------------------------------------------------------------

## 1. Purpose

This document translates the semantic manifest model defined by AICF-002
into a concrete JSON Schema contract.

The schema is intended to allow AICF-aware tooling to validate:

``` text
.aicf/manifest.json
```

against a stable machine-readable structure.

The schema defines structural constraints only. It does not replace the
semantic validation rules defined by AICF-001R1 and AICF-002.

------------------------------------------------------------------------

# 2. Canonical Location

The canonical manifest remains:

``` text
.aicf/manifest.json
```

The schema itself belongs in the AICF repository under:

``` text
schemas/
└── manifest/
    └── aicf-manifest.schema.json
```

The schema file is a framework artifact. It is not copied into every
user repository unless an implementation explicitly requires local
schema availability.

------------------------------------------------------------------------

# 3. Schema Goals

The schema MUST:

1.  identify a valid AICF manifest;
2.  require the minimum core metadata;
3.  enforce stable structural types;
4.  prevent unknown top-level fields unless explicitly allowed;
5.  permit controlled extension namespaces;
6.  prevent absolute or machine-specific artifact paths;
7.  remain vendor-neutral;
8.  support future schema evolution.

The schema MUST NOT attempt to validate the contents of:

-   `project.md`;
-   `rules.md`;
-   `state.md`;
-   requirements;
-   decisions;
-   features;
-   tasks;
-   domains.

Those are validated by their respective artifact specifications.

------------------------------------------------------------------------

# 4. Proposed JSON Schema Dialect

Use a current JSON Schema dialect supported by the chosen validation
tooling.

The initial implementation SHOULD use:

``` text
JSON Schema Draft 2020-12
```

The exact `$schema` URI belongs in the implementation artifact.

------------------------------------------------------------------------

# 5. Top-Level Structure

Conceptually:

``` json
{
  "aicf": {},
  "project": {},
  "profile": {},
  "repository": {},
  "artifacts": {},
  "extensions": {}
}
```

The top-level object SHOULD reject unknown properties.

This prevents accidental configuration drift.

------------------------------------------------------------------------

# 6. `aicf`

The `aicf` object identifies the AICF specification contract.

Required:

``` text
aicf.version
```

Conceptually:

``` json
{
  "aicf": {
    "version": "0.1"
  }
}
```

## Constraints

-   `aicf` MUST be an object.
-   `version` MUST be a string.
-   `version` MUST be non-empty.
-   The value MUST represent an AICF specification version.

The exact version grammar SHOULD remain compatible with the versioning
policy established by the AICF architecture.

------------------------------------------------------------------------

# 7. `project`

The `project` object identifies the AICF project instance.

Required:

``` text
project.id
project.name
```

Conceptually:

``` json
{
  "project": {
    "id": "stable-project-id",
    "name": "example-web-app"
  }
}
```

## `project.id`

Constraints:

-   MUST be a string.
-   MUST be non-empty.
-   MUST be stable after initialization.
-   MUST NOT be interpreted as a filesystem path.

The exact identifier grammar is intentionally permissive in v0.1.

A future revision MAY introduce a stronger identifier format.

## `project.name`

Constraints:

-   MUST be a string.
-   MUST be non-empty.
-   SHOULD be human-readable.
-   MUST NOT be treated as globally unique identity.

------------------------------------------------------------------------

# 8. `profile`

The `profile` object identifies the AICF profile used by the project.

Required:

``` text
profile.id
```

Conceptually:

``` json
{
  "profile": {
    "id": "web-application"
  }
}
```

## Constraints

-   `profile` MUST be an object.
-   `profile.id` MUST be a non-empty string.
-   Profile identifiers SHOULD use lowercase kebab-case.
-   Profile identifiers MUST NOT encode editor/vendor names.

Optional future metadata MAY include profile versioning, but this is not
required for the first schema revision.

------------------------------------------------------------------------

# 9. `repository`

The `repository` object contains normalized repository characteristics
useful to AICF tooling.

This section is informational metadata rather than authoritative
architecture.

Example:

``` json
{
  "repository": {
    "type": "git",
    "languages": ["typescript"],
    "frameworks": ["angular"],
    "packageManager": "npm"
  }
}
```

All properties in this section SHOULD be optional.

This allows AICF manifests to remain valid even when detection cannot
determine every characteristic.

## Proposed fields

### `repository.type`

String.

Examples:

``` text
git
none
other
```

The schema SHOULD avoid an overly restrictive enum in v0.1 because
repository systems may expand.

### `repository.languages`

Array of non-empty strings.

### `repository.frameworks`

Array of non-empty strings.

### `repository.packageManager`

String.

### `repository.runtime`

String.

### `repository.buildSystem`

String.

### `repository.testFrameworks`

Array of non-empty strings.

### `repository.workspace`

Boolean indicating whether the repository is detected as a
workspace/monorepo.

Unknown or undetected characteristics SHOULD be omitted rather than
represented as fabricated values.

------------------------------------------------------------------------

# 10. `artifacts`

The `artifacts` object provides canonical references to AICF artifacts.

Example:

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

Artifact paths MUST be:

-   strings;
-   relative;
-   `.aicf/`-relative;
-   free of drive letters;
-   free of URI schemes;
-   free of absolute path prefixes;
-   free of path traversal outside `.aicf/`.

Examples that MUST be rejected:

``` text
C:\project\.aicf\project.md
```

``` text
file:///d:/Work/project/.aicf/project.md
```

``` text
../../project.md
```

Valid example:

``` text
project.md
```

or:

``` text
requirements/login.md
```

------------------------------------------------------------------------

# 11. Artifact Reference Model

The initial schema SHOULD support named artifact references rather than
requiring every possible AICF artifact category.

This allows the artifact model to evolve without forcing a manifest
update every time a new artifact category is introduced.

For example:

``` json
{
  "artifacts": {
    "project": "project.md",
    "rules": "rules.md",
    "state": "state.md",
    "requirements": "requirements",
    "tasks": "tasks"
  }
}
```

Artifact reference values MAY point to files or directories.

The manifest schema validates path safety.

Artifact existence and artifact semantics belong to the validation
layer.

------------------------------------------------------------------------

# 12. `extensions`

The `extensions` object provides controlled extensibility.

Conceptually:

``` json
{
  "extensions": {
    "example-extension": {
      "version": "1.0",
      "configuration": {}
    }
  }
}
```

The core schema SHOULD allow extension namespaces without requiring the
core AICF schema to know their internal structure.

Extension keys SHOULD:

-   be strings;
-   identify a namespace;
-   avoid reserved core names.

The extension payload MAY be an object.

Vendor-specific configuration MUST live under extensions rather than
becoming a core AICF field.

------------------------------------------------------------------------

# 13. Unknown Properties

The schema SHOULD use strict top-level validation.

Unknown top-level fields SHOULD be rejected.

This means the following is invalid:

``` json
{
  "aicf": {},
  "project": {},
  "profile": {},
  "randomConfiguration": {}
}
```

Extensions must use:

``` json
{
  "extensions": {
    "random-configuration": {}
  }
}
```

This keeps the core contract explicit while retaining extensibility.

------------------------------------------------------------------------

# 14. Required vs Optional Fields

## Required

``` text
aicf.version
project.id
project.name
profile.id
```

## Optional

``` text
repository.*
artifacts.*
extensions.*
```

This deliberately keeps the minimum valid manifest small.

AICF initialization may populate additional metadata, but tooling must
not require every detector to know every repository characteristic.

------------------------------------------------------------------------

# 15. Schema-Level Constraints

The schema SHOULD enforce:

### Type constraints

Objects, arrays, strings, booleans, and values use their declared types.

### Non-empty strings

Required identifiers and names cannot be empty.

### Unique arrays

Repository metadata arrays SHOULD contain unique values.

### Path safety

Artifact references MUST conform to the AICF-relative path rules.

### No vendor-specific core properties

The schema MUST NOT add:

``` text
cursor
claude
gemini
antigravity
openai
anthropic
google
```

as core manifest fields.

These belong to extensions/adapters.

------------------------------------------------------------------------

# 16. Semantic Validation Beyond JSON Schema

JSON Schema alone cannot enforce every AICF rule.

The implementation validation layer MUST additionally check:

1.  manifest version compatibility;
2.  project identity stability;
3.  profile availability;
4.  artifact existence;
5.  artifact semantics;
6.  monorepo inheritance;
7.  migration state;
8.  adapter extension compatibility;
9.  repository boundary rules.

Therefore:

``` text
JSON Schema validation
        +
AICF semantic validation
        =
AICF conformance validation
```

------------------------------------------------------------------------

# 17. Example Valid Manifest

The following is an illustrative valid manifest:

``` json
{
  "aicf": {
    "version": "0.1"
  },
  "project": {
    "id": "example-project",
    "name": "example-web-app"
  },
  "profile": {
    "id": "web-application"
  },
  "repository": {
    "type": "git",
    "languages": [
      "typescript"
    ],
    "frameworks": [
      "angular"
    ],
    "packageManager": "npm",
    "workspace": false
  },
  "artifacts": {
    "project": "project.md",
    "rules": "rules.md",
    "state": "state.md",
    "environment": "environment.md",
    "requirements": "requirements",
    "tasks": "tasks"
  },
  "extensions": {}
}
```

This example illustrates the intended shape only.

------------------------------------------------------------------------

# 18. Example Invalid Manifests

## Missing AICF version

``` json
{
  "project": {
    "id": "example",
    "name": "example"
  },
  "profile": {
    "id": "default"
  }
}
```

Invalid because `aicf.version` is required.

## Missing project identity

``` json
{
  "aicf": {
    "version": "0.1"
  },
  "project": {
    "name": "example"
  },
  "profile": {
    "id": "default"
  }
}
```

Invalid because `project.id` is required.

## Absolute artifact path

``` json
{
  "aicf": {
    "version": "0.1"
  },
  "project": {
    "id": "example",
    "name": "example"
  },
  "profile": {
    "id": "default"
  },
  "artifacts": {
    "project": "C:\\Work\\example\\.aicf\\project.md"
  }
}
```

Invalid because artifact paths must be `.aicf`-relative.

## Unknown core field

``` json
{
  "aicf": {
    "version": "0.1"
  },
  "project": {
    "id": "example",
    "name": "example"
  },
  "profile": {
    "id": "default"
  },
  "cursor": {
    "enabled": true
  }
}
```

Invalid because editor-specific configuration does not belong at the
AICF core level.

------------------------------------------------------------------------

# 19. Schema Evolution

The schema itself is versioned independently from the AICF specification
where necessary.

The relationship is:

``` text
AICF specification version
        │
        ▼
Manifest semantic contract
        │
        ▼
JSON Schema implementation
```

A schema change that changes the meaning of existing valid manifests
MUST be treated as a compatibility-impacting change.

Backward-compatible additions MAY be introduced without invalidating
existing manifests, subject to the compatibility policy.

------------------------------------------------------------------------

# 20. Migration Requirements

Migration MUST NOT be implemented as an implicit side effect of
validation.

The preferred lifecycle is:

``` text
Detect old manifest
       ↓
Report migration required
       ↓
Preview migration
       ↓
Apply migration
       ↓
Validate result
```

Existing artifacts MUST be preserved unless migration explicitly
requires a content transformation.

------------------------------------------------------------------------

# 21. Relationship to Artifact Schemas

The manifest schema does not define every AICF artifact.

Instead:

``` text
manifest.schema.json
        │
        ├── identifies AICF installation
        │
        └── references artifacts
                  │
                  ├── project artifact schema
                  ├── rules artifact schema
                  ├── task schema
                  ├── decision schema
                  └── requirement schema
```

Artifact-specific schemas SHOULD evolve independently while maintaining
compatibility with the manifest reference model.

------------------------------------------------------------------------

# 22. Acceptance Criteria

The JSON Schema implementation is ready when it can:

-   validate a minimal valid manifest;
-   reject missing required fields;
-   reject invalid field types;
-   reject unsafe artifact paths;
-   reject unknown core fields;
-   accept extension namespaces;
-   remain vendor-neutral;
-   validate repository metadata when supplied;
-   support manifests with optional artifact indexes;
-   work with the semantic validation layer.

------------------------------------------------------------------------

# 23. Deferred Decisions

The following remain intentionally outside the first concrete schema:

1.  exact project ID grammar;
2.  exact AICF semantic versioning policy;
3.  profile version field;
4.  artifact content hashes;
5.  detection evidence persistence;
6.  formal monorepo inheritance metadata;
7.  extension namespace registry;
8.  adapter-specific schema contracts.

These should be resolved when their respective capabilities are
specified.

------------------------------------------------------------------------

# 24. Status

**Draft --- AICF-002A**

This document defines the concrete schema requirements derived from
AICF-002.

The next implementation artifact should be:

``` text
schemas/manifest/aicf-manifest.schema.json
```

Implementation should be performed only after this schema specification
is accepted.
