# AICF Cross-Artifact Conventions

## 1. Purpose

This specification defines the common conventions used across AICF artifacts.

It establishes:

* identifiers
* naming
* statuses
* references
* timestamps
* versioning
* authority
* lifecycle transitions
* artifact relationships
* conflict resolution
* archival and deprecation

The objective is interoperability between:

* humans
* AI agents
* different AI tools
* future AICF tooling

---

# 2. Design Principle

AICF artifacts should behave like a **small knowledge system**, not a collection of unrelated Markdown documents.

Therefore:

> **Identity, relationships, status, authority, and lifecycle must be predictable across artifacts.**

---

# 3. Artifact Identity

Every persistent AICF record should have a stable identifier.

Recommended formats:

```text
REQ-001
DEC-001
TASK-001
VAL-001
DOMAIN-001
FEATURE-001
```

The identifier should:

* be unique within the project
* never be reused
* remain stable throughout the artifact lifecycle
* be independent of the filename

---

# 4. Identifier Scope

IDs are unique within their artifact type.

Therefore:

```text
TASK-001
REQ-001
DEC-001
```

may all coexist.

This makes references immediately understandable.

---

# 5. ID Assignment

IDs should normally be sequential.

Example:

```text
TASK-001
TASK-002
TASK-003
```

Gaps are acceptable.

An abandoned or deleted record must not cause its ID to be reused.

The exact mechanism for ID allocation may later be automated by tooling.

---

# 6. Filenames

Recommended format:

```text
<ID>-<short-descriptive-name>.md
```

Examples:

```text
REQ-001-user-registration.md
DEC-004-authentication-strategy.md
TASK-012-search-filtering.md
VAL-012-search-filtering.md
```

The filename is primarily for human navigation.

The ID is the canonical identity.

---

# 7. Naming Rules

Names should be:

* descriptive
* concise
* stable
* lowercase after the ID
* hyphen separated

Prefer:

```text
TASK-012-search-filtering.md
```

Avoid:

```text
TASK-012-final-new-search-v2.md
```

If the subject changes materially, the artifact itself should be updated or superseded rather than creating confusing filename versions.

---

# 8. Status Model

AICF uses status to communicate **actual lifecycle state**.

Status should never represent aspiration.

For example:

```text
IN_PROGRESS
```

means work is actually underway.

It does not mean:

> "We intend to start this soon."

---

# 9. Common Status Vocabulary

Different artifact types may require different statuses.

The following vocabulary should be standardized where applicable:

```text
PROPOSED
DRAFT
DEFINED
PLANNED
IN_PROGRESS
VERIFYING
COMPLETED
PARTIALLY_COMPLETED
BLOCKED
FAILED
CANCELLED
ACCEPTED
REJECTED
SUPERSEDED
DEPRECATED
```

Not every artifact needs every status.

---

# 10. Task Status

Recommended:

```text
PROPOSED
DEFINED
PLANNED
IN_PROGRESS
VERIFYING
COMPLETED
PARTIALLY_COMPLETED
BLOCKED
FAILED
CANCELLED
```

Typical lifecycle:

```text
PROPOSED
   ↓
DEFINED
   ↓
PLANNED
   ↓
IN_PROGRESS
   ↓
VERIFYING
   ↓
COMPLETED
```

A task may transition to:

```text
BLOCKED
FAILED
CANCELLED
PARTIALLY_COMPLETED
```

at appropriate points.

---

# 11. Requirement Status

Recommended:

```text
PROPOSED
ACCEPTED
IN_PROGRESS
SATISFIED
REJECTED
SUPERSEDED
DEPRECATED
```

An accepted requirement should not be silently rewritten when its intent changes materially.

---

# 12. Decision Status

Recommended:

```text
PROPOSED
ACCEPTED
REJECTED
SUPERSEDED
DEPRECATED
```

A decision becomes active only when appropriately accepted.

---

# 13. Validation Status

Recommended:

```text
PASSED
FAILED
PARTIALLY_PASSED
NOT_RUN
NOT_APPLICABLE
BLOCKED
```

Validation status represents evidence, not expectation.

---

# 14. Feature Status

Recommended:

```text
PROPOSED
PLANNED
IN_PROGRESS
COMPLETED
PARTIALLY_COMPLETED
DEPRECATED
```

Projects may simplify this where necessary.

---

# 15. Domain Status

Domains generally change slowly.

A minimal status model is sufficient:

```text
ACTIVE
DEPRECATED
```

A domain does not need a task-like lifecycle.

---

# 16. Status Transition Rules

Status transitions should reflect legitimate lifecycle movement.

The AI should not arbitrarily jump states when doing so would hide meaningful work.

For example:

```text
PROPOSED → COMPLETED
```

may be inappropriate for a complex task because it hides definition, implementation, and validation.

However, lightweight projects may intentionally simplify their lifecycle.

The framework should favour **truthful state over procedural ceremony**.

---

# 17. References

AICF uses stable IDs for cross-artifact references.

Example:

```text
Related Requirement:
- REQ-012

Related Task:
- TASK-031

Related Decision:
- DEC-008

Validation:
- VAL-031
```

References should be added when they provide useful traceability.

Not every relationship requires a reference.

---

# 18. Bidirectional References

Where practical, important relationships may be represented from both sides.

Example:

`TASK-031`:

```text
Requirement:
REQ-012
```

`REQ-012`:

```text
Implementation Task:
TASK-031
```

However, AICF should avoid requiring perfect bidirectional synchronization for every relationship.

The primary artifact should remain authoritative for its own information.

---

# 19. Relationship Types

Common relationships include:

```text
IMPLEMENTS
SATISFIES
DEPENDS_ON
RELATED_TO
DERIVED_FROM
SUPERSEDES
SUPERSEDED_BY
VALIDATES
AFFECTS
CONSTRAINED_BY
```

These relationships may be represented explicitly when useful.

---

# 20. Requirement Traceability

The preferred engineering trace is:

```text
Requirement
    ↓
Task
    ↓
Implementation
    ↓
Validation
```

For decisions:

```text
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

This provides enough traceability without requiring every source-code line to be linked to a requirement.

---

# 21. Decision Traceability

Material decisions should be traceable to the work they influence.

Example:

```text
DEC-008
Authentication strategy

Related:
REQ-012
TASK-031
TASK-034
```

If the decision is superseded:

```text
DEC-008
Status: SUPERSEDED
Superseded By: DEC-021
```

The old decision remains available for historical reasoning.

---

# 22. Timestamps

Artifacts may include:

```text
created
updated
```

Recommended format:

```text
YYYY-MM-DD
```

or, where exact timing is important:

```text
YYYY-MM-DDTHH:MM:SSZ
```

Timestamps are metadata, not evidence of correctness.

The existence of a recently modified file does not mean its contents are current or authoritative.

---

# 23. Time and Freshness

AICF distinguishes:

**Created recently**

from:

**Knowledge is current.**

Freshness must be assessed using:

* content
* status
* implementation evidence
* related decisions
* current state

not timestamp alone.

---

# 24. Artifact Versioning

AICF artifacts generally should **not** use filenames such as:

```text
project-v2.md
project-final.md
project-final-final.md
```

Version history should normally be handled by source control.

Material semantic versions may be included inside an artifact when necessary.

---

# 25. Framework Version vs Project Artifact Version

These are different concepts.

### AICF Framework Version

Example:

```text
AICF v0.1
```

Defines the framework itself.

### Artifact Version

Represents changes to a specific project artifact where explicit versioning is useful.

### Project Version

Represents the software product/release.

These must not be conflated.

---

# 26. Authority Model

Authority is **context dependent**.

No artifact should be considered universally authoritative for every question.

The AI should ask:

> **“Authoritative for what?”**

Examples:

| Question                       | Strongest Source                       |
| ------------------------------ | -------------------------------------- |
| What should the feature do?    | Accepted requirement                   |
| Why was architecture chosen?   | Accepted decision                      |
| What rules must AI follow?     | Rules                                  |
| What is current project state? | State + evidence                       |
| What code currently exists?    | Source                                 |
| Did a test actually pass?      | Validation evidence / execution result |
| What happens at runtime?       | Runtime evidence                       |

---

# 27. Intended vs Actual State

AICF explicitly distinguishes:

### Intended state

What requirements, decisions, or documentation say should exist.

### Actual state

What source code, tests, infrastructure, or runtime evidence shows exists.

Example:

```text
Requirement:
OTP must expire after 10 minutes.

Implementation:
OTP currently expires after 15 minutes.
```

The requirement remains the intended behaviour.

The implementation reveals actual behaviour.

The AI should not silently modify either artifact to make the contradiction disappear.

It should surface the conflict.

---

# 28. Conflict Resolution

When two artifacts disagree:

```text
1. Identify the conflicting claims.
2. Identify the sources.
3. Determine their authority for the question.
4. Check freshness.
5. Inspect implementation/evidence.
6. Determine intended vs actual state.
7. Determine whether the difference is intentional.
8. Resolve or escalate.
9. Record the material resolution.
```

The agent must never resolve conflicts merely by choosing the document it read most recently.

---

# 29. Staleness

An artifact may be marked stale or superseded when appropriate.

However, AICF should prefer explicit lifecycle states over vague labels.

Prefer:

```text
Status: SUPERSEDED
Superseded By: DEC-021
```

over:

```text
Status: OLD
```

---

# 30. Deprecation

Deprecation means:

> The artifact is no longer active, but its historical existence remains useful.

Deprecated artifacts should remain discoverable unless there is a legitimate reason to remove them.

---

# 31. Deletion

AICF should favour deprecation over deletion for material engineering knowledge.

Deletion may be appropriate for:

* accidental artifacts
* duplicate artifacts
* temporary generated files
* incorrect records with no historical value
* sensitive information that must be removed

Deletion should not be used merely to hide inconvenient history.

---

# 32. Source of Truth

AICF does not create a single universal source of truth.

Instead:

> **Each information type should have a clear authoritative source.**

This creates a distributed but structured truth model.

```text
Rules       → rules.md
Requirements → requirements/
Decisions   → decisions/
Current State → state.md
Implementation → source
Evidence     → validation / execution
```

---

# 33. Duplicate Information

Avoid duplicating authoritative information.

For example, do not maintain:

```text
project.md:
Database = PostgreSQL

domain.md:
Database = PostgreSQL

feature.md:
Database = PostgreSQL

state.md:
Database = PostgreSQL
```

unless the statement has a different contextual purpose.

Prefer references to the authoritative source.

---

# 34. Derived Information

Some information may legitimately be derived.

Example:

`state.md`:

```text
Active Tasks:
TASK-012
TASK-014
```

The task artifacts remain authoritative for detailed task state.

`state.md` provides the project-level summary.

This distinction should be preserved.

---

# 35. Summary vs Source

AICF allows summaries.

But:

> **A summary should never silently become more authoritative than the information it summarizes.**

Example:

```text
state.md
↓
Summary of task status

tasks/TASK-012.md
↓
Detailed task state
```

If they conflict, the AI investigates rather than blindly overwriting either.

---

# 36. Artifact Integrity

An AI should avoid partial updates that leave an artifact misleading.

For example, do not update:

```text
Task Status: COMPLETED
```

before required validation has been performed.

Where multiple artifacts must change as part of one logical transition, update them coherently.

---

# 37. Atomicity of State Changes

Where practical, a meaningful lifecycle transition should update the relevant artifacts together.

Example:

Task completed:

```text
TASK-012
→ COMPLETED

VAL-012
→ PASSED

state.md
→ Remove TASK-012 from Active Work
→ Add to Recently Completed
```

This reduces inconsistent project state.

---

# 38. Orphan Detection

An artifact becomes potentially orphaned when:

* its referenced parent no longer exists
* its requirement is removed
* its task is cancelled
* its decision is superseded
* its feature is deprecated

Orphaned artifacts should be reviewed rather than automatically deleted.

---

# 39. Context Retrieval Priority

When selecting artifacts, prioritize:

1. relevance
2. authority
3. freshness
4. task dependency
5. risk
6. context cost

This reinforces the AICF principle:

> **Minimum sufficient context.**

---

# 40. Context Cost

AICF should consider not only whether context is relevant but whether loading it provides enough value relative to its cost.

For example:

A 2,000-line architecture document may be relevant.

But if the task only needs one API contract, loading the entire document may be inefficient.

The agent should retrieve the smallest useful portion where tooling permits.

---

# 41. Context Escalation Rule

The default sequence is:

```text
Core Context
   ↓
Task Context
   ↓
Relevant Context
   ↓
Source
   ↓
Evidence
```

Escalate only when:

* uncertainty remains
* dependency appears
* conflict appears
* risk increases
* implementation requires additional context
* validation requires additional evidence

---

# 42. Human Authority

AICF distinguishes:

### Information authority

Which artifact should be trusted for a fact?

### Decision authority

Who is allowed to decide?

### Execution authority

What may the AI actually change?

These are separate concepts.

An AI may have information authority without having decision authority.

---

# 43. Example

Suppose `project.md` says:

> PostgreSQL is the primary database.

The AI may treat this as project context.

But if the task requires changing the database architecture:

```text
Information:
PostgreSQL is current.

Decision:
Whether to replace it.

Authority:
May require human approval.

Execution:
May be prohibited without approval.
```

This distinction prevents accidental architectural autonomy.

---

# 44. Convention for Unknowns

Unknowns should be expressed explicitly.

Recommended:

```text
Open Unknowns

- OTP expiry requirement has not been confirmed.
- Production rate limit is unknown.
```

Avoid:

```text
TODO: figure this out
```

unless it is purely an implementation task.

---

# 45. Convention for Assumptions

Material assumptions should state:

```text
Assumption
Reason
Risk
Reversibility
```

Example:

```text
Assumption:
Use the existing email provider.

Reason:
Existing integration already supports transactional email.

Risk:
Low.

Reversibility:
High.
```

---

# 46. Convention for Evidence

Evidence should identify what was actually observed.

Example:

```text
Evidence:
- Unit tests passed.
- Integration test returned HTTP 200.
- QA deployment completed.
- Query latency decreased from 820ms to 310ms.
```

Avoid unsupported statements such as:

> "This should work."

That is reasoning, not evidence.

---

# 47. Convention for Notes

Notes are temporary-supporting information.

If a note becomes material and durable, it should move into the appropriate artifact.

This prevents `Notes` sections from becoming uncontrolled knowledge stores.

---

# 48. Convention for Human Decisions

When a human provides an explicit decision:

```text
Decision:
Use PostgreSQL.

Authority:
Engineering Lead.

Status:
ACCEPTED.
```

The AI should record the decision and rationale where sufficient information exists.

It should not invent rationale that the human did not provide.

---

# 49. Convention for AI Recommendations

AI recommendations should remain distinguishable from accepted decisions.

Example:

```text
Recommendation:
Use PostgreSQL.

Status:
PROPOSED.
```

Only after appropriate acceptance:

```text
Status:
ACCEPTED.
```

This prevents AI suggestions from becoming project facts accidentally.

---

# 50. Canonical Cross-Artifact Model

The complete convention system can be summarized as:

```text id="yq5n8w"
IDENTITY
   ↓
RELATIONSHIP
   ↓
STATUS
   ↓
AUTHORITY
   ↓
EVIDENCE
   ↓
LIFECYCLE
   ↓
CURRENT STATE
```

These conventions allow different AI agents and tools to interpret the same repository consistently.

---

# 51. Core Principle

> **AICF artifacts should be identifiable, traceable, authoritative for their intended purpose, honest about their state, and lightweight enough to maintain.**

The objective is not perfect documentation.

The objective is **reliable continuity of engineering knowledge**.
