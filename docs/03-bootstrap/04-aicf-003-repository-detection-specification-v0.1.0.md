# AICF-003 --- Repository Detection Specification

**Status:** Draft\
**Version:** 0.1.0\
**Parent Specifications:** AICF-001R1 --- Bootstrap & Discovery;
AICF-002 --- Manifest & Artifact Schema\
**Scope:** Passive, deterministic detection of repository and project
characteristics for AICF bootstrap and editor/agent integration\
**Implementation Status:** Specification only

## 1. Purpose

This specification defines how AICF detects the characteristics of a
repository or project before bootstrap, profile selection, or AICF
initialization.

Repository Detection is an **observation capability**. It determines
facts and evidence about the repository. It does not decide what the
repository should become, and it does not generate AICF artifacts.

The intended flow is:

``` text
Repository
    ↓
Detection
    ↓
Facts + Evidence + Confidence
    ↓
Profile Selection
    ↓
Bootstrap
```

This is the foundational capability for the cross-cutting experience:

``` text
Open repository
    ↓
Discover AICF
    ↓
If absent → detect repository
    ↓
Select appropriate AICF profile
    ↓
Preview bootstrap
    ↓
Generate .aicf/
```

## 2. Scope

This specification defines:

1.  repository boundary detection;
2.  AICF presence detection;
3.  language detection;
4.  framework detection;
5.  runtime detection;
6.  package-manager detection;
7.  build-system detection;
8.  test-framework detection;
9.  workspace/monorepo detection;
10. evidence and confidence;
11. deterministic detection;
12. passive inspection and safety;
13. ambiguity handling;
14. detection result structure;
15. consumption by later AICF capabilities.

It does **not** define profile selection, template generation, bootstrap
implementation, editor-specific integration, CLI implementation,
dependency installation, or project-code execution.

## 3. Design Principles

### 3.1 Detection is observation, not decision

The detector reports what it can establish.

It MUST NOT decide architecture, AICF profile, generated files, coding
standards, or migration targets.

### 3.2 Passive inspection

Detection MUST NOT run package scripts, application code, builds, tests,
dependency installation, modify files, or require network access.

It MAY inspect directory structure, filenames, file contents,
configuration metadata, lockfiles, workspace definitions, and
version-control metadata.

### 3.3 Deterministic results

Given the same repository state and detection rules, detection SHOULD
produce the same result.

It MUST NOT depend on AI interpretation, network responses, installed
local dependencies, machine-specific absolute paths, or transient
environment state.

### 3.4 Evidence before inference

Every meaningful detected characteristic SHOULD have identifiable
evidence.

Example:

``` text
Technology:
    TypeScript
Evidence:
    tsconfig.json
Confidence:
    HIGH
```

### 3.5 No fabricated certainty

If evidence is insufficient, the detector MUST report `UNKNOWN` or
equivalent. Weak evidence MUST NOT be promoted to high-confidence fact.

## 4. Repository Boundary Detection

Before detecting technologies, AICF MUST establish the applicable
repository/project boundary.

Possible indicators include:

``` text
.git/
package.json
pnpm-workspace.yaml
yarn.lock
package-lock.json
pom.xml
build.gradle
settings.gradle
Cargo.toml
go.mod
pyproject.toml
```

The detector SHOULD prefer explicit repository boundaries such as
version-control roots when available.

If multiple plausible roots exist, detection MUST represent the
ambiguity rather than arbitrarily selecting one.

For example:

``` text
repository/
├── frontend/
│   └── package.json
└── backend/
    └── pom.xml
```

This SHOULD be represented as a multi-project or monorepo candidate
where evidence supports it.

## 5. Existing AICF Detection

Repository Detection MUST identify whether an applicable `.aicf/`
exists.

The result SHOULD distinguish:

``` text
NOT_FOUND
FOUND_VALID_CANDIDATE
FOUND_PARTIAL
FOUND_INVALID
MULTIPLE_APPLICABLE
```

Detailed AICF qualification remains governed by AICF-001R1 and
validation capabilities.

Detection MUST NOT automatically repair an existing `.aicf/`.

## 6. Detection Categories

The initial detection model SHOULD support:

``` text
repository
languages
frameworks
runtimes
package managers
build systems
test frameworks
workspace / monorepo
```

Additional categories MAY be introduced later.

## 7. Language Detection

Language detection SHOULD use direct repository evidence.

Examples:

``` text
TypeScript → tsconfig.json
Java       → pom.xml / build.gradle / *.java
Python     → pyproject.toml / requirements.txt
Go         → go.mod / *.go
Rust       → Cargo.toml
```

The detector MAY report multiple languages.

Language presence MUST NOT imply that it is the primary runtime or
architecture.

## 8. Framework Detection

Framework detection SHOULD use explicit configuration or dependency
evidence.

Examples:

``` text
Angular  → angular.json / @angular/core
React    → react dependency / project configuration
Next.js  → next dependency / next.config.*
Spring   → Spring dependencies / Maven or Gradle configuration
```

Detection SHOULD distinguish direct, dependency, and heuristic evidence.

Multiple frameworks MAY be reported. The detector MUST NOT arbitrarily
choose one.

## 9. Runtime Detection

Runtime detection identifies execution environments supported by
repository configuration.

Examples:

``` text
Node.js → package.json engines / runtime configuration
Java    → Maven or Gradle configuration
Python  → pyproject.toml / runtime configuration
Go      → go.mod
```

A runtime version SHOULD be reported only when established from
repository configuration. The currently installed local runtime MUST NOT
be treated as the repository requirement unless explicitly configured.

## 10. Package Manager Detection

Detection SHOULD inspect lockfiles and package-manager configuration.

Examples:

``` text
npm  → package-lock.json
pnpm → pnpm-lock.yaml
Yarn → yarn.lock
Bun  → bun.lock / bun.lockb
```

If multiple package-manager indicators exist, the detector MUST report
the ambiguity instead of silently selecting one.

## 11. Build-System Detection

The detector MAY inspect:

``` text
package.json scripts
Makefile
Gradle files
Maven files
Nx configuration
Turborepo configuration
Vite configuration
Webpack configuration
Angular configuration
```

Build-system detection is evidence collection. For example, a
`vite build` script is evidence for Vite.

## 12. Test-Framework Detection

Detection SHOULD inspect configuration and dependency metadata for
frameworks such as:

``` text
Vitest
Jest
Playwright
Cypress
JUnit
```

The detector MUST NOT execute tests to establish their existence.

## 13. Workspace and Monorepo Detection

Workspace detection is important because it affects AICF scope and
bootstrap.

Potential evidence includes:

``` text
npm workspaces
pnpm-workspace.yaml
Yarn workspaces
Nx
Turborepo
multiple package manifests
workspace configuration
```

A conceptual result:

``` text
workspace:
    detected: true
type:
    monorepo
manager:
    pnpm
packages:
    packages/*
    apps/*
```

Workspace patterns SHOULD be preserved where safely extractable.

## 14. Evidence Model

Every meaningful detected characteristic SHOULD have evidence.

Conceptually:

``` json
{
  "name": "typescript",
  "confidence": "HIGH",
  "evidence": [
    {
      "type": "file",
      "path": "tsconfig.json"
    }
  ]
}
```

Evidence types MAY include:

``` text
file
directory
configuration
dependency
lockfile
workspace-definition
content-pattern
```

The final machine-readable structure is defined by the subsequent
detection-result schema specification.

## 15. Confidence Model

The initial model SHOULD use:

``` text
HIGH
MEDIUM
LOW
UNKNOWN
```

**HIGH** --- direct, unambiguous evidence.

**MEDIUM** --- strong but indirect evidence.

**LOW** --- heuristic or weak evidence.

**UNKNOWN** --- insufficient evidence.

Unknown MUST NOT be converted into a guess.

## 16. Evidence Precedence

Where multiple evidence sources exist, the detector SHOULD prefer
stronger evidence.

Conceptually:

``` text
Explicit repository configuration
        ↓
Direct configuration file
        ↓
Declared dependency
        ↓
Lockfile
        ↓
File extension/content heuristic
```

Conflicting strong evidence MUST be reported rather than silently
discarded.

## 17. Conflicting Evidence

Example:

``` text
package.json:
    packageManager = pnpm

package-lock.json:
    exists

pnpm-lock.yaml:
    exists
```

The result SHOULD indicate:

``` text
package manager:
    status: CONFLICT
    candidates:
      - pnpm
      - npm
```

The detector MUST NOT silently declare one authoritative.

## 18. Detection Result Model

The result SHOULD conceptually contain:

``` text
result
├── repository
├── aicf
├── languages
├── frameworks
├── runtimes
├── packageManagers
├── buildSystems
├── testFrameworks
├── workspace
└── diagnostics
```

Illustrative example:

``` json
{
  "repository": {
    "root": ".",
    "type": "git"
  },
  "aicf": {
    "status": "NOT_FOUND"
  },
  "languages": [
    {
      "name": "typescript",
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
      "name": "angular",
      "confidence": "HIGH",
      "evidence": [
        {
          "type": "file",
          "path": "angular.json"
        }
      ]
    }
  ]
}
```

This is conceptual only and is not the final JSON Schema.

## 19. Repository Paths

Detection results MUST NOT expose machine-specific absolute paths.

Invalid:

``` text
D:\Work\web-ui\package.json
```

Valid:

``` text
package.json
```

Nested project paths SHOULD be repository-relative:

``` text
apps/web/package.json
```

## 20. Detection Does Not Modify the Repository

Detection MUST be read-only.

It MUST NOT create `.aicf/`, modify `package.json`, modify `README.md`,
or add configuration.

Generation belongs to Bootstrap.

## 21. Detection Does Not Install Dependencies

A detector MUST NOT perform package installation or equivalent
operations.

Dependency metadata already present in repository files is sufficient
for initial detection.

## 22. Detection Does Not Execute Project Code

The detector MUST NOT invoke project scripts, builds, tests, application
startup, or custom repository executables.

## 23. Network Independence

The base detector MUST work without network access.

It MUST NOT call package registries, GitHub, framework APIs, cloud
services, or external AI models.

Optional enrichment, if introduced later, MUST remain separate from
deterministic base detection.

## 24. Performance Expectations

Detection should be lightweight enough to run when a repository is
opened in an editor.

The detector SHOULD inspect only relevant files, avoid recursively
scanning every file, and avoid generated/build/dependency directories.

It SHOULD generally avoid:

``` text
node_modules/
dist/
build/
coverage/
target/
.next/
.cache/
.git/
```

unless a specific required file is needed.

## 25. Ambiguity Handling

Detection MUST explicitly represent ambiguity.

Possible statuses:

``` text
DETECTED
NOT_DETECTED
UNKNOWN
CONFLICT
```

The detector MUST NOT hide ambiguity by choosing an arbitrary result.

## 26. Detection and Profile Selection Boundary

This is a critical architectural boundary.

Detection produces:

``` text
facts
+
evidence
+
confidence
+
diagnostics
```

Profile selection consumes those results and determines the AICF
profile.

For example:

``` text
Detection:
    TypeScript
    Angular
    npm
    Git
    single application

        ↓

Profile Selection:
    web-application
```

The detector MUST NOT directly generate `.aicf/` or select a bootstrap
template.

## 27. Detection and Manifest Boundary

Detection may provide metadata that is later persisted into
`.aicf/manifest.json`.

The two are conceptually different:

``` text
Detection Result
    ↓
Profile / Bootstrap
    ↓
Manifest
```

The manifest contains stable project metadata. Transient detector
diagnostics do not belong in the canonical manifest unless a later
specification explicitly requires them.

## 28. Detection Result Stability

Repeated detection against unchanged repository content SHOULD produce
equivalent results.

It MUST NOT vary merely because a different AI model, local global tool,
or execution time was used.

## 29. Security Requirements

Repository Detection MUST treat repository content as untrusted input.

It MUST:

-   avoid code execution;
-   constrain filesystem access to the repository boundary;
-   protect against path traversal;
-   avoid unsafe symlink traversal outside the repository;
-   avoid executing configuration-defined commands;
-   avoid network access.

## 30. Failure Model

Detection failures SHOULD be represented as diagnostics rather than
causing silent partial results.

Example:

``` text
diagnostics:
  - severity: WARNING
    code: DETECTOR_UNREADABLE_FILE
    path: package.json
```

A failure to inspect one file SHOULD NOT necessarily invalidate all
other detection results.

Fatal boundary failures MAY prevent further detection.

## 31. Diagnostics

Diagnostics SHOULD include:

``` text
severity
code
message
path (when applicable)
```

Severity:

``` text
ERROR
WARNING
INFO
```

Examples:

``` text
WARNING DETECTOR_CONFLICTING_PACKAGE_MANAGERS
WARNING DETECTOR_MULTIPLE_PROJECT_ROOTS
INFO DETECTOR_AICF_NOT_FOUND
```

Diagnostic codes SHOULD be stable enough for tooling to consume.

## 32. Initial Detection Categories --- Summary

  Category          Example evidence
  ----------------- --------------------------------
  Repository        `.git/`
  AICF              `.aicf/`
  Language          `tsconfig.json`, `pom.xml`
  Framework         `angular.json`, dependencies
  Runtime           `engines`, `pom.xml`, `go.mod`
  Package manager   lockfiles
  Build system      build configuration/scripts
  Test framework    config/dependencies
  Workspace         workspace files/configuration

The list is intentionally extensible.

## 33. Non-Goals

AICF-003 does NOT:

-   generate `.aicf/`;
-   choose the final AICF profile;
-   generate project artifacts;
-   modify repository files;
-   install dependencies;
-   execute project code;
-   execute builds/tests;
-   contact external services;
-   configure editors;
-   configure AI agents.

## 34. Future Implementation Mapping

The specification should lead to:

``` text
AICF-003
Repository Detection Specification
        │
        ▼
AICF-003A
Detection Result Schema
        │
        ▼
AICF-003B
Detection Rules / Evidence Model
        │
        ▼
Implementation
        │
        ▼
Fixtures + Tests
        │
        ▼
CI
```

Implementation should not begin until the semantic model and
detection-result contract are accepted.

## 35. Acceptance Criteria

AICF-003 is ready for implementation when:

-   repository boundary semantics are clear;
-   AICF discovery status is defined;
-   detection categories are agreed;
-   evidence model is agreed;
-   confidence model is agreed;
-   conflict handling is agreed;
-   ambiguity handling is agreed;
-   detection is explicitly passive;
-   network independence is preserved;
-   repository-relative paths are enforced;
-   detector/profile-selection boundaries are clear;
-   detector/bootstrap boundaries are clear;
-   detection-result structure is sufficiently stable.

## 36. Open Questions

The following should be resolved before implementation:

1.  Exact repository-root precedence rules when multiple roots exist.
2.  Whether `git` should be the only VCS boundary recognized initially.
3.  Exact normalized naming conventions for
    languages/frameworks/runtimes.
4.  Exact confidence calculation rules.
5.  Whether confidence should be computed or assigned by rule.
6.  Exact evidence structure.
7.  Whether detector results should be persisted for debugging.
8.  Exact monorepo/workspace representation.
9.  Symlink handling policy.
10. Maximum scan depth/performance limits.
11. Whether repository-specific detector plugins are needed later.
12. Exact diagnostic code registry.

## 37. Status

**Draft --- AICF-003**

This document defines the semantic contract for repository detection.

No implementation is implied.

The next design artifact should define the machine-readable
detection-result schema only after this specification is accepted.
