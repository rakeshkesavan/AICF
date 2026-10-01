# AICF Canonical Artifact Schemas — Extended Artifacts

## 1. Purpose

This specification defines the remaining canonical AICF artifacts:

1. `requirement.md`
2. `domain.md`
3. `feature.md`
4. `validation.md`
5. `environment.md`

Together with the foundational artifacts, these provide the complete initial AICF operational vocabulary.

The design remains intentionally lightweight.

> **Not every project needs every artifact.**

---

# 2. Requirement Artifact

## 2.1 Purpose

A requirement defines an expected system behaviour, capability, constraint, or outcome.

It answers:

> **“What must be true?”**

Requirements provide the primary bridge between business intent and engineering execution.

---

## 2.2 Schema

```markdown
# REQ-XXX — Requirement Title

## Status

PROPOSED

## Type

Functional

## Objective

...

## Description

...

## Rationale

...

## Acceptance Criteria

- [ ] ...
- [ ] ...

## Constraints

- ...

## Dependencies

- ...

## Related Domain

- DOMAIN-...

## Related Feature

- FEATURE-...

## Related Decisions

- DEC-...

## Related Tasks

- TASK-...

## Notes

...
```

---

## 2.3 Required Information

* Requirement ID
* Status
* Objective
* Description
* Acceptance Criteria

---

## 2.4 Optional Information

* Type
* Rationale
* Constraints
* Dependencies
* Domain
* Feature
* Decisions
* Tasks
* Notes

---

## 2.5 Requirement States

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

An AI should not silently change an accepted requirement.

Changes to material requirements should be explicit and traceable.

---

# 3. Domain Artifact

## 3.1 Purpose

A domain artifact captures persistent knowledge about a business or technical area.

It answers:

> **“What should an AI understand about this area of the system?”**

---

## 3.2 Schema

```markdown
# DOMAIN-XXX — Domain Name

## Purpose

...

## Scope

...

## Terminology

- **Term:** Meaning

## Entities

- ...

## Rules

- ...

## Workflows

1. ...

## Dependencies

- ...

## Related Features

- FEATURE-...

## Related Decisions

- DEC-...

## Known Constraints

- ...

## Open Unknowns

- ...
```

---

## 3.3 Required Information

* Domain ID
* Purpose
* Scope

---

## 3.4 Optional Information

* Terminology
* Entities
* Rules
* Workflows
* Dependencies
* Features
* Decisions
* Constraints
* Open Unknowns

---

## 3.5 Design Rule

A domain should represent a meaningful contextual boundary.

Do not create a domain artifact merely because a folder or software module exists.

---

# 4. Feature Artifact

## 4.1 Purpose

A feature artifact captures persistent knowledge about a meaningful capability or workflow.

It answers:

> **“What does this capability do and how does it fit into the system?”**

---

## 4.2 Schema

```markdown
# FEATURE-XXX — Feature Name

## Status

PLANNED

## Purpose

...

## User / Business Outcome

...

## Scope

### Included

- ...

### Excluded

- ...

## Workflow

1. ...

## Requirements

- REQ-...

## Business Rules

- ...

## Technical Context

...

## Dependencies

- ...

## Related Domain

- DOMAIN-...

## Related Decisions

- DEC-...

## Related Tasks

- TASK-...

## Validation

- VAL-...

## Known Issues

- ...

## Open Questions

- ...
```

---

## 4.3 Required Information

* Feature ID
* Status
* Purpose
* Scope
* Requirements

---

## 4.4 Optional Information

* User outcome
* Workflow
* Business rules
* Technical context
* Dependencies
* Domain
* Decisions
* Tasks
* Validation
* Known issues
* Open questions

---

## 4.5 Design Rule

Feature artifacts should describe the capability, not become implementation logs.

Implementation detail belongs primarily in:

* source code
* task context
* decisions
* architecture documentation where appropriate

---

# 5. Validation Artifact

## 5.1 Purpose

A validation artifact records evidence that a change, requirement, system property, or migration state has been verified.

It answers:

> **“What did we actually verify, and what evidence do we have?”**

---

## 5.2 Schema

````markdown
# VAL-XXX — Validation Title

## Status

PASSED

## Related Task

- TASK-XXX

## Related Requirement

- REQ-XXX

## Validation Level

V4 — Unit

## Objective

...

## Validation Performed

...

## Method

```text
command or action
````

## Expected Result

...

## Actual Result

...

## Evidence

* ...

## Failures

* ...

## Known Limitations

* ...

## Environment

* QA

## Conclusion

...

````

---

# 5.3 Required Information

- Validation ID
- Status
- Validation level
- Objective
- Validation performed
- Actual result
- Conclusion

---

# 5.4 Optional Information

- Related task
- Requirement
- Method
- Expected result
- Evidence
- Failures
- Limitations
- Environment

---

# 5.5 Validation Status

Recommended:

```text
PASSED
FAILED
PARTIALLY_PASSED
NOT_RUN
NOT_APPLICABLE
BLOCKED
````

---

# 5.6 Evidence Rule

Validation records must represent actual evidence.

The AI must never generate:

```text
Status: PASSED
```

merely because the implementation appears correct.

---

# 6. Environment Artifact

## 6.1 Purpose

The environment artifact describes the environments in which the system is developed, tested, deployed, or operated.

It answers:

> **“Where does this system run, and what differs between environments?”**

---

## 6.2 Schema

```markdown
# Environment

## Local

### Purpose

...

### Configuration

...

### Data

...

### External Systems

...

---

## Development

### Purpose

...

### Configuration

...

### Data

...

### External Systems

...

---

## QA

### Purpose

...

### Configuration

...

### Data

...

### External Systems

...

---

## Staging

...

---

## Production

...
```

---

# 6.3 Required Information

At least the environments relevant to the project should be identified.

For each relevant environment:

* purpose
* important differences
* relevant external systems

---

# 6.4 Optional Information

* deployment mechanism
* data characteristics
* validation restrictions
* operational constraints
* feature flags
* environment-specific dependencies

---

# 6.5 Security Rule

Environment artifacts must never contain:

* credentials
* API keys
* passwords
* private keys
* secrets
* sensitive production data

They may reference the existence of secure configuration without exposing it.

---

# 7. Extended Artifact Relationships

The complete AICF information model is now:

```text
                    PROJECT
                       │
          ┌────────────┼────────────┐
          │            │            │
       DOMAIN       FEATURE      DECISION
          │            │            │
          └──────┬─────┘            │
                 ↓                  │
             REQUIREMENT ──────────┘
                 │
                 ↓
                TASK
                 │
                 ↓
          IMPLEMENTATION
                 │
                 ↓
             VALIDATION
                 │
                 ↓
               STATE
```

`RULES` and `ENVIRONMENT` provide cross-cutting context.

---

# 8. Artifact Responsibility Matrix

| Artifact    | Primary Question                     | Persistent? | Typical Update |
| ----------- | ------------------------------------ | ----------: | -------------- |
| Rules       | How must we operate?                 |         Yes | Rare           |
| Project     | What is the system?                  |         Yes | Low            |
| State       | Where are we now?                    |         Yes | High           |
| Environment | Where does it run?                   |         Yes | Medium         |
| Domain      | What should we know about this area? |         Yes | Medium         |
| Feature     | What does this capability do?        |         Yes | Medium         |
| Requirement | What must be true?                   |         Yes | Medium         |
| Decision    | Why was this choice made?            |         Yes | As needed      |
| Task        | What are we doing?                   |         Yes | High           |
| Validation  | What did we prove?                   |         Yes | High           |

---

# 9. Artifact Creation Principle

AICF should not require all artifacts to exist at project initialization.

A project may begin with:

```text
.aicf/
├── rules.md
├── project.md
└── state.md
```

As complexity increases:

```text
requirements/
domains/
features/
decisions/
tasks/
validation/
environment.md
```

are introduced when justified.

---

# 10. Core Principle

> **AICF artifacts should emerge from engineering needs, not from a requirement to fill every template.**

The framework should remain usable for both a two-week project and a multi-year system.
