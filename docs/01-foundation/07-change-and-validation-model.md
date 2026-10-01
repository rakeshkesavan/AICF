# AICF Framework Definition v0.1

## 7. Change & Validation Model

### 7.1 Purpose

The AICF Change & Validation Model defines how AI-generated or AI-assisted changes are:

* bounded
* authorized
* implemented
* measured
* validated
* reviewed
* accepted
* recorded

The model addresses two fundamental risks of AI-assisted development:

### Change Risk

> **The agent changes more than it should.**

### Quality Risk

> **The agent changes the right area, but the resulting implementation is incorrect.**

AICF therefore establishes:

```text
CONTROL THE CHANGE
        +
PROVE THE RESULT
```

---

# 7.2 Change Principle

The fundamental AICF change principle is:

> **Every meaningful change must have a known purpose, an understood boundary, and an appropriate validation strategy.**

A change should be traceable to:

```text
Requirement
    ↓
Task
    ↓
Implementation
    ↓
Validation
```

---

# 7.3 Change Scope

Every meaningful task should establish its intended change scope.

The scope may include:

```text
Objective
Allowed Areas
Restricted Areas
Non-goals
Expected Files
Expected Components
Expected Interfaces
Expected Data Changes
Expected Behaviour Changes
```

Not every task needs every field.

The amount of definition should be proportional to complexity and risk.

---

# 7.4 Change Categories

AICF classifies changes into four categories.

### C1 — Required Change

Directly necessary to satisfy the task.

Example:

```text
Add employee profile validation
```

The validation code is a required change.

---

### C2 — Supporting Change

A limited change required to safely implement the task.

Example:

```text
Feature requires a small update to an existing
shared validation utility.
```

This is acceptable when clearly necessary and within reasonable scope.

---

### C3 — Opportunistic Change

A useful improvement discovered during implementation but not required for the task.

Examples:

```text
Refactor nearby code
Upgrade dependency
Improve unrelated error handling
Rename unrelated variables
Optimize another component
```

These should generally become separate work.

---

### C4 — Prohibited Change

Changes explicitly outside the task or project authority boundary.

Examples:

```text
Modify authentication architecture
Change production infrastructure
Delete data
Change database schema
```

when not authorized.

---

# 7.5 Change Boundary

A task establishes a boundary:

```text id="09e7y4"
                 TASK
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
     ALLOWED    RESTRICTED  PROHIBITED
        │          │          │
      Execute     Ask        Stop
```

This allows agents to work autonomously without giving them unrestricted authority.

---

# 7.6 Change Budget

AICF introduces the concept of a **Change Budget**.

The Change Budget represents the expected magnitude and impact of a task.

It may include:

```text
Expected file count
Maximum file count
Expected modules
Expected components
Expected APIs
Expected database impact
Expected architectural impact
Expected dependency changes
```

Example:

```text id="9x0w4g"
TASK-042

Expected files:
3–6

Maximum files:
10

Expected modules:
Employee Profile

Database changes:
None

Authentication changes:
None

Architecture changes:
None
```

The budget is not a rigid mathematical constraint.

It is an **early warning mechanism**.

---

# 7.7 Change Budget Breach

A change-budget breach occurs when implementation significantly exceeds the expected change surface.

Example:

```text id="j8u8ne"
Expected:
3–6 files

Actual:
17 files
```

The agent should pause and investigate.

It should determine:

```text
Is the original estimate wrong?
Is the requirement larger than expected?
Is there an architectural dependency?
Is the implementation over-engineered?
Has scope expanded?
```

The agent should not automatically continue simply because the changes compile.

---

# 7.8 Change Budget Is Not a Hard File Limit

AICF explicitly avoids:

> "Never modify more than 10 files."

Some legitimate changes affect hundreds of files.

Examples:

* migration
* framework upgrade
* large refactor
* generated code changes

The Change Budget therefore measures **expected impact**, not merely file count.

For high-scale tasks, the budget may instead be expressed as:

```text
Affected subsystem
Migration scope
API surface
Data volume
Architecture boundaries
```

---

# 7.9 Change Surface

AICF defines **Change Surface** as the total area of the system potentially affected by a change.

It includes:

```text
Files
Modules
Components
APIs
Data
Dependencies
Infrastructure
External systems
User behaviour
```

A change with a large surface requires greater validation.

---

# 7.10 Change Risk

Change risk is influenced by:

```text
Impact
+
Scope
+
Uncertainty
+
Coupling
+
Irreversibility
+
Security sensitivity
```

A simple UI change may have low risk.

A database migration may have high risk even if it changes only one file.

---

# 7.11 Risk Classification

AICF uses four general risk levels.

### R1 — Low

Characteristics:

* isolated
* reversible
* low user impact
* low architectural impact

Examples:

* text change
* isolated styling
* small UI correction

---

### R2 — Moderate

Characteristics:

* multiple files
* behaviour change
* moderate dependencies
* limited cross-system impact

Examples:

* feature addition
* API integration
* shared component change

---

### R3 — High

Characteristics:

* architectural impact
* sensitive data
* security boundaries
* major integration
* significant migration

Examples:

* authorization changes
* database schema migration
* major API contract changes

---

### R4 — Critical

Characteristics:

* potentially irreversible
* production impact
* security-critical
* financial or highly sensitive data

Examples:

* production data deletion
* destructive migration
* payment settlement logic
* production infrastructure destruction

---

# 7.12 Autonomy Based on Risk

Change authority should correspond to risk.

```text id="k0cqkl"
R1 → Autonomous
R2 → Autonomous / Supervised
R3 → Approval Required
R4 → Human Controlled
```

The exact project-specific rules may tighten these defaults.

---

# 7.13 Protected Boundaries

Certain areas may be protected regardless of task size.

Examples:

```text id="z7m9w2"
Authentication
Authorization
Secrets
Production infrastructure
Database deletion
Payment processing
Sensitive data
Security configuration
Public API contracts
```

An agent attempting to cross a protected boundary should trigger additional controls.

---

# 7.14 Validation Principle

The fundamental validation principle is:

> **Every meaningful change must be validated against what it was intended to accomplish and what it was required not to break.**

Therefore validation has two dimensions:

```text id="y8tq0a"
Positive Validation
        +
Negative / Regression Validation
```

### Positive

Does the new functionality work?

### Regression

Did existing functionality continue to work?

---

# 7.15 Validation Levels

AICF defines a layered validation model.

```text id="x9j7r5"
V1 — Build / Syntax
V2 — Type Safety
V3 — Static Analysis
V4 — Unit Testing
V5 — Integration Testing
V6 — Functional Validation
V7 — Regression Validation
V8 — Security Validation
V9 — Performance Validation
V10 — Architecture / Compliance Validation
```

The appropriate levels depend on task risk.

---

# 7.16 V1 — Build and Syntax

Verify:

* syntax
* compilation
* build
* imports
* generated artifacts

This establishes basic technical validity.

Passing V1 does not establish functional correctness.

---

# 7.17 V2 — Type Safety

Where applicable:

* type checking
* schema validation
* interface consistency
* API type compatibility

The agent should resolve type errors rather than suppressing them merely to complete the task.

---

# 7.18 V3 — Static Analysis

Where applicable:

* linting
* static analysis
* code quality rules
* dependency checks
* security scanners

Project-specific standards take precedence.

---

# 7.19 V4 — Unit Validation

Relevant isolated behaviour should be tested.

The objective is not to maximize test count.

The objective is:

> **Test the behaviour that matters.**

---

# 7.20 V5 — Integration Validation

Where the change crosses boundaries, verify integration.

Examples:

```text
Frontend → API
API → Database
Service → External API
Event → Consumer
Authentication → Application
```

---

# 7.21 V6 — Functional Validation

Verify the actual user or system behaviour described by the requirement.

Example:

```text
Requirement:
User can edit employee department.

Functional validation:
1. Open employee profile.
2. Change department.
3. Save.
4. Confirm success.
5. Reload.
6. Confirm persisted value.
```

Functional validation is particularly important for AI-generated UI and full-stack changes.

---

# 7.22 V7 — Regression Validation

Verify that existing behaviour remains intact.

Regression scope should be proportional to the Change Surface.

For example:

```text
Shared authentication component changed
        ↓
Broad regression required
```

versus:

```text
Isolated static text changed
        ↓
Minimal regression required
```

---

# 7.23 V8 — Security Validation

Security validation should be applied when relevant.

Examples:

* authentication
* authorization
* input validation
* injection protection
* secret handling
* data access
* file access
* privilege boundaries

High-risk security changes should not rely solely on AI-generated reasoning.

---

# 7.24 V9 — Performance Validation

Performance changes should be evidence-driven.

The agent should avoid claiming:

> "This is faster."

unless supported by measurement or appropriate evidence.

Where performance is the objective:

```text id="4uxy42"
Baseline
   ↓
Change
   ↓
Measure
   ↓
Compare
```

---

# 7.25 V10 — Architecture / Compliance Validation

For significant changes, verify:

* architectural rules
* project conventions
* dependency constraints
* API contracts
* data rules
* compliance requirements where applicable

This prevents technically working code from violating the intended architecture.

---

# 7.26 Validation Matrix

AICF maps risk to validation depth.

| Risk | Typical Validation                                                   |
| ---- | -------------------------------------------------------------------- |
| R1   | Build / targeted functional check                                    |
| R2   | Build + types + relevant tests + functional                          |
| R3   | Full relevant test suite + regression + security/architecture checks |
| R4   | Comprehensive validation + explicit human review/approval            |

This is a default model, not an absolute rule.

Project-specific requirements may increase validation.

---

# 7.27 Acceptance Criteria vs Quality Gates

AICF distinguishes:

### Acceptance Criteria

Does the implementation satisfy the requested outcome?

### Quality Gates

Does the implementation meet engineering standards?

For example:

```text id="z0h0cm"
Acceptance:
User can submit the leave request.

Quality:
Type-safe
Tests pass
No authorization regression
Architecture compliant
```

Both must be satisfied.

---

# 7.28 Validation Evidence

Validation should produce evidence where practical.

Examples:

```text id="5a2m4k"
Test results
Build output
Screenshots
Benchmark measurements
Static-analysis results
API responses
Migration checks
```

The agent should distinguish:

```text
Evidence obtained
```

from:

```text
Expected result
```

---

# 7.29 No False Completion

AICF defines a strict completion rule:

> **An agent must never declare a task complete when required validation has not been performed.**

Instead:

```text id="1n1n0f"
Validation incomplete
```

should be explicitly reported.

Possible states:

```text
COMPLETE
COMPLETE WITH KNOWN LIMITATIONS
PARTIALLY COMPLETE
BLOCKED
FAILED
```

---

# 7.30 Validation Failure

When validation fails, the agent must not immediately expand the implementation indiscriminately.

Preferred sequence:

```text id="o5k8sq"
Failure
   ↓
Collect evidence
   ↓
Identify root cause
   ↓
Determine scope
   ↓
Plan corrective change
   ↓
Implement
   ↓
Revalidate
```

If the corrective change materially expands scope:

```text id="7f3xj2"
STOP
→ reassess task
→ update scope
→ approval if required
```

---

# 7.31 Rollback and Recovery

For higher-risk changes, the implementation strategy should consider recovery.

Possible mechanisms:

* version control
* migration rollback
* feature flags
* staged rollout
* reversible configuration
* backup
* transactional changes

AICF does not prescribe one mechanism.

It requires the agent to consider recoverability where risk warrants it.

---

# 7.32 Change Traceability

A meaningful change should be traceable through:

```text id="n8v2dz"
Requirement
     ↓
Task
     ↓
Change Scope
     ↓
Implementation
     ↓
Validation
     ↓
Result
```

For significant changes:

```text id="o5c4l1"
Requirement
     ↓
Decision
     ↓
Task
     ↓
Implementation
     ↓
Validation
```

This enables later investigation.

---

# 7.33 Change Reporting

At completion, the agent should report:

```text id="3f1f2x"
Objective
Changes made
Affected areas
Validation performed
Validation results
Known limitations
Assumptions
Remaining work
```

The report should be concise but sufficient for another engineer to understand the outcome.

---

# 7.34 Change & Validation State Machine

The combined process can be represented as:

```text id="x6o4yk"
                  TASK
                    │
                    ↓
              DEFINE SCOPE
                    │
                    ↓
             SET CHANGE BUDGET
                    │
                    ↓
               ASSESS RISK
                    │
             ┌──────┴──────┐
             ↓             ↓
         LOW/MEDIUM       HIGH
             │             │
             ↓          APPROVAL
             │             │
             └──────┬──────┘
                    ↓
                 EXECUTE
                    ↓
                 VERIFY
                    │
             ┌──────┴──────┐
             ↓             ↓
           PASS           FAIL
             │             │
             ↓          DIAGNOSE
          RECORD            │
             │              ↓
             │          REASSESS
             │              │
             │         ┌────┴────┐
             │         ↓         ↓
             │       RETRY      SCOPE
             │                   CHANGE
             │                     │
             │                  APPROVAL
             │                     │
             └──────────┬──────────┘
                        ↓
                     COMPLETE
```

---

# 7.35 Definition of Done

AICF defines the general completion condition as:

```text id="8x5p8e"
DONE =
Scope satisfied
+
Implementation complete
+
Required validation passed
+
Known limitations disclosed
+
Material state recorded
```

Therefore:

```text
Code generated ≠ Done

Code compiles ≠ Done

Tests pass ≠ necessarily Done

Feature works ≠ necessarily Done
```

The task must satisfy its complete acceptance and quality requirements.

---

# 7.36 Change & Validation Principles

The section can be summarized by the following rules:

```text
C01 — Every meaningful change has a purpose.
C02 — Every meaningful change has a boundary.
C03 — Change authority is proportional to risk.
C04 — Change surface should be minimized.
C05 — Change Budget provides an early warning.
C06 — Protected boundaries require additional controls.
C07 — Validation must match risk.
C08 — Acceptance and quality are separate concerns.
C09 — Validation must be evidenced where practical.
C10 — Validation that did not occur must never be claimed.
C11 — Failed validation triggers diagnosis, not blind patching.
C12 — High-risk changes must be recoverable.
C13 — Completed changes must leave traceable state.
```

---

# 7.37 Core Principle

The AICF Change & Validation Model can be summarized as:

> **Bound the change before making it. Match autonomy to risk. Validate what changed and what must not break. Use evidence rather than confidence. Never confuse generated code with completed engineering.**

---

# 7.38 Relationship to Other AICF Sections

The framework now has the following control chain:

```text
SECTION 2
Core Principles
        ↓
SECTION 3
AI Behaviour Contract
        ↓
SECTION 4
Operating Model
        ↓
SECTION 5
Context & Memory Model
        ↓
SECTION 6
Truth / Uncertainty / Decision Model
        ↓
SECTION 7
Change & Validation Model
```

Together these establish the primary AICF engineering control system.

The next section will define **Project Modes** — how this common system adapts itself to Greenfield, Existing Systems, Migration, Feature Development, Bug Fixes, Refactoring, Integration, Optimization, and Maintenance without creating separate frameworks for each.
