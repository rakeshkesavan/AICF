# AICF-003B --- Detection Rules & Evidence Model Specification

**Status:** Draft\
**Version:** 0.1.0\
**Parent Specification:** AICF-003 --- Repository Detection
Specification\
**Result Contract:** AICF-003A --- Detection Result Schema
Specification\
**Scope:** Deterministic rules used to produce repository detection
results\
**Implementation Status:** Specification only

------------------------------------------------------------------------

## 1. Purpose

AICF-003B defines how the repository detector turns observable
repository signals into the `DetectionResult` defined by AICF-003A.

The specification establishes:

-   detection rule structure;
-   supported indicator types;
-   rule strength and confidence;
-   evidence generation;
-   rule precedence;
-   conflicting signals;
-   negative/exclusion signals;
-   scan boundaries;
-   performance constraints;
-   rule identifiers and versioning;
-   the initial rule registry.

It does not define the implementation language, editor integration, CLI,
or profile-selection algorithm.

------------------------------------------------------------------------

## 2. Core Principle

Every positive detection SHOULD be explainable through one or more
deterministic rules and repository evidence.

Conceptually:

``` text
Repository Evidence
        ↓
Detection Rule
        ↓
Candidate
        ↓
Confidence
        ↓
Evidence
        ↓
DetectionResult
```

A detector MUST NOT produce a technology candidate solely from opaque
heuristics that cannot be traced to a defined rule.

------------------------------------------------------------------------

## 3. Detection Rule

A detection rule is a deterministic mapping between repository
indicators and a candidate technology.

Conceptually:

``` text
Rule
├── id
├── version
├── category
├── candidate
├── indicators
├── exclusions?
├── confidence
└── rationale
```

Example:

``` text
Rule ID: angular.workspace-config
Version: 1
Category: framework
Candidate: angular

Indicator:
    angular.json exists at repository root

Result:
    Angular / HIGH
```

------------------------------------------------------------------------

## 4. Rule Identifier

Every rule MUST have a stable machine-readable identifier.

Format:

``` text
<technology>.<rule-name>
```

Examples:

``` text
typescript.tsconfig
angular.workspace-config
npm.package-lock
pnpm.lockfile
node.package-config
turborepo.config
```

Rule IDs MUST NOT contain local filesystem paths.

Rule IDs SHOULD remain stable when implementation details change,
provided the semantic meaning of the rule remains the same.

------------------------------------------------------------------------

## 5. Rule Version

Each rule SHOULD have an integer version.

Example:

``` text
angular.workspace-config@1
```

The version changes when the semantic behavior of the rule changes in a
way that can affect detection results.

Implementation refactoring that does not change rule semantics SHOULD
NOT require a rule-version change.

------------------------------------------------------------------------

# 6. Rule Categories

A rule MUST target one of the AICF-003A detection categories:

``` text
language
framework
runtime
packageManager
buildSystem
testFramework
```

A rule MUST produce a candidate belonging to its declared category.

------------------------------------------------------------------------

# 7. Indicator Types

The initial indicator model supports:

``` text
file
directory
configuration
dependency
lockfile
workspace-definition
content-pattern
```

Indicators identify observable repository facts.

They are not themselves detections.

For example:

``` text
package.json
```

is evidence.

``` text
node
```

is the candidate produced by a rule.

------------------------------------------------------------------------

# 8. File Indicators

A file indicator checks for the existence of a repository-relative file.

Example:

``` text
Indicator:
    type = file
    path = angular.json
```

File existence alone MAY produce HIGH confidence when the file is
strongly specific to a technology.

Example:

``` text
angular.json
    → angular
    → HIGH
```

A generic file MUST NOT automatically produce a strong detection.

For example:

``` text
README.md
```

is not sufficient evidence for a technology detection.

------------------------------------------------------------------------

# 9. Directory Indicators

A directory indicator checks for a known repository-relative directory.

Example:

``` text
node_modules/
```

Directory indicators SHOULD generally be weaker than explicit
configuration or lockfile indicators.

Generated/dependency directories MUST be treated carefully and SHOULD
normally be excluded from recursive scanning.

------------------------------------------------------------------------

# 10. Configuration Indicators

Configuration indicators inspect known configuration files and their
relevant fields.

Example:

``` text
package.json
    dependencies:
        @angular/core
```

may produce:

``` text
angular
MEDIUM or HIGH
```

depending on the rule definition.

Configuration rules SHOULD prefer structured parsing over raw text
matching when the format is known.

------------------------------------------------------------------------

# 11. Dependency Indicators

Dependency indicators identify technology-specific packages in
dependency declarations.

Example:

``` text
package.json
    dependencies:
        @angular/core
```

produces an Angular candidate.

Dependency evidence SHOULD include:

``` json
{
  "type": "dependency",
  "path": "package.json",
  "detail": "@angular/core is declared as a dependency",
  "ruleId": "angular.core-dependency"
}
```

Dependencies alone SHOULD normally be weaker than an unambiguous
framework configuration file when such a file exists.

------------------------------------------------------------------------

# 12. Lockfile Indicators

Lockfiles provide strong evidence for package-manager detection.

Examples:

``` text
package-lock.json
    → npm

pnpm-lock.yaml
    → pnpm

yarn.lock
    → yarn

bun.lockb
    → bun
```

A package-manager lockfile SHOULD normally produce HIGH confidence.

Multiple lockfiles SHOULD produce multiple candidates plus a diagnostic
rather than silently selecting one.

------------------------------------------------------------------------

# 13. Workspace-Definition Indicators

Workspace indicators identify package/workspace declarations.

Examples:

``` text
pnpm-workspace.yaml
package.json workspaces
nx.json
turbo.json
```

Workspace indicators may contribute to:

-   package-manager detection;
-   build-system detection;
-   workspace detection.

A single indicator MAY therefore support more than one independent
detection rule.

------------------------------------------------------------------------

# 14. Content-Pattern Indicators

Content-pattern indicators inspect targeted file content.

Example:

``` text
package.json contains:
    "@angular/core"
```

Content-pattern rules MUST be targeted.

The detector MUST NOT perform unrestricted full-repository text searches
in v0.1.

------------------------------------------------------------------------

# 15. Indicator Specificity

Indicators have different evidentiary strength.

The initial conceptual ordering is:

``` text
Strongly identifying configuration
        ↓
Explicit lockfile
        ↓
Structured dependency declaration
        ↓
Workspace definition
        ↓
Known file/directory
        ↓
Generic content pattern
```

This ordering is guidance for rule design, not a universal numeric
scoring system.

Each rule explicitly declares the confidence produced when its
conditions are satisfied.

------------------------------------------------------------------------

# 16. Confidence Assignment

Rules assign categorical confidence:

``` text
HIGH
MEDIUM
LOW
UNKNOWN
```

The same candidate MAY be supported by multiple rules with different
confidence levels.

Example:

``` text
angular.workspace-config
    → Angular / HIGH

angular.core-dependency
    → Angular / MEDIUM
```

The resulting candidate SHOULD retain the strongest applicable
confidence while preserving all relevant evidence.

------------------------------------------------------------------------

# 17. Evidence Aggregation

When multiple rules identify the same candidate:

``` text
Rule A → Angular / HIGH
Rule B → Angular / MEDIUM
Rule C → Angular / LOW
```

the detector produces one Angular candidate:

``` text
Angular / HIGH
```

with evidence from all applicable rules, subject to duplicate
suppression.

The detector MUST NOT emit three separate Angular entries merely because
three rules matched.

------------------------------------------------------------------------

# 18. Duplicate Evidence

Equivalent evidence SHOULD be deduplicated.

For example, if two internal rule paths produce the same:

``` text
type
path
ruleId
```

combination, the result SHOULD contain one evidence record.

Evidence deduplication MUST NOT remove materially different evidence.

------------------------------------------------------------------------

# 19. Rule Precedence

Rules MUST NOT be implemented as an arbitrary first-match-wins chain.

All applicable rules SHOULD be evaluated within the permitted scan
boundary.

Precedence is used to determine:

-   confidence;
-   candidate aggregation;
-   conflict diagnostics;
-   preferred interpretation.

Example:

``` text
angular.json
    → Angular / HIGH

@angular/core dependency
    → Angular / MEDIUM
```

The existence of the stronger rule does not suppress the weaker
evidence.

------------------------------------------------------------------------

# 20. Conflicting Candidates

When different candidates are supported by strong evidence, the detector
MUST preserve the candidates.

Example:

``` text
package-lock.json
    → npm / HIGH

pnpm-lock.yaml
    → pnpm / HIGH
```

Result:

``` text
npm / HIGH
pnpm / HIGH
```

plus:

``` text
DETECTOR_CONFLICTING_PACKAGE_MANAGERS
```

The detector MUST NOT invent a winner.

------------------------------------------------------------------------

# 21. Non-Conflicting Multiple Technologies

Multiple technologies are not automatically conflicts.

Examples:

``` text
TypeScript + JavaScript
Angular + Node
pnpm + Turborepo
TypeScript + Java
```

The detector SHOULD represent all valid candidates.

A conflict diagnostic is appropriate only when candidates represent
mutually competing interpretations within the same semantic category or
rule-defined constraint.

------------------------------------------------------------------------

# 22. Negative and Exclusion Signals

Rules MAY define exclusion conditions.

Example:

``` text
Rule:
    react.package-dependency

Exclusion:
    dependency appears only inside an ignored/generated directory
```

Exclusions MUST be explicit.

The detector MUST NOT infer negative evidence merely from the absence of
a positive indicator unless the rule explicitly defines that absence as
meaningful.

------------------------------------------------------------------------

# 23. Absence Is Not Automatically Negative Evidence

The following is invalid reasoning:

``` text
angular.json does not exist
    ↓
therefore this is not Angular
```

A repository may use Angular without the specific configuration file
being present at the detected root.

Instead:

``` text
angular.json absent
    ↓
angular.workspace-config did not match
```

Other Angular rules may still match.

This distinction prevents false negatives.

------------------------------------------------------------------------

# 24. Generated and Dependency Directories

The detector MUST define an exclusion set for recursive inspection.

Initial default exclusions:

``` text
.git/
node_modules/
dist/
build/
coverage/
.next/
.cache/
target/
```

The exclusion list MAY be extended as additional ecosystems are
supported.

Excluded directories MUST NOT be used as the primary basis for
repository technology detection unless a specific rule explicitly
requires inspecting them.

------------------------------------------------------------------------

# 25. Repository Boundary

Rules operate within the repository boundary established by AICF-003.

A rule MUST NOT:

-   traverse above the repository root;
-   follow paths outside the repository;
-   inspect arbitrary neighboring repositories;
-   use machine-specific absolute paths as evidence.

------------------------------------------------------------------------

# 26. Symlinks

The detector MUST NOT follow symlinks outside the repository boundary.

A symlink pointing to content outside the repository MUST NOT become
evidence.

Internal symlinks MAY be followed only where doing so does not violate
the scan boundary and the behavior is deterministic.

------------------------------------------------------------------------

# 27. Scan Strategy

Detection SHOULD use targeted inspection in this order:

``` text
1. Establish repository boundary
2. Check AICF indicators
3. Check known root-level indicator files
4. Inspect known configuration files
5. Inspect package/workspace metadata
6. Inspect targeted dependency declarations
7. Inspect bounded directory structures
8. Produce candidates
9. Aggregate evidence
10. Produce diagnostics
```

The detector SHOULD avoid unrestricted recursive scanning.

------------------------------------------------------------------------

# 28. Performance Requirements

Detection is intended to support editor workflows.

Therefore:

-   common repository detection SHOULD complete quickly;
-   known indicator files SHOULD be checked before broad scanning;
-   large generated/dependency directories MUST be excluded;
-   file contents SHOULD only be read when required by an applicable
    rule;
-   the detector SHOULD avoid reading the same file repeatedly.

Implementation-specific performance thresholds are deferred until
benchmarking.

------------------------------------------------------------------------

# 29. Determinism

Given the same repository state and the same rule-set version:

``` text
Repository + Ruleset
        ↓
same DetectionResult
```

The detector SHOULD produce equivalent candidates, confidence, evidence,
and diagnostics regardless of:

-   machine hostname;
-   user account;
-   absolute workspace location;
-   execution timestamp;
-   operating-system-specific absolute path.

Ordering of arrays SHOULD be deterministic.

------------------------------------------------------------------------

# 30. Rule Evaluation Order

Rules SHOULD be grouped by detection category rather than relying on
global execution order.

Conceptually:

``` text
Language rules
Framework rules
Runtime rules
Package-manager rules
Build-system rules
Test-framework rules
Workspace rules
```

Within a category, all applicable rules SHOULD be evaluated.

This avoids hidden behavior caused by rule registration order.

------------------------------------------------------------------------

# 31. Initial Rule Registry

AICF-003B v0.1 defines an initial conceptual rule registry.

## 31.1 TypeScript

### `typescript.tsconfig`

Indicator:

``` text
tsconfig.json exists
```

Candidate:

``` text
typescript
```

Confidence:

``` text
HIGH
```

Evidence:

``` text
file
```

------------------------------------------------------------------------

## 31.2 JavaScript

### `javascript.package-config`

Indicator:

``` text
package.json exists
```

Candidate:

``` text
javascript
```

Confidence:

``` text
LOW
```

This rule is intentionally weak because `package.json` is not sufficient
to establish that JavaScript is the primary language.

A stronger JavaScript rule MAY inspect bounded source/configuration
evidence in a later ruleset.

------------------------------------------------------------------------

## 31.3 Angular

### `angular.workspace-config`

Indicator:

``` text
angular.json exists
```

Candidate:

``` text
angular
```

Confidence:

``` text
HIGH
```

### `angular.core-dependency`

Indicator:

``` text
package.json declares @angular/core
```

Candidate:

``` text
angular
```

Confidence:

``` text
MEDIUM
```

------------------------------------------------------------------------

## 31.4 React

### `react.core-dependency`

Indicator:

``` text
package.json declares react
```

Candidate:

``` text
react
```

Confidence:

``` text
MEDIUM
```

Additional stronger configuration rules MAY be introduced later.

------------------------------------------------------------------------

## 31.5 Node.js

### `node.package-config`

Indicator:

``` text
package.json exists
```

Candidate:

``` text
node
```

Confidence:

``` text
MEDIUM
```

The rule SHOULD be reviewed alongside package metadata before claiming
Node as the runtime.

------------------------------------------------------------------------

## 31.6 npm

### `npm.package-lock`

Indicator:

``` text
package-lock.json exists
```

Candidate:

``` text
npm
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.7 pnpm

### `pnpm.lockfile`

Indicator:

``` text
pnpm-lock.yaml exists
```

Candidate:

``` text
pnpm
```

Confidence:

``` text
HIGH
```

### `pnpm.workspace`

Indicator:

``` text
pnpm-workspace.yaml exists
```

Candidate:

``` text
pnpm
```

Confidence:

``` text
HIGH
```

This rule also contributes workspace evidence.

------------------------------------------------------------------------

## 31.8 Yarn

### `yarn.lock`

Indicator:

``` text
yarn.lock exists
```

Candidate:

``` text
yarn
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.9 Bun

### `bun.lockb`

Indicator:

``` text
bun.lockb exists
```

Candidate:

``` text
bun
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.10 Vite

### `vite.config`

Indicators:

``` text
vite.config.js
vite.config.mjs
vite.config.ts
```

Candidate:

``` text
vite
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.11 Nx

### `nx.config`

Indicator:

``` text
nx.json exists
```

Candidate:

``` text
nx
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.12 Turborepo

### `turborepo.config`

Indicator:

``` text
turbo.json exists
```

Candidate:

``` text
turborepo
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.13 Jest

### `jest.config`

Indicators:

``` text
jest.config.js
jest.config.ts
jest.config.mjs
```

Candidate:

``` text
jest
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.14 Vitest

### `vitest.config`

Indicators:

``` text
vitest.config.js
vitest.config.ts
vitest.config.mjs
```

Candidate:

``` text
vitest
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.15 Playwright

### `playwright.config`

Indicators:

``` text
playwright.config.js
playwright.config.ts
playwright.config.mjs
```

Candidate:

``` text
playwright
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

## 31.16 Cypress

### `cypress.config`

Indicators:

``` text
cypress.config.js
cypress.config.ts
cypress.config.mjs
```

Candidate:

``` text
cypress
```

Confidence:

``` text
HIGH
```

------------------------------------------------------------------------

# 32. Initial Rule Registry Is Not Exhaustive

The initial registry exists to establish the model and provide a
controlled implementation starting point.

It MUST NOT be interpreted as the complete AICF ecosystem registry.

Additional ecosystems SHOULD be introduced through later rule-set
revisions.

------------------------------------------------------------------------

# 33. Rule Metadata

A future executable representation MAY represent rules as:

``` json
{
  "id": "angular.workspace-config",
  "version": 1,
  "category": "framework",
  "candidate": "angular",
  "confidence": "HIGH",
  "indicators": [
    {
      "type": "file",
      "path": "angular.json"
    }
  ]
}
```

The exact executable rule format is intentionally deferred.

AICF-003B defines semantics, not implementation syntax.

------------------------------------------------------------------------

# 34. Evidence-to-Rule Traceability

A DetectionResult SHOULD allow the consumer to answer:

``` text
Why was this technology detected?
```

by following:

``` text
candidate
    ↓
evidence
    ↓
ruleId
    ↓
rule definition
    ↓
repository indicator
```

Example:

``` text
Angular / HIGH
    ↓
angular.json
    ↓
angular.workspace-config
    ↓
angular.workspace-config@1
```

This traceability is a core requirement for editor UX and debugging.

------------------------------------------------------------------------

# 35. Rule-Set Versioning

The detector SHOULD expose or internally track the rule-set version used
to produce a result.

However, the rule-set version is not part of the AICF-003A canonical
result in v0.1 unless explicitly added by a later schema revision.

Individual evidence `ruleId` and rule version provide the minimum
required traceability.

------------------------------------------------------------------------

# 36. Diagnostics Generated by Rules

Rules MAY generate diagnostics when they encounter meaningful ambiguity
or invalid combinations.

Examples:

``` text
DETECTOR_CONFLICTING_PACKAGE_MANAGERS
DETECTOR_MULTIPLE_PROJECT_ROOTS
DETECTOR_UNREADABLE_FILE
```

A rule MUST NOT generate a warning merely because another unrelated
technology is also present.

------------------------------------------------------------------------

# 37. Error Handling

An unreadable or malformed optional indicator MUST NOT necessarily
terminate the entire detection process.

Example:

``` text
package.json unreadable
```

may produce:

``` text
WARNING / DETECTOR_UNREADABLE_FILE
```

while detection continues using other indicators.

A fatal repository-boundary error MAY terminate detection.

The exact fatal/non-fatal classification is implementation-specific and
SHOULD be formalized during implementation.

------------------------------------------------------------------------

# 38. Security Model

Detection rules MUST treat repository content as untrusted input.

Rules MUST NOT:

-   execute repository scripts;
-   execute package lifecycle hooks;
-   execute build commands;
-   invoke arbitrary project tooling;
-   follow external symlinks;
-   fetch network resources;
-   inspect files outside the repository boundary.

Detection is an observation operation, not an execution operation.

------------------------------------------------------------------------

# 39. Network Independence

The initial detector MUST be network-independent.

Detection MUST NOT require:

``` text
npm registry access
Maven Central
PyPI
GitHub API
external metadata services
```

All v0.1 detection decisions must be derivable from local repository
evidence.

------------------------------------------------------------------------

# 40. Environment Independence

Detection MUST NOT require globally installed project tools.

For example, the detector should not require:

``` text
Angular CLI
Node.js CLI
Java
Python
pnpm
```

to be globally installed merely to determine whether their corresponding
repository indicators exist.

------------------------------------------------------------------------

# 41. Acceptance Criteria

AICF-003B is ready for implementation when:

-   rule structure is accepted;
-   rule IDs and versions are accepted;
-   indicator types are accepted;
-   confidence assignment is accepted;
-   evidence aggregation is accepted;
-   duplicate evidence handling is accepted;
-   conflict handling is accepted;
-   negative/exclusion behavior is accepted;
-   scan boundaries are accepted;
-   performance principles are accepted;
-   determinism requirements are accepted;
-   security restrictions are accepted;
-   network independence is accepted;
-   initial rule registry is accepted;
-   the executable rule format remains implementation-neutral.

------------------------------------------------------------------------

# 42. Status

**Draft --- AICF-003B v0.1.0**

This document defines the semantic detection-rule model.

It intentionally does not define executable rule syntax or
implementation architecture.

The next review should focus on:

1.  whether the initial rules are sufficiently conservative;
2.  whether confidence levels are justified;
3.  whether any rule can create false positives;
4.  whether the rule registry should be reduced or expanded before
    implementation;
5.  whether an executable rule schema should be created as AICF-003C.

No implementation should begin until this specification is accepted.
