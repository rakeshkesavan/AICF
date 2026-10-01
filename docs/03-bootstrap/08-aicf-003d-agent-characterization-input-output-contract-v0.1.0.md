# AICF-003D --- Agent Characterization Input & Output Contract

**Status:** Draft\
**Version:** 0.1.0\
**Parent Specification:** AICF-003C --- Repository Characterization
Architecture Specification\
**Scope:** Contract for the minimum repository context supplied to an
agent and the characterization result returned by the agent\
**Implementation Status:** Specification only

------------------------------------------------------------------------

## 1. Purpose

AICF-003D defines the semantic contract between AICF and an AI agent
used for repository characterization.

It answers two questions:

1.  **What minimum context should the agent receive to characterize a
    repository?**
2.  **What structured result should the agent return?**

The contract is designed for editor-driven workflows where an arbitrary
repository may be opened and AICF must determine whether and how the
repository should be initialized.

The contract deliberately does not define:

-   a specific AI model;
-   a specific editor;
-   a specific prompt language;
-   an MCP implementation;
-   a JSON Schema implementation;
-   a CLI implementation.

Those are implementation concerns.

------------------------------------------------------------------------

# 2. Architectural Position

AICF-003D sits between deterministic detection and profile selection:

``` text
Repository
    ↓
Static Detection
    ↓
DetectionResult
    ↓
Agent Context Builder
    ↓
Agent Analysis
    ↓
CharacterizationResult
    ↓
Profile Selection
    ↓
AICF Bootstrap
```

The agent does not replace deterministic detection.

The agent consumes deterministic evidence and performs bounded
contextual reasoning.

------------------------------------------------------------------------

# 3. Core Principle

The agent SHOULD receive the **minimum sufficient context** required to
make a characterization decision.

The agent SHOULD NOT automatically receive the entire repository.

The preferred model is:

``` text
L0 → L1 → L2
```

where context expands only when the current evidence is insufficient.

------------------------------------------------------------------------

# 4. Context Levels

## 4.1 Level 0 --- Repository Overview

L0 is always available.

It contains:

``` text
repository boundary
repository tree / bounded file listing
DetectionResult
AICF discovery status
```

L0 should normally be sufficient for straightforward repositories.

Example:

``` text
Repository
├── angular.json
├── package.json
├── package-lock.json
├── tsconfig.json
├── src/
│   ├── app/
│   └── assets/
└── README.md
```

Combined with:

``` text
Angular / HIGH
TypeScript / HIGH
npm / HIGH
```

this may already be sufficient to characterize the repository as a
frontend application.

------------------------------------------------------------------------

# 5. Level 1 --- Targeted Configuration Context

L1 is requested when L0 does not provide sufficient confidence.

The agent MAY receive selected files such as:

``` text
package.json
angular.json
nx.json
turbo.json
pom.xml
build.gradle
tsconfig.json
vite.config.ts
README.md
```

The selection SHOULD be driven by the deterministic detection results
and the characterization fields still unresolved.

The system SHOULD avoid supplying unrelated configuration files.

------------------------------------------------------------------------

# 6. Level 2 --- Targeted Source and Documentation Context

L2 is used only when material ambiguity remains after L0 and L1.

Examples include:

``` text
apps/web/
services/api/
src/main.*
src/app/
README.md
architecture documentation
```

The agent SHOULD inspect only the minimum additional content required to
resolve the ambiguity.

L2 MUST NOT become an unrestricted repository dump.

------------------------------------------------------------------------

# 7. Context Escalation

The preferred decision flow is:

``` text
L0
 │
 ├── sufficient confidence → characterize
 │
 └── insufficient
          ↓
         L1
          │
          ├── sufficient confidence → characterize
          │
          └── insufficient
                   ↓
                  L2
                   │
                   ├── sufficient confidence → characterize
                   │
                   └── unresolved → UNKNOWN / AMBIGUOUS
```

The agent SHOULD stop inspection once the requested characterization is
sufficiently supported.

------------------------------------------------------------------------

# 8. Context Budget

AICF-003D does not define a universal token limit.

Instead, the context builder SHOULD enforce bounded inspection.

The implementation SHOULD track:

``` text
files inspected
directories inspected
bytes read
estimated token volume
```

This metadata is operational and need not be part of the canonical
characterization result.

------------------------------------------------------------------------

# 9. Context Selection Rules

The context builder SHOULD prioritize:

1.  deterministic DetectionResult;
2.  repository root metadata;
3.  technology-specific configuration;
4.  workspace definitions;
5.  project manifests;
6.  targeted source entry points;
7.  relevant documentation.

It SHOULD deprioritize:

``` text
generated files
dependency trees
build output
coverage
cache directories
binary files
large assets
```

------------------------------------------------------------------------

# 10. Repository Tree Representation

The repository tree supplied to the agent SHOULD be:

-   repository-relative;
-   bounded;
-   deterministic;
-   free of machine-specific paths.

Example:

``` text
apps/
  web/
    src/
    package.json
  admin/
    src/
    package.json
services/
  api/
    src/
    package.json
package.json
pnpm-workspace.yaml
nx.json
```

The tree SHOULD communicate structure without requiring the agent to
read every file.

------------------------------------------------------------------------

# 11. DetectionResult as Ground Truth for Observable Facts

The agent SHOULD receive the DetectionResult generated by
AICF-003A/003B.

Example:

``` json
{
  "languages": [
    {
      "id": "typescript",
      "confidence": "HIGH"
    }
  ],
  "frameworks": [
    {
      "id": "angular",
      "confidence": "HIGH"
    }
  ],
  "packageManagers": [
    {
      "id": "pnpm",
      "confidence": "HIGH"
    }
  ]
}
```

The agent SHOULD treat these as detected observations.

It SHOULD NOT rewrite or mutate them.

------------------------------------------------------------------------

# 12. Evidence Provenance

Where possible, the agent SHOULD receive evidence references associated
with detections.

Example:

``` text
Angular / HIGH
Evidence:
    angular.json
Rule:
    angular.workspace-config
```

This allows the agent to reason from explicit evidence rather than
rediscovering facts unnecessarily.

------------------------------------------------------------------------

# 13. Agent Task Definition

The characterization task given to the agent SHOULD explicitly state:

``` text
You are characterizing a software repository for AICF profile selection.

Use deterministic detection results as evidence.

Inspect additional repository context only when required.

Do not modify files.

Do not execute project code.

Do not install dependencies.

Do not invent repository facts.

If evidence is insufficient, return UNKNOWN or AMBIGUOUS.
```

The exact prompt wording is implementation-specific.

The semantic requirements are not.

------------------------------------------------------------------------

# 14. Initial Characterization Fields

The initial output contract contains five core characteristics:

``` text
projectType
workspaceType
primaryTechnology
applicationScope
architectureRole
```

These are intentionally limited.

------------------------------------------------------------------------

# 15. `projectType`

Describes the broad role of the repository or project.

Initial values:

``` text
frontend-application
backend-service
full-stack-application
shared-library
cli-application
service
unknown
```

Additional values MAY be introduced later.

The agent MUST NOT invent new enum values in a canonical result.

If none apply:

``` text
unknown
```

------------------------------------------------------------------------

# 16. `workspaceType`

Describes project/workspace organization.

Initial values:

``` text
single-project
monorepo
multi-project
unknown
```

Where a specific workspace technology is already deterministically
detected, the agent MAY provide a more specific characterization through
supporting metadata.

For example:

``` text
workspaceType:
    monorepo

workspaceManager:
    nx
```

`workspaceManager` is supporting context rather than a replacement for
`workspaceType`.

------------------------------------------------------------------------

# 17. `primaryTechnology`

Represents the technology the agent believes is most central to the
characterized project.

Example:

``` text
primaryTechnology:
    angular
```

This MUST be grounded in DetectionResult and/or additional repository
evidence.

The agent MUST NOT select a primary technology solely because it appears
in one incidental file.

------------------------------------------------------------------------

# 18. `applicationScope`

Describes the broad execution/user-facing scope.

Initial values:

``` text
web
api
service
library
cli
mixed
unknown
```

Example:

``` text
Angular browser application
    → web
```

``` text
Spring Boot REST service
    → api
```

------------------------------------------------------------------------

# 19. `architectureRole`

Describes the role of the characterized project.

Initial values:

``` text
application
service
library
shared-package
workspace
unknown
```

This is intentionally coarse.

Detailed architecture discovery belongs to later AICF capabilities.

------------------------------------------------------------------------

# 20. Characteristic Result Structure

Each characteristic SHOULD carry:

``` text
value
confidence
source
reason
evidence
```

Conceptually:

``` json
{
  "value": "frontend-application",
  "confidence": "HIGH",
  "source": "AGENT",
  "reason": "The repository contains an Angular browser application with application targets.",
  "evidence": [
    "angular.json",
    "src/"
  ]
}
```

------------------------------------------------------------------------

# 21. Source

Allowed source values:

``` text
DETECTED
AGENT
COMBINED
USER_CONFIRMED
```

### DETECTED

The value is directly established by deterministic rules.

### AGENT

The value is inferred by agent reasoning.

### COMBINED

The value is derived from deterministic evidence plus agent reasoning.

### USER_CONFIRMED

The value was explicitly confirmed by the user.

------------------------------------------------------------------------

# 22. Confidence

Allowed values:

``` text
HIGH
MEDIUM
LOW
UNKNOWN
```

Agent confidence represents confidence in the characterization, not a
mathematical probability.

------------------------------------------------------------------------

# 23. Reason

`reason` is a concise explanation of why the characteristic was
selected.

Example:

``` text
"The repository contains Angular application targets under the Nx workspace."
```

The reason SHOULD reference observable context.

It SHOULD NOT contain unsupported assumptions.

------------------------------------------------------------------------

# 24. Evidence References

Agent evidence SHOULD be repository-relative.

Example:

``` text
angular.json
apps/web/project.json
apps/web/src/
```

Absolute paths are prohibited.

URI-style local paths are prohibited.

Examples of invalid evidence:

``` text
D:\Work\project\angular.json
file:///d:/Work/project/angular.json
```

------------------------------------------------------------------------

# 25. Unknown

The agent MUST be able to explicitly return:

``` text
value: unknown
confidence: UNKNOWN
```

when available evidence is insufficient.

It MUST NOT force a classification merely to complete the response.

------------------------------------------------------------------------

# 26. Ambiguity

The result SHOULD support an ambiguity state for cases where more than
one characterization remains plausible.

Example:

``` text
projectType:
    value: unknown
    confidence: LOW
    source: AGENT
    reason:
        "Repository contains independent Angular and Java applications
         and no primary project could be established."
```

The implementation MAY represent ambiguity through an explicit status
field in a future executable schema.

------------------------------------------------------------------------

# 27. Multiple Projects

For a monorepository, the initial characterization contract describes
the repository-level characterization.

It does not attempt to fully model every project.

Example:

``` text
Repository:
    monorepo
    primary technology: Angular
    project type: frontend-application
```

If multiple materially independent projects exist, the agent SHOULD
report the ambiguity rather than pretending that one project represents
the entire repository.

Detailed per-project characterization is a future extension.

------------------------------------------------------------------------

# 28. Agent Must Not Mutate Detection

The following behavior is prohibited:

``` text
DetectionResult:
    Angular / HIGH

Agent:
    "I think this is React"

System:
    replace Angular with React
```

Instead:

``` text
DetectionResult:
    Angular / HIGH

Agent characterization:
    React / MEDIUM

Result:
    conflict / ambiguity
```

The underlying evidence remains intact.

------------------------------------------------------------------------

# 29. Contradictory Evidence

When agent reasoning conflicts with strong deterministic evidence, the
agent SHOULD explain the conflict.

Example:

``` text
Detected:
    Angular / HIGH
    React / MEDIUM

Agent:
    primaryTechnology = angular
    confidence = MEDIUM
```

The result can then be escalated to targeted inspection or user
confirmation.

------------------------------------------------------------------------

# 30. User Confirmation

User confirmation SHOULD be requested when:

-   project type remains ambiguous;
-   multiple primary technologies compete;
-   multiple independent applications exist;
-   agent confidence is low;
-   profile selection would materially differ depending on the
    characterization;
-   the bootstrap action is not safely reversible.

The confirmation request SHOULD be concise.

Example:

``` text
AICF detected an Nx monorepo containing Angular and Java projects.

Which project should be treated as the primary AICF project?
```

------------------------------------------------------------------------

# 31. Agent Output Must Be Structured

The agent SHOULD return machine-readable characterization data rather
than only prose.

Prose MAY accompany the result for user presentation.

The canonical semantic output is structured.

Conceptually:

``` json
{
  "characteristics": {
    "projectType": {},
    "workspaceType": {},
    "primaryTechnology": {},
    "applicationScope": {},
    "architectureRole": {}
  },
  "status": "CONFIDENT"
}
```

The executable schema is deferred.

------------------------------------------------------------------------

# 32. Overall Characterization Status

The initial conceptual status values are:

``` text
CONFIDENT
AMBIGUOUS
INCOMPLETE
FAILED
```

### CONFIDENT

Required characteristics are sufficiently supported.

### AMBIGUOUS

Multiple materially plausible interpretations remain.

### INCOMPLETE

Additional context may resolve the characterization.

### FAILED

The agent analysis could not complete due to an execution or context
error.

A failed agent analysis MUST NOT invalidate the deterministic
DetectionResult.

------------------------------------------------------------------------

# 33. Escalation on INCOMPLETE

An `INCOMPLETE` result SHOULD cause the context builder to determine
whether additional L1/L2 inspection is justified.

Example:

``` text
L0
 ↓
INCOMPLETE
 ↓
L1
 ↓
INCOMPLETE
 ↓
L2
 ↓
CONFIDENT
```

If sufficient evidence cannot be established:

``` text
UNKNOWN / AMBIGUOUS
```

should be returned rather than continuing indefinitely.

------------------------------------------------------------------------

# 34. Bounded Agent Analysis

The system SHOULD impose an implementation-defined maximum on:

``` text
context expansion
files inspected
bytes read
analysis iterations
```

The agent MUST NOT recursively request more context without bounds.

------------------------------------------------------------------------

# 35. No Repository Mutation

Characterization is read-only.

During characterization the agent MUST NOT:

-   create files;
-   modify files;
-   delete files;
-   install dependencies;
-   run migrations;
-   execute project scripts;
-   change configuration.

Bootstrap is a separate explicit phase.

------------------------------------------------------------------------

# 36. No Network-Dependent Repository Reasoning

The characterization result SHOULD be derivable from repository-local
context.

An external model service may be used by the agent adapter, but the
agent MUST NOT require external project metadata to characterize the
repository.

------------------------------------------------------------------------

# 37. Secret Handling

Agent context MUST avoid unnecessary secret exposure.

The context builder SHOULD exclude or redact files such as:

``` text
.env
.env.*
credentials
private keys
certificates
secret stores
```

unless a specific characterization rule explicitly requires them.

Even when inspected, secrets MUST NOT appear in characterization output.

------------------------------------------------------------------------

# 38. Adapter Contract

Every AICF agent adapter SHOULD implement the semantic flow:

``` text
Input:
    DetectionResult
    Repository Context
    Characterization Request

Output:
    CharacterizationResult
```

Adapters MAY differ in how they:

-   build prompts;
-   invoke models;
-   provide file context;
-   parse responses;
-   handle retries.

The resulting semantic contract MUST remain consistent.

------------------------------------------------------------------------

# 39. Agent Independence

The characterization contract MUST be independent of:

``` text
Antigravity
Claude
Gemini
Cursor
OpenAI
Anthropic
Google
```

An adapter translates the common AICF contract into the capabilities of
a particular environment.

------------------------------------------------------------------------

# 40. Profile Selection Input

Profile Selection consumes:

``` text
DetectionResult
+
CharacterizationResult
+
optional User Confirmation
```

It MUST NOT depend solely on free-form agent prose.

Conceptually:

``` text
Detection:
    Angular / HIGH
    TypeScript / HIGH
    Nx / HIGH

Characterization:
    projectType = frontend-application
    workspaceType = monorepo
    primaryTechnology = angular

        ↓

Profile Selection
```

------------------------------------------------------------------------

# 41. Bootstrap Input

Bootstrap consumes a selected profile.

It does not consume raw agent reasoning directly.

The intended boundary is:

``` text
Agent
    ↓
Characterization
    ↓
Profile Selection
    ↓
Selected Profile
    ↓
Bootstrap
```

This prevents an agent from directly generating arbitrary AICF
structures without passing through validation and profile rules.

------------------------------------------------------------------------

# 42. Example --- Simple Angular Repository

### DetectionResult

``` text
Angular / HIGH
TypeScript / HIGH
npm / HIGH
Node / LOW
```

### Agent Context

``` text
L0:
    repository tree
    DetectionResult

No additional inspection required.
```

### Characterization

``` text
projectType:
    frontend-application
    HIGH
    COMBINED

workspaceType:
    single-project
    HIGH
    AGENT

primaryTechnology:
    angular
    HIGH
    COMBINED

applicationScope:
    web
    HIGH
    AGENT

architectureRole:
    application
    HIGH
    AGENT
```

### Result

``` text
CONFIDENT
```

------------------------------------------------------------------------

# 43. Example --- Ambiguous Monorepo

Repository:

``` text
apps/web/
apps/admin/
services/api/
packages/shared/
```

Detection:

``` text
Angular / HIGH
Java / HIGH
TypeScript / HIGH
pnpm / HIGH
Nx / HIGH
```

Agent:

``` text
projectType:
    unknown
    LOW

workspaceType:
    monorepo
    HIGH

primaryTechnology:
    unknown
    LOW

applicationScope:
    mixed
    HIGH

architectureRole:
    workspace
    HIGH
```

Status:

``` text
AMBIGUOUS
```

The system should request clarification before selecting a single
application profile.

------------------------------------------------------------------------

# 44. Example --- Full-Stack Repository

Detection:

``` text
Angular / HIGH
TypeScript / HIGH
Java / HIGH
Gradle / HIGH
npm / HIGH
```

Agent inspection:

``` text
frontend/
backend/
```

Characterization:

``` text
projectType:
    full-stack-application
    HIGH

workspaceType:
    multi-project
    HIGH

primaryTechnology:
    angular
    MEDIUM

applicationScope:
    mixed
    HIGH

architectureRole:
    application
    HIGH
```

The profile-selection layer can then decide whether a full-stack AICF
profile exists or whether separate project characterization is required.

------------------------------------------------------------------------

# 45. Minimum Viable Characterization

For the first implementation, AICF SHOULD NOT require exhaustive
characterization.

The minimum viable contract is:

``` text
projectType
workspaceType
primaryTechnology
```

The following may remain optional:

``` text
applicationScope
architectureRole
```

This allows the editor bootstrap workflow to start with a small,
reliable contract.

------------------------------------------------------------------------

# 46. Acceptance Criteria

AICF-003D is ready for implementation planning when:

-   L0/L1/L2 context levels are accepted;
-   progressive context expansion is accepted;
-   minimum context principles are accepted;
-   DetectionResult is treated as immutable evidence;
-   agent reasoning is explicitly separated from detection;
-   initial characterization fields are accepted;
-   provenance is represented;
-   confidence semantics are accepted;
-   UNKNOWN and AMBIGUOUS outcomes are supported;
-   user confirmation boundaries are accepted;
-   agent adapters are vendor-neutral;
-   agent analysis is read-only;
-   secret handling is defined;
-   repository-boundary rules are preserved;
-   bootstrap remains separate from characterization;
-   structured output is required;
-   exhaustive repository analysis is explicitly avoided.

------------------------------------------------------------------------

# 47. Status

**Draft --- AICF-003D v0.1.0**

This specification defines the minimum semantic contract between AICF
and an agent performing repository characterization.

The next review should focus on:

1.  whether the five characterization fields are sufficient;
2.  whether L0/L1/L2 provides the right context boundary;
3.  whether `UNKNOWN`, `AMBIGUOUS`, and `INCOMPLETE` are sufficiently
    distinct;
4.  whether provenance needs a stronger formal model;
5.  whether the minimum viable characterization can support profile
    selection;
6.  whether the next step should be a formal Characterization JSON
    Schema and fixtures.

No implementation should begin until the contract is accepted.
