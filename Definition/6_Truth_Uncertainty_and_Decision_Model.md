# AICF Framework Definition v0.1

## 6. Truth, Uncertainty & Decision Model

### 6.1 Purpose

The Truth, Uncertainty & Decision Model defines how an AICF agent should:

* determine what is known
* distinguish facts from inference
* identify assumptions
* recognize unknown information
* resolve conflicting information
* assess uncertainty
* make decisions
* record material decisions
* determine when it should proceed, ask, or stop

The purpose is not to eliminate uncertainty.

Software development inevitably involves incomplete information.

The objective is:

> **Make uncertainty visible and prevent unsupported assumptions from silently becoming implementation facts.**

---

# 6.2 The Fundamental Problem

AI agents are optimized to produce useful responses.

Software engineering requires something different:

> **Correct decisions based on sufficient evidence.**

An agent can produce a technically plausible implementation while being completely wrong about the underlying requirement.

For example:

```text id="zblqj2"
Requirement:
"Users can approve requests."

Possible interpretations:

Manager approval
Admin approval
Multi-level approval
Role-based approval
Any authorized user
Sequential approval
Parallel approval
```

The AI may choose one.

The fact that it can implement that interpretation does not mean that interpretation is correct.

AICF therefore separates:

```text id="b0j7r5"
Knowledge
   ↓
Confidence
   ↓
Decision
   ↓
Implementation
```

---

# 6.3 Knowledge States

AICF defines four primary knowledge states.

```text id="3wq2eh"
KNOWN
INFERRED
ASSUMED
UNKNOWN
```

These states should be used consistently across project work.

---

# 6.4 KNOWN

Information is **KNOWN** when it is directly supported by reliable evidence.

Examples:

* explicitly stated requirement
* approved architecture
* recorded decision
* current source implementation
* passing test demonstrating behaviour
* official technical documentation
* verified runtime behaviour

Example:

```text id="g1y8vr"
KNOWN:
The project uses PostgreSQL.
Evidence:
Project architecture documentation and database configuration.
```

Known information should generally be safe to use as a foundation for implementation.

---

# 6.5 INFERRED

Information is **INFERRED** when it is strongly derived from available evidence but is not explicitly stated.

Example:

```text id="4gc5cr"
Existing APIs use REST.
New API is expected to follow REST.
```

The second statement may be a strong inference.

However:

```text id="m3g8x0"
Inference ≠ explicit decision
```

The agent should not silently elevate an inference into a project rule when the distinction matters.

---

# 6.6 ASSUMED

Information is **ASSUMED** when the agent chooses an interpretation because sufficient explicit information is unavailable.

Example:

```text id="p7k0r4"
Assumption:
Employee profile updates are allowed for HR managers.
Reason:
No explicit permission rule exists.
```

Assumptions may be acceptable when:

* risk is low
* the assumption is reversible
* existing patterns strongly support it
* clarification would create unnecessary interruption

Material assumptions should be recorded.

---

# 6.7 UNKNOWN

Information is **UNKNOWN** when the available evidence is insufficient to determine the correct answer.

Example:

```text id="9g4n0m"
UNKNOWN:
Whether employee termination requires dual approval.
```

The agent should not invent an answer.

Unknown information becomes particularly important when it affects:

* security
* data integrity
* financial behaviour
* business rules
* public APIs
* destructive operations
* architecture
* compliance

---

# 6.8 Knowledge State Transition

Information can evolve.

```text id="b5o0v9"
UNKNOWN
   ↓
Discovery
   ↓
INFERRED
   ↓
Confirmation
   ↓
KNOWN
```

Or:

```text id="y9o6r3"
UNKNOWN
   ↓
Low-risk assumption
   ↓
ASSUMED
   ↓
Validation
   ↓
KNOWN
```

AICF should allow knowledge states to become more certain as evidence becomes available.

---

# 6.9 Truth Hierarchy

When determining what to trust, AICF uses an evidence hierarchy.

```text id="1p1h8m"
T0 — Explicit approved requirement
T1 — Explicit project rule / specification
T2 — Recorded architectural or business decision
T3 — Current implementation
T4 — Tests / observable system behaviour
T5 — Verified technical documentation
T6 — Strong inference
T7 — Agent assumption
```

The exact ordering may vary by context.

For example, source code may provide stronger evidence of **current behaviour** than documentation, while approved requirements provide stronger authority for **intended behaviour**.

Therefore the hierarchy must be interpreted together with:

```text id="j9k3e2"
Authority
+
Freshness
+
Evidence
+
Intent
```

---

# 6.10 Authority vs Reality

AICF distinguishes between:

### Intended State

What the system is supposed to do.

Examples:

* requirements
* approved specifications
* architecture decisions

### Actual State

What the system currently does.

Examples:

* source code
* tests
* runtime behaviour
* database state

These may differ.

Example:

```text id="p9v1u7"
Requirement:
Users cannot delete records.

Implementation:
Delete endpoint exists.
```

The agent must not silently choose between them.

It should identify:

> **Requirement/implementation discrepancy.**

---

# 6.11 Contradiction Protocol

When two sources conflict, the agent should:

1. Identify the contradiction.
2. Identify each source.
3. Assess authority.
4. Assess freshness.
5. Determine whether the conflict is intentional.
6. Resolve through existing decisions or clarification.
7. Record the resolution when material.

Example:

```text id="i2m7q0"
Documentation:
PostgreSQL

Configuration:
MySQL

Action:
Do not assume either is correct.
Investigate current architecture and project intent.
```

---

# 6.12 Confidence Is Not Truth

AICF explicitly separates:

```text id="9g0f7k"
Confidence
```

from:

```text id="1w6y4r"
Evidence
```

An AI may be highly confident and still be wrong.

Therefore:

```text id="yq7c0h"
High confidence + weak evidence
        ≠
Known fact
```

AICF prioritizes evidence over model confidence.

---

# 6.13 Uncertainty Classification

Uncertainty should be classified by impact.

### U0 — Negligible

Uncertainty has no meaningful impact.

Example:

* internal variable naming
* formatting preference where project convention is clear

Proceed.

### U1 — Low

Uncertainty is reversible and low impact.

Example:

* minor UI implementation detail

Proceed with an explicit assumption when appropriate.

### U2 — Moderate

Uncertainty can affect behaviour or architecture.

Example:

* API response structure
* state-management approach

Investigate and clarify where practical.

### U3 — High

Uncertainty can cause material damage or incorrect system behaviour.

Example:

* authorization rules
* financial calculations
* data migration semantics

Do not silently assume.

### U4 — Critical

Uncertainty affects irreversible or highly consequential operations.

Example:

* production data deletion
* destructive migration
* security boundary
* payment settlement

Stop until sufficiently resolved.

---

# 6.14 The Proceed / Ask / Stop Model

AICF converts uncertainty into an action.

```text id="7n9c0f"
                 UNCERTAINTY
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
        LOW        MODERATE      HIGH
          │           │           │
       PROCEED       ASK         STOP
          │           │           │
     Assumption     Clarify    Resolve first
      if needed
```

The decision should consider:

```text id="s9f8y3"
Impact
+
Reversibility
+
Confidence
+
Cost of being wrong
```

---

# 6.15 Assumption Protocol

When the agent must make an assumption, it should:

```text id="q7y9y6"
1. State the assumption.
2. Explain why it is necessary.
3. Assess its risk.
4. Determine whether it is reversible.
5. Record it if material.
6. Continue only if permitted.
```

Example:

```text id="n0h7w3"
ASSUMPTION

The dashboard should display the user's local timezone.

Reason:
No timezone display requirement exists and the existing UI
uses local timezone formatting.

Risk:
Low

Reversible:
Yes

Action:
Proceed.
```

---

# 6.16 Decision Protocol

When a material decision is required, the agent should follow:

```text id="b2g9az"
Problem
   ↓
Evidence
   ↓
Constraints
   ↓
Options
   ↓
Trade-offs
   ↓
Recommendation
   ↓
Decision
   ↓
Record
```

The agent may recommend.

The authorized human or project governance mechanism establishes the decision where required.

---

# 6.17 Decision Categories

AICF distinguishes several decision types.

### Business Decision

Defines product or business behaviour.

### Product Decision

Defines user experience or product functionality.

### Architecture Decision

Defines system structure or technical direction.

### Implementation Decision

Defines how a specific task is implemented.

### Operational Decision

Defines deployment, infrastructure, monitoring, or runtime behaviour.

### Temporary Decision

A short-term choice made to unblock work.

Not every decision requires permanent documentation.

Material decisions do.

---

# 6.18 Decision Threshold

The agent should consider recording a decision when changing it later would:

* require significant rework
* affect multiple features
* affect architecture
* affect external integrations
* affect security
* affect data
* affect future development
* be difficult to reverse

Simple implementation choices generally do not require formal decision records.

---

# 6.19 Decision Record

A material decision should capture:

```text id="kr7t1k"
Decision ID
Date
Context
Problem
Options considered
Decision
Reason
Consequences
Status
```

Example:

```text id="e5c3j8"
ADR-007

Decision:
Use asynchronous processing for document generation.

Reason:
Generation may take several seconds and should not block
the request lifecycle.

Consequences:
Requires job tracking and status updates.

Status:
Accepted
```

---

# 6.20 Decision Status

Decisions should have explicit states:

```text id="a8g1vq"
PROPOSED
ACCEPTED
SUPERSEDED
REJECTED
DEPRECATED
```

This prevents old decisions from being treated as current.

---

# 6.21 Reopening Decisions

An agent may identify that an existing decision is no longer appropriate.

It should not silently replace it.

Instead:

```text id="t8v2k1"
Existing Decision
       ↓
New Evidence
       ↓
Conflict / Reassessment
       ↓
Recommendation
       ↓
Approval
       ↓
New Decision
       ↓
Old Decision → SUPERSEDED
```

This preserves decision history while allowing the architecture to evolve.

---

# 6.22 Evidence Record

For material decisions, the agent should preserve meaningful evidence where practical.

Evidence may include:

* requirement references
* source locations
* test results
* measurements
* benchmarks
* API documentation
* architectural analysis

The goal is not to create bureaucracy.

The goal is to make important decisions explainable.

---

# 6.23 Hallucination Control

AICF's hallucination-control strategy is therefore not a single instruction.

It is a layered mechanism:

```text id="2j4w5e"
Persistent Context
        ↓
Truth Classification
        ↓
Evidence Evaluation
        ↓
Uncertainty Detection
        ↓
Risk Assessment
        ↓
Proceed / Ask / Stop
        ↓
Decision Recording
        ↓
Validation
```

This is significantly stronger than:

> "Don't hallucinate."

---

# 6.24 The No-Fabrication Rule

The following is a strict AICF rule:

> **An agent must not fabricate project facts, APIs, schemas, business rules, credentials, system behaviour, test results, or external capabilities.**

If information is unavailable, it must be identified as unavailable.

Examples of prohibited behaviour:

```text id="s1j3j1"
Inventing an API endpoint
Inventing database fields
Inventing authentication rules
Inventing library behaviour
Claiming a test passed when it was not run
Claiming an integration exists when it was not verified
```

---

# 6.25 External Knowledge

When external technical information is required, the agent may use authoritative external sources where available.

Examples:

* official framework documentation
* official API documentation
* official library documentation
* verified specifications

External information should not automatically override project-specific decisions.

For example:

```text id="x4f8sm"
Framework documentation:
"Pattern A is recommended."

Project architecture:
"Pattern B is intentionally used."

```

The agent should understand why the project differs before changing it.

---

# 6.26 Unknowns as First-Class Project State

Important unresolved unknowns should be recorded.

Example:

```text id="j7v3m4"
OPEN QUESTION

Does a terminated employee retain access to historical
documents?

Impact:
Authorization behaviour

Status:
Awaiting product decision

Blocking:
Employee termination implementation
```

This is preferable to allowing the AI to make a hidden assumption.

---

# 6.27 Assumption Expiration

Assumptions should not become permanent facts merely because time passes.

Material assumptions should be revisited when:

* new evidence appears
* the feature expands
* the assumption affects another subsystem
* validation exposes a conflict
* the assumption becomes difficult to reverse

This prevents temporary shortcuts from silently becoming architecture.

---

# 6.28 Decision and State Relationship

Decisions affect project state.

```text id="3q8y8h"
Decision
   ↓
Implementation
   ↓
Validation
   ↓
Current State
```

If a decision changes:

```text id="c1j0f9"
Decision change
   ↓
Impact analysis
   ↓
Affected tasks
   ↓
Implementation changes
   ↓
Validation
```

This preserves consistency between what the project has decided and what it actually implements.

---

# 6.29 AICF Knowledge Model

The complete model is:

```text id="z6q2s0"
                    INFORMATION
                         │
             ┌───────────┼───────────┐
             ↓           ↓           ↓
           FACT       INFERENCE    UNKNOWN
             │           │
             │           ↓
             │       ASSUMPTION
             │           │
             └─────┬─────┘
                   ↓
                DECISION
                   ↓
             IMPLEMENTATION
                   ↓
                EVIDENCE
                   ↓
               VALIDATION
                   ↓
            PERSISTENT STATE
```

This creates a feedback loop between knowledge and implementation.

---

# 6.30 AICF Decision Matrix

The agent should use the following general decision model:

| Situation                         | Default Behaviour                   |
| --------------------------------- | ----------------------------------- |
| Explicit requirement              | Proceed                             |
| Existing established pattern      | Reuse                               |
| Strong inference, low risk        | Proceed with assumption if needed   |
| Moderate uncertainty              | Investigate / ask                   |
| Conflicting project information   | Stop and reconcile                  |
| High-risk unknown                 | Stop                                |
| Material architectural choice     | Recommend + approval where required |
| Destructive operation             | Explicit approval                   |
| Existing decision conflict        | Reassess; do not silently override  |
| Validation contradicts assumption | Reassess                            |
| Insufficient evidence             | Do not fabricate                    |

---

# 6.31 Core Principle

The Truth, Uncertainty & Decision Model can be summarized as:

> **Know what you know. Identify what you infer. Declare what you assume. Expose what you don't know. Use evidence to decide. Record decisions that matter. Never turn uncertainty into silent invention.**

---

# 6.32 Relationship to Other AICF Sections

This model connects the previous sections:

```text
Core Principles
       ↓
AI Behaviour
       ↓
Operating Model
       ↓
Context & Memory
       ↓
Truth / Uncertainty / Decisions
       ↓
Change & Validation
```

The next section will define the final major control layer:

> **What exactly is the AI allowed to change, how much can it change, when does it need approval, and how do we prove that the change is correct?**

That becomes **Section 7 — Change & Validation Model**.
