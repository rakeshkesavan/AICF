# AICF-003A --- Detection Result Schema Specification

**Status:** Draft\
**Version:** 0.1.0\
**Parent Specification:** AICF-003 --- Repository Detection
Specification\
**Scope:** Machine-readable contract for repository detection results\
**Implementation Status:** Specification only

------------------------------------------------------------------------

## 1. Purpose

This specification defines the machine-readable structure returned by
the AICF Repository Detection capability.

AICF-003 defines **what detection means**. AICF-003A defines **how the
detection result is represented**.

The result is an observation contract:

``` text
Repository
    ↓
Detection
    ↓
DetectionResult
    ↓
Profile Selection
    ↓
Bootstrap
```

A `DetectionResult` MUST NOT itself select an AICF profile or generate
`.aicf/` artifacts.

------------------------------------------------------------------------

## 2. Design Goals

The result schema MUST:

1.  represent repository identity and boundary information;
2.  represent AICF discovery status;
3.  represent detected technologies;
4.  represent confidence;
5.  preserve evidence;
6.  represent conflicts and ambiguity;
7.  represent workspace/monorepo signals;
8.  represent diagnostics;
9.  use repository-relative paths;
10. remain vendor-neutral;
11. be deterministic and serializable;
12. permit future detection categories without redesigning the core
    model.

------------------------------------------------------------------------

## 3. Top-Level Structure

The conceptual result is:

``` json
{
  "repository": {},
  "aicf": {},
  "languages": [],
  "frameworks": [],
  "runtimes": [],
  "packageManagers": [],
  "buildSystems": [],
  "testFrameworks": [],
  "workspace": {},
  "diagnostics": []
}
```

All top-level fields SHOULD be explicitly defined by the schema.

Unknown top-level fields SHOULD be rejected.

------------------------------------------------------------------------

# 4. `repository`

The `repository` object describes the detected repository boundary and
version-control context.

Conceptually:

``` json
{
  "repository": {
    "root": ".",
    "vcs": {
      "id": "git",
      "detected": true
    }
  }
}
```

## 4.1 `root`

Required.

The repository root MUST be represented as a repository-relative path.

For the repository itself:

``` text
.
```

Examples:

``` text
.
apps/web
services/orders
```

Machine-specific absolute paths MUST NOT be allowed.

## 4.2 `vcs`

Optional.

The initial schema supports:

``` text
git
```

The schema SHOULD permit future VCS identifiers without requiring a
schema redesign.

The absence of VCS detection MUST NOT prevent technology detection.

------------------------------------------------------------------------

# 5. `aicf`

The `aicf` object represents discovery of an applicable `.aicf/`
installation.

Conceptually:

``` json
{
  "aicf": {
    "status": "NOT_FOUND"
  }
}
```

Allowed statuses:

``` text
NOT_FOUND
FOUND_VALID_CANDIDATE
FOUND_PARTIAL
FOUND_INVALID
MULTIPLE_APPLICABLE
```

The detection result MUST NOT repair or mutate the detected AICF
installation.

Detailed semantic validation belongs to AICF validation capabilities.

------------------------------------------------------------------------

# 6. Technology Detection Entries

The following top-level categories use a common detection-entry
structure:

``` text
languages[]
frameworks[]
runtimes[]
packageManagers[]
buildSystems[]
testFrameworks[]
```

Each entry conceptually contains:

``` json
{
  "id": "typescript",
  "confidence": "HIGH",
  "evidence": []
}
```

------------------------------------------------------------------------

# 7. Canonical Identifiers

Detection identifiers MUST use normalized machine-readable IDs.

Initial conventions:

``` text
typescript
javascript
java
python
go
rust

angular
react
nextjs
spring

node
jvm
python
go

npm
pnpm
yarn
bun

vite
webpack
nx
turborepo
maven
gradle

vitest
jest
playwright
cypress
junit
```

Identifiers SHOULD be lowercase and stable.

Human-readable display names are outside the core detection contract.

The identifier namespace is intentionally extensible.

------------------------------------------------------------------------

# 8. Confidence

Each detected technology entry MUST contain a confidence value.

Allowed values:

``` text
HIGH
MEDIUM
LOW
UNKNOWN
```

Confidence is categorical rather than numeric.

The schema MUST NOT require arbitrary probability values such as:

``` text
0.87
92%
```

Confidence SHOULD be assigned by deterministic detection rules.

------------------------------------------------------------------------

# 9. Evidence

Each technology entry SHOULD contain one or more evidence records.

Conceptually:

``` json
{
  "type": "file",
  "path": "angular.json",
  "detail": "Angular workspace configuration detected"
}
```

Evidence types initially include:

``` text
file
directory
configuration
dependency
lockfile
workspace-definition
content-pattern
```

------------------------------------------------------------------------

# 10. Evidence Paths

Evidence paths MUST be repository-relative.

Valid:

``` text
angular.json
package.json
apps/web/package.json
pnpm-workspace.yaml
```

Invalid:

``` text
D:\Work\web-uingular.json
```

``` text
file:///d:/Work/web-ui/angular.json
```

Evidence paths MUST NOT escape the repository boundary.

Path traversal such as:

``` text
../../package.json
```

MUST be rejected.

------------------------------------------------------------------------

# 11. Evidence Detail

`detail` is optional human-readable explanatory information.

It MAY describe why the evidence supports the detection.

Example:

``` json
{
  "type": "dependency",
  "path": "package.json",
  "detail": "@angular/core is declared as a dependency"
}
```

The schema SHOULD NOT attempt to encode every possible detector-specific
explanation.

------------------------------------------------------------------------

# 12. Multiple Detections

A category MAY contain multiple entries.

Example:

``` json
{
  "languages": [
    {
      "id": "typescript",
      "confidence": "HIGH",
      "evidence": []
    },
    {
      "id": "java",
      "confidence": "HIGH",
      "evidence": []
    }
  ]
}
```

The detector MUST NOT force a single language, framework, runtime, or
test framework when multiple valid detections exist.

------------------------------------------------------------------------

# 13. Conflicts

Some categories may contain conflicting candidates.

The result MUST have a representation for conflict.

Recommended structure:

``` json
{
  "packageManagers": {
    "status": "CONFLICT",
    "candidates": [
      {
        "id": "npm",
        "confidence": "MEDIUM",
        "evidence": []
      },
      {
        "id": "pnpm",
        "confidence": "HIGH",
        "evidence": []
      }
    ]
  }
}
```

However, because the initial category model uses arrays, the exact
conflict representation MUST be finalized consistently before
implementation.

The key requirement is:

> The detector MUST NOT silently choose one candidate when strong
> evidence conflicts.

------------------------------------------------------------------------

# 14. Workspace

The `workspace` object represents workspace or monorepo signals.

Conceptually:

``` json
{
  "workspace": {
    "detected": true,
    "manager": "pnpm",
    "patterns": [
      "apps/*",
      "packages/*"
    ]
  }
}
```

## 14.1 `detected`

Boolean.

Indicates whether workspace/monorepo evidence was found.

## 14.2 `manager`

Optional normalized identifier.

Examples:

``` text
npm
pnpm
yarn
nx
turborepo
```

## 14.3 `patterns`

Optional array of repository-relative workspace patterns.

Examples:

``` text
apps/*
packages/*
```

The schema MUST prevent absolute paths and traversal.

Deep project classification is intentionally outside AICF-003A v0.1.

------------------------------------------------------------------------

# 15. Diagnostics

The `diagnostics` array represents detection warnings, errors, and
informational messages.

Conceptually:

``` json
{
  "severity": "WARNING",
  "code": "DETECTOR_CONFLICTING_PACKAGE_MANAGERS",
  "message": "Multiple package manager indicators were detected.",
  "path": "package-lock.json"
}
```

## 15.1 Severity

Allowed:

``` text
ERROR
WARNING
INFO
```

## 15.2 Code

Required stable machine-readable diagnostic identifier.

Examples:

``` text
DETECTOR_AICF_NOT_FOUND
DETECTOR_CONFLICTING_PACKAGE_MANAGERS
DETECTOR_MULTIPLE_PROJECT_ROOTS
DETECTOR_UNREADABLE_FILE
```

## 15.3 Message

Required human-readable diagnostic description.

## 15.4 Path

Optional repository-relative path.

------------------------------------------------------------------------

# 16. Unknown and Empty Results

A category SHOULD be represented as an empty array when no candidates
were detected:

``` json
{
  "frameworks": []
}
```

An individual detection SHOULD use `UNKNOWN` confidence only when a
candidate exists but its confidence cannot be established.

The detector MUST NOT manufacture an entry merely to represent absence.

------------------------------------------------------------------------

# 17. Detection Status vs Detection Absence

These are different concepts.

Example:

``` text
languages: []
```

means no language was detected.

Whereas:

``` text
languages:
  TypeScript
  confidence: UNKNOWN
```

means TypeScript was identified as a candidate but confidence could not
be established.

The schema MUST preserve this distinction.

------------------------------------------------------------------------

# 18. Repository Boundary Ambiguity

If multiple project roots are detected, diagnostics MUST be able to
represent the ambiguity.

Example:

``` json
{
  "diagnostics": [
    {
      "severity": "WARNING",
      "code": "DETECTOR_MULTIPLE_PROJECT_ROOTS",
      "message": "Multiple plausible project roots were detected."
    }
  ]
}
```

The result MUST NOT silently expose a machine-specific path as the
selected root.

The exact multi-root representation is deferred until the
repository-boundary rules are finalized.

------------------------------------------------------------------------

# 19. Vendor Neutrality

The core schema MUST remain vendor-neutral.

The following MUST NOT become core detection categories:

``` text
cursor
claude
gemini
antigravity
openai
anthropic
google
```

If a future adapter needs additional information, it MUST use an
extension mechanism defined by a later specification.

------------------------------------------------------------------------

# 20. Determinism

A serialized DetectionResult SHOULD be stable for unchanged repository
content.

The schema SHOULD therefore avoid fields such as:

``` text
timestamp
machine hostname
absolute path
local username
installed global tool versions
```

Transient execution metadata SHOULD remain outside the canonical
detection result unless a later specification explicitly defines it.

------------------------------------------------------------------------

# 21. Security Constraints

The result schema MUST constrain all paths to repository-relative
values.

It MUST reject:

``` text
absolute filesystem paths
URI schemes
drive-letter paths
path traversal
```

This applies to:

-   `repository.root`;
-   evidence paths;
-   workspace patterns where interpreted as paths;
-   diagnostic paths.

------------------------------------------------------------------------

# 22. Extensibility

The initial schema SHOULD permit future categories without allowing
arbitrary unknown core fields.

Future detection categories SHOULD be introduced through:

1.  a schema revision; or
2.  an explicitly defined extension mechanism.

The core result MUST remain predictable for consumers.

------------------------------------------------------------------------

# 23. Example --- Simple Angular Repository

Illustrative result:

``` json
{
  "repository": {
    "root": ".",
    "vcs": {
      "id": "git",
      "detected": true
    }
  },
  "aicf": {
    "status": "NOT_FOUND"
  },
  "languages": [
    {
      "id": "typescript",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "file",
          "path": "tsconfig.json"
        }
      ]
    }
  ],
  "frameworks": [
    {
      "id": "angular",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "file",
          "path": "angular.json"
        }
      ]
    }
  ],
  "runtimes": [
    {
      "id": "node",
      "confidence": "MEDIUM",
      "evidence": [
        {
          "type": "dependency",
          "path": "package.json"
        }
      ]
    }
  ],
  "packageManagers": [
    {
      "id": "npm",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "lockfile",
          "path": "package-lock.json"
        }
      ]
    }
  ],
  "buildSystems": [],
  "testFrameworks": [],
  "workspace": {
    "detected": false,
    "patterns": []
  },
  "diagnostics": []
}
```

------------------------------------------------------------------------

# 24. Example --- Monorepo

Illustrative result:

``` json
{
  "repository": {
    "root": ".",
    "vcs": {
      "id": "git",
      "detected": true
    }
  },
  "aicf": {
    "status": "NOT_FOUND"
  },
  "languages": [
    {
      "id": "typescript",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "file",
          "path": "tsconfig.json"
        }
      ]
    }
  ],
  "frameworks": [],
  "runtimes": [
    {
      "id": "node",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "file",
          "path": "package.json"
        }
      ]
    }
  ],
  "packageManagers": [
    {
      "id": "pnpm",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "lockfile",
          "path": "pnpm-lock.yaml"
        }
      ]
    }
  ],
  "buildSystems": [
    {
      "id": "turborepo",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "file",
          "path": "turbo.json"
        }
      ]
    }
  ],
  "testFrameworks": [],
  "workspace": {
    "detected": true,
    "manager": "pnpm",
    "patterns": [
      "apps/*",
      "packages/*"
    ]
  },
  "diagnostics": []
}
```

------------------------------------------------------------------------

# 25. Relationship to AICF Manifest

DetectionResult is not the manifest.

``` text
DetectionResult
    ↓
Profile Selection / Bootstrap
    ↓
.aicf/manifest.json
```

Detection may provide input to manifest creation, but transient evidence
and diagnostics do not automatically become manifest content.

------------------------------------------------------------------------

# 26. Relationship to Profile Selection

Profile selection consumes DetectionResult.

Example:

``` text
DetectionResult
    │
    ├── TypeScript / HIGH
    ├── Angular / HIGH
    ├── Node / MEDIUM
    ├── npm / HIGH
    └── workspace / false
              │
              ▼
       Profile Selection
              │
              ▼
       web-application
```

The detection schema MUST remain independent of profile names.

------------------------------------------------------------------------

# 27. Acceptance Criteria

AICF-003A is ready for implementation when:

-   top-level result structure is accepted;
-   canonical identifiers are accepted;
-   confidence model is accepted;
-   evidence model is accepted;
-   repository-relative path rules are accepted;
-   AICF discovery status is accepted;
-   diagnostics are accepted;
-   workspace representation is accepted;
-   ambiguity/conflict representation is finalized;
-   vendor neutrality is preserved;
-   the boundary between detection, profile selection, and bootstrap
    remains explicit.

------------------------------------------------------------------------

# 28. Open Decisions Before Implementation

The following should be resolved before implementation:

1.  Whether `packageManagers`, and similar categories, should always be
    arrays or support an explicit category-level `status`.
2.  Exact conflict representation.
3.  Whether `repository.vcs.detected` is necessary when `id` exists.
4.  Whether `workspace.manager` should allow multiple managers.
5.  Exact canonical identifier registry.
6.  Whether evidence `detail` should be mandatory or optional.
7.  Whether evidence should support a machine-readable `ruleId`.
8.  Whether diagnostics need a structured `relatedPaths` field.
9.  Exact multi-root representation.
10. Whether extensions belong in v0.1 or should be deferred.

------------------------------------------------------------------------

# 29. Status

**Draft --- AICF-003A**

This document defines the proposed machine-readable DetectionResult
contract.

No implementation is implied.

Implementation should begin only after the open decisions above are
resolved and this specification is accepted.
