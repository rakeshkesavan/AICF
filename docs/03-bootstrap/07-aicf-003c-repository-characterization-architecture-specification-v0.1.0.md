# AICF-003C --- Repository Characterization Architecture Specification

**Status:** Draft\
**Version:** 0.1.0\
**Parent Specifications:** AICF-003, AICF-003A, AICF-003B\
**Scope:** Architecture for combining deterministic repository evidence
with agent-assisted reasoning\
**Implementation Status:** Specification only

------------------------------------------------------------------------

## 1. Purpose

AICF-003C defines the architecture for characterizing a repository or
project before AICF profile selection and bootstrap.

It establishes a deliberate separation between:

1.  deterministic repository detection;
2.  agent-assisted repository analysis;
3.  repository characterization;
4.  AICF profile selection;
5.  `.aicf/` bootstrap.

The objective is to allow AICF to work across different editors and AI
agents while preserving a common, explainable detection foundation.

------------------------------------------------------------------------

## 2. Core Principle

AICF MUST distinguish between **observable repository facts** and
**agent-derived interpretation**.

The architecture is:

``` text
Repository
    │
    ├── Static Detection
    │       └── Deterministic Evidence
    │
    └── Agent Analysis
            └── Contextual Reasoning
                    │
                    ▼
            Repository Characterization
                    │
                    ▼
             Profile Selection
                    │
                    ▼
              AICF Bootstrap
                    │
                    ▼
                 .aicf/
```

Static detection establishes facts.

Agent analysis interprets those facts and the broader repository
context.

Neither layer should silently replace the other.

------------------------------------------------------------------------

## 3. Why Two Layers

Purely deterministic detection is strong at identifying explicit
repository signals:

``` text
angular.json
package-lock.json
tsconfig.json
nx.json
pom.xml
build.gradle
```

However, some characteristics require contextual reasoning:

``` text
Is this primarily a frontend application?
Is this a shared library?
Is this a full-stack repository?
Is this a monorepo?
What is the role of apps/web?
Which project is the primary application?
Which AICF profile best fits the repository?
```

These decisions may require understanding relationships among multiple
files and project structures.

Therefore AICF uses two complementary layers.

------------------------------------------------------------------------

## 4. Static Detection

Static Detection is deterministic and repository-local.

It consumes repository evidence and produces a `DetectionResult` as
defined by AICF-003A and AICF-003B.

Examples:

``` text
angular.json
    → Angular / HIGH

tsconfig.json
    → TypeScript / HIGH

pnpm-lock.yaml
    → pnpm / HIGH

nx.json
    → Nx / HIGH
```

Static Detection MUST:

-   be deterministic;
-   be network-independent;
-   operate within the repository boundary;
-   avoid executing project code;
-   produce explainable evidence;
-   preserve conflicting candidates;
-   remain independent of a specific AI vendor.

------------------------------------------------------------------------

## 5. Agent Analysis

Agent Analysis is an optional reasoning layer.

It consumes:

-   DetectionResult;
-   selected repository files;
-   repository structure;
-   relevant configuration;
-   documentation where appropriate;
-   user-provided context when available.

The agent MAY infer higher-level characteristics such as:

``` text
frontend-application
backend-service
full-stack-application
shared-library
monorepo
single-project
multi-project
primary-project
architectural-role
```

Agent Analysis SHOULD use the deterministic evidence as a foundation
rather than ignoring it.

------------------------------------------------------------------------

## 6. Agent Analysis Is Not a Replacement for Detection

The agent MUST NOT be treated as the authoritative source for basic
machine-observable facts when deterministic evidence is available.

For example:

``` text
angular.json exists
```

should remain a deterministic fact.

An agent may reason:

``` text
This repository is primarily an Angular application.
```

The distinction is:

``` text
Fact:
    angular.json exists

Inference:
    repository is an Angular application
```

The architecture preserves this distinction.

------------------------------------------------------------------------

## 7. Characterization

Repository Characterization is the combined interpretation layer.

Conceptually:

``` text
DetectionResult
        +
AgentAnalysisResult
        +
Optional user input
        ↓
RepositoryCharacterization
```

The characterization describes what the repository appears to be and
what AICF profile may be appropriate.

It MUST retain the distinction between:

-   detected evidence;
-   agent inference;
-   user-confirmed information.

------------------------------------------------------------------------

## 8. Characterization Categories

The initial characterization model MAY include:

``` text
projectType
projectStructure
primaryTechnology
architectureRole
workspaceType
applicationScope
recommendedProfile
```

These are intentionally higher-level than the detection categories.

For example:

``` text
Detection:
    TypeScript
    Angular
    Node
    npm
    Nx

Characterization:
    projectType = frontend-application
    projectStructure = monorepo
    primaryTechnology = angular
    workspaceType = nx
```

------------------------------------------------------------------------

## 9. Evidence vs Inference

A characterization SHOULD make provenance explicit.

Example:

``` text
Evidence:
    angular.json exists

Inference:
    Angular is the primary frontend framework

Source:
    agent analysis
```

A consumer SHOULD be able to determine whether a characteristic is:

``` text
DETECTED
INFERRED
USER_CONFIRMED
UNKNOWN
```

This distinction becomes important when profile selection is ambiguous.

------------------------------------------------------------------------

## 10. Confidence

Agent-derived characteristics SHOULD use the same broad confidence
vocabulary established by AICF-003A:

``` text
HIGH
MEDIUM
LOW
UNKNOWN
```

However, agent confidence MUST NOT be treated as mathematically
equivalent to deterministic rule confidence.

For example:

``` text
Angular / HIGH
```

from a deterministic `angular.json` rule means strong observable
evidence.

Whereas:

``` text
frontend-application / HIGH
```

from an agent means the agent considers the repository strongly
characterized as a frontend application.

These are different kinds of confidence.

------------------------------------------------------------------------

## 11. Agent Analysis Output

The exact executable schema is deferred, but conceptually an agent
result may contain:

``` json
{
  "projectType": {
    "value": "frontend-application",
    "confidence": "HIGH",
    "source": "AGENT"
  },
  "workspaceType": {
    "value": "nx-monorepo",
    "confidence": "HIGH",
    "source": "AGENT"
  },
  "primaryTechnology": {
    "value": "angular",
    "confidence": "HIGH",
    "source": "COMBINED"
  }
}
```

This is illustrative, not an implementation contract.

------------------------------------------------------------------------

## 12. Agent Input Boundary

The agent SHOULD receive only the repository context required for
characterization.

The system SHOULD prefer:

``` text
repository structure
known configuration files
relevant manifests
relevant documentation
deterministic DetectionResult
```

over indiscriminately providing the entire repository.

This reduces:

-   token consumption;
-   latency;
-   accidental exposure of irrelevant content;
-   inconsistent reasoning.

------------------------------------------------------------------------

## 13. Progressive Context Expansion

Agent Analysis SHOULD follow a progressive inspection model.

Conceptually:

``` text
Stage 1
Repository tree + DetectionResult

        ↓ if ambiguity exists

Stage 2
Relevant configuration/manifests

        ↓ if ambiguity remains

Stage 3
Targeted source/documentation inspection

        ↓

Characterization
```

The agent SHOULD stop when sufficient evidence exists.

It SHOULD NOT perform broad repository analysis merely because
additional files are available.

------------------------------------------------------------------------

## 14. Agent Prompt Contract

The AICF agent adapter SHOULD provide a standardized analysis
instruction.

The prompt SHOULD define:

-   repository boundary;
-   available DetectionResult;
-   requested characterization fields;
-   evidence requirements;
-   uncertainty behavior;
-   prohibited assumptions;
-   output format.

Different AI agents MAY use different adapter implementations, but the
semantic contract SHOULD remain common.

------------------------------------------------------------------------

## 15. Agent Adapter Architecture

AICF is intended to work across multiple AI environments.

Conceptually:

``` text
                    AICF Characterization Contract
                              │
             ┌────────────────┼────────────────┐
             │                │                │
         Antigravity        Claude          Gemini
             │                │                │
        Adapter A          Adapter B       Adapter C
             │                │                │
             └────────────────┼────────────────┘
                              ↓
                    Common characterization
```

Adapters MAY differ in:

-   prompt format;
-   tool invocation;
-   file-access mechanism;
-   response parsing;
-   editor integration.

They MUST preserve the common semantic contract.

------------------------------------------------------------------------

## 16. Vendor Neutrality

The core AICF characterization model MUST NOT depend on:

``` text
Claude
Gemini
Antigravity
Cursor
OpenAI
Anthropic
Google
```

Vendor-specific behavior belongs in adapters.

The repository characterization contract remains AICF-owned.

------------------------------------------------------------------------

## 17. Agent Non-Determinism

Agent analysis may produce different interpretations across models or
runs.

Therefore the architecture MUST NOT make agent reasoning the sole source
of truth for critical repository facts.

The system SHOULD:

1.  retain deterministic evidence;
2.  expose agent-derived characteristics as inference;
3.  identify uncertainty;
4.  request confirmation when profile selection is materially ambiguous.

------------------------------------------------------------------------

## 18. Conflict Between Static Detection and Agent Analysis

The system MUST distinguish disagreement from error.

Example:

``` text
Static Detection:
    Angular / HIGH

Agent:
    React application / MEDIUM
```

This SHOULD produce an ambiguity or conflict condition rather than
silently overwriting Angular.

Possible resolution:

``` text
Static evidence
    ↓
Agent explanation
    ↓
Additional targeted evidence
    ↓
User confirmation if still ambiguous
```

The agent MAY explain why it believes React is primary, but it MUST NOT
delete the Angular detection.

------------------------------------------------------------------------

## 19. Agent Cannot Override Evidence

Agent reasoning MUST NOT mutate the underlying DetectionResult.

Instead:

``` text
DetectionResult
    immutable evidence
        ↓
Agent Analysis
    additional interpretation
```

This preserves auditability.

------------------------------------------------------------------------

## 20. Profile Selection

Profile Selection consumes Repository Characterization.

Conceptually:

``` text
DetectionResult
       +
AgentAnalysisResult
       +
User confirmation
       ↓
Profile Selection
```

Example:

``` text
TypeScript / HIGH
Angular / HIGH
Nx / HIGH
pnpm / HIGH

Agent:
    frontend-application
    Nx monorepo

        ↓

Recommended profile:
    angular-monorepo
```

Profile selection is a separate concern from detection.

------------------------------------------------------------------------

## 21. Profile Recommendation vs Automatic Selection

AICF SHOULD distinguish:

``` text
RECOMMENDED
```

from:

``` text
SELECTED
```

A profile may be strongly recommended without being automatically
selected.

Example:

``` text
Recommended:
    angular-monorepo

Reason:
    Angular + Nx + pnpm + multi-project workspace

Status:
    AWAITING_CONFIRMATION
```

This is especially appropriate during the initial editor bootstrap
experience.

------------------------------------------------------------------------

## 22. When User Confirmation Is Required

User confirmation SHOULD be requested when:

-   multiple profiles have comparable support;
-   the agent reports material uncertainty;
-   static evidence and agent analysis disagree;
-   profile selection could materially affect generated `.aicf` content;
-   the repository contains multiple independent applications;
-   the system cannot determine the primary project.

User confirmation MAY be skipped when:

-   evidence is strong;
-   characterization is unambiguous;
-   the selected profile is low-risk and reversible.

------------------------------------------------------------------------

## 23. Bootstrap Boundary

Bootstrap begins only after profile selection.

The flow is:

``` text
Detect
  ↓
Analyze
  ↓
Characterize
  ↓
Select profile
  ↓
Bootstrap
  ↓
Generate .aicf/
```

The detector and agent analyzer MUST NOT directly generate `.aicf/` as a
side effect of detection.

------------------------------------------------------------------------

## 24. Bootstrap Safety

The bootstrap operation SHOULD be:

-   explicit;
-   previewable;
-   reversible;
-   validation-backed.

Before writing `.aicf/`, the system SHOULD be able to show:

``` text
Detected characteristics
Recommended profile
Files to be generated
Files to be preserved
Potential conflicts
```

------------------------------------------------------------------------

## 25. Existing `.aicf`

If `.aicf/` already exists, the bootstrap flow MUST NOT overwrite it
merely because characterization runs.

The system SHOULD first perform AICF discovery and validation.

Conceptually:

``` text
.aicf exists
    ↓
validate/discover
    ↓
existing installation path
```

The characterization layer does not imply re-bootstrap.

------------------------------------------------------------------------

## 26. New Repository

For a repository without `.aicf/`:

``` text
No .aicf
    ↓
Static Detection
    ↓
Agent Characterization
    ↓
Profile Recommendation
    ↓
Optional confirmation
    ↓
Generate .aicf/
```

This is the primary workflow for the editor integration goal.

------------------------------------------------------------------------

## 27. Existing Repository Without AICF

The same flow applies:

``` text
Repository
    ↓
No .aicf
    ↓
Characterize
    ↓
Recommend profile
    ↓
Bootstrap
```

The detector does not assume that every repository should have the same
AICF structure.

------------------------------------------------------------------------

## 28. Monorepositories

Monorepositories require special handling.

The system SHOULD distinguish:

``` text
Repository
    ├── apps/web
    ├── apps/admin
    ├── services/api
    └── packages/shared
```

from:

``` text
Single application
```

Agent analysis may help determine project roles.

However, profile selection SHOULD NOT collapse multiple materially
independent projects into a single application profile without explicit
support.

Multi-project profile architecture is a future concern if required.

------------------------------------------------------------------------

## 29. Characterization Should Be Explainable

The user SHOULD be able to ask:

> Why did AICF recommend this profile?

The system should be able to answer using:

``` text
Deterministic evidence
+
Agent reasoning
+
Profile-selection rationale
```

Example:

``` text
Recommended: angular-monorepo

Evidence:
- angular.json detected
- tsconfig.json detected
- nx.json detected
- pnpm-lock.yaml detected

Agent characterization:
- repository contains multiple application projects
- Angular is the primary frontend technology
- Nx manages the workspace
```

------------------------------------------------------------------------

## 30. Characterization Should Be Bounded

The agent MUST NOT be asked to understand the entire repository
architecture when only profile selection is required.

For example, profile selection may require:

``` text
framework
language
runtime
workspace type
project type
```

It may not require:

``` text
complete service dependency graph
database architecture
deployment topology
all business domains
```

Deeper architectural analysis belongs to later AICF workflows.

------------------------------------------------------------------------

## 31. Cost and Token Awareness

Agent characterization SHOULD be designed as a bounded operation.

The system SHOULD:

-   reuse deterministic evidence;
-   avoid rereading known files;
-   prioritize high-value files;
-   stop once sufficient confidence is achieved;
-   avoid full-repository summarization.

This is particularly important for editor-triggered workflows.

------------------------------------------------------------------------

## 32. Caching

Future implementations MAY cache characterization results.

A cache SHOULD be invalidated when relevant repository evidence changes.

The cache MUST NOT cause stale characterization to override current
deterministic evidence.

Caching strategy is implementation-specific.

------------------------------------------------------------------------

## 33. Reproducibility

The combined system cannot guarantee identical agent reasoning across
models.

Therefore AICF reproducibility is defined at two levels:

### Deterministic layer

``` text
Same repository + same rules
→ equivalent DetectionResult
```

### Agent layer

``` text
Same repository + same context + same adapter/model configuration
→ expected but not guaranteed equivalent characterization
```

The system SHOULD preserve enough evidence and reasoning output to
explain differences.

------------------------------------------------------------------------

## 34. Security

Agent analysis MUST follow the same repository boundary and security
restrictions as deterministic detection.

The agent MUST NOT:

-   execute repository code;
-   install dependencies;
-   invoke arbitrary scripts;
-   access files outside the repository;
-   fetch unrelated external content;
-   expose secrets in characterization output.

If secrets are encountered, they SHOULD NOT be copied into the
characterization result.

------------------------------------------------------------------------

## 35. Network Independence

The core characterization workflow SHOULD be possible without network
access.

An adapter MAY use external model infrastructure as required by its
execution environment, but repository characterization semantics MUST
NOT depend on querying external project metadata.

The repository itself remains the authoritative source of local
evidence.

------------------------------------------------------------------------

## 36. Relationship to AICF-003A

AICF-003A defines the structured result of deterministic detection.

AICF-003C does not replace it.

``` text
AICF-003A
DetectionResult
        ↓
AICF-003C
Characterization
```

The DetectionResult remains a stable lower-level contract.

------------------------------------------------------------------------

## 37. Relationship to AICF-003B

AICF-003B defines how deterministic rules produce evidence.

AICF-003C consumes that evidence and introduces the agent-assisted
reasoning layer.

``` text
003B
Detection Rules
    ↓
003A
DetectionResult
    ↓
003C
Characterization
```

------------------------------------------------------------------------

## 38. Relationship to Profile Specifications

Profile definitions are outside AICF-003C.

003C only defines the input/output boundary for profile selection.

Future profile specifications SHOULD define:

``` text
profile identity
profile applicability
required characteristics
optional characteristics
generated artifacts
```

------------------------------------------------------------------------

## 39. Future Characterization Schema

A future specification MAY define a formal schema such as:

``` json
{
  "characteristics": {
    "projectType": {
      "value": "frontend-application",
      "confidence": "HIGH",
      "source": "AGENT"
    },
    "workspaceType": {
      "value": "nx-monorepo",
      "confidence": "HIGH",
      "source": "COMBINED"
    }
  },
  "profile": {
    "recommended": "angular-monorepo",
    "confidence": "HIGH",
    "status": "AWAITING_CONFIRMATION"
  }
}
```

This is intentionally illustrative.

Executable schema design is deferred.

------------------------------------------------------------------------

## 40. Implementation Boundary

AICF-003C is an architecture specification only.

It does not define:

-   TypeScript interfaces;
-   Python classes;
-   CLI commands;
-   editor APIs;
-   MCP tools;
-   prompt templates;
-   JSON Schema;
-   storage implementation;
-   cache implementation.

Those should be derived from the accepted architecture.

------------------------------------------------------------------------

## 41. Acceptance Criteria

AICF-003C is ready for implementation planning when:

-   deterministic detection and agent analysis are explicitly separated;
-   the distinction between evidence and inference is accepted;
-   agent analysis is optional;
-   agent adapters are vendor-neutral at the contract level;
-   DetectionResult remains immutable;
-   agent reasoning cannot silently override deterministic evidence;
-   characterization combines evidence and inference;
-   profile selection is separate from characterization;
-   bootstrap is separate from profile selection;
-   user confirmation boundaries are defined;
-   monorepository ambiguity is recognized;
-   security and repository-boundary rules apply to both layers;
-   agent analysis is bounded and cost-aware;
-   executable schemas and adapters remain deferred.

------------------------------------------------------------------------

## 42. Proposed End-to-End Architecture

The resulting conceptual architecture is:

``` text
                         Repository
                             │
                             ▼
                  ┌─────────────────────┐
                  │ AICF Discovery      │
                  │ Is .aicf present?   │
                  └──────────┬──────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                 Existing           New
                   AICF            / absent
                    │                 │
                    │                 ▼
                    │       ┌──────────────────┐
                    │       │ Static Detection │
                    │       └────────┬─────────┘
                    │                │
                    │                ▼
                    │       ┌──────────────────┐
                    │       │ DetectionResult  │
                    │       └────────┬─────────┘
                    │                │
                    │                ▼
                    │       ┌──────────────────┐
                    │       │ Agent Analysis   │
                    │       └────────┬─────────┘
                    │                │
                    │                ▼
                    │       ┌──────────────────┐
                    │       │ Repository       │
                    │       │ Characterization │
                    │       └────────┬─────────┘
                    │                │
                    │                ▼
                    │       ┌──────────────────┐
                    │       │ Profile Selection│
                    │       └────────┬─────────┘
                    │                │
                    │        confirmation?
                    │                │
                    │                ▼
                    │       ┌──────────────────┐
                    │       │ AICF Bootstrap   │
                    │       └────────┬─────────┘
                    │                │
                    └────────────────┴──────► .aicf/
```

The important invariant is:

``` text
Detection ≠ Characterization ≠ Profile Selection ≠ Bootstrap
```

Each stage has a clear responsibility.

------------------------------------------------------------------------

## 43. Status

**Draft --- AICF-003C v0.1.0**

This specification establishes the architectural boundary for
agent-assisted repository characterization.

Before implementation, the next review should focus on:

1.  whether the deterministic/agent boundary is sufficiently clear;
2.  whether the proposed characterization categories are appropriate;
3.  what information the agent actually needs to inspect;
4.  when user confirmation should be mandatory;
5.  whether profile selection should be a separate specification;
6.  whether the characterization output now warrants a formal schema.

No implementation should begin until these architectural decisions are
accepted.
