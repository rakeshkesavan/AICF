# AICF Framework Definition v0.1

## 4. Operating Model

### 4.1 Purpose

The AICF Operating Model defines how AI-assisted software development progresses from an initial requirement to a validated and recoverable implementation.

The model provides a common lifecycle across:

* Greenfield development
* Existing applications
* Feature development
* Bug fixes
* Refactoring
* Migration
* Modernization
* Integration
* Optimization
* Maintenance

The lifecycle remains consistent while the depth and activities within each stage vary according to the project's complexity, risk, and uncertainty.

---

# 4.2 The AICF Development Lifecycle

AICF uses six primary stages:

```text
DISCOVER
    ↓
DEFINE
    ↓
PLAN
    ↓
EXECUTE
    ↓
VERIFY
    ↓
RECORD
```

These stages form a continuous development loop:

```text
                    ┌───────────────┐
                    │    DISCOVER   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │     DEFINE    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │      PLAN     │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    EXECUTE    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │     VERIFY    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    RECORD     │
                    └───────┬───────┘
                            │
                            └──────────→ NEXT TASK
```

The lifecycle is iterative rather than strictly linear.

Discovery may reveal the need to redefine the requirement.

Validation may reveal the need to return to planning.

Implementation may reveal a previously unknown dependency.

AICF therefore permits controlled movement backwards through the lifecycle.

---

# 4.3 Stage 1 — DISCOVER

## Objective

Build sufficient understanding of the problem and the current system before defining an implementation.

Discovery answers:

> **What exists, what is needed, and what do we not yet know?**

---

## Activities

Depending on the project, discovery may include:

### Project discovery

* Identify project purpose
* Identify technology stack
* Identify repository structure
* Identify major components
* Identify external dependencies
* Identify existing documentation

### Requirement discovery

* Understand the business problem
* Identify stakeholders
* Identify expected behaviour
* Identify constraints
* Identify success criteria

### Existing-system discovery

* Inspect relevant code
* Trace execution paths
* Identify dependencies
* Identify current behaviour
* Identify existing patterns
* Inspect tests

### Migration discovery

* Analyse source system
* Analyse target system
* Identify compatibility gaps
* Identify data dependencies
* Identify integration dependencies
* Identify migration risks

---

## Discovery Output

Discovery should produce sufficient understanding to proceed.

Typical outputs include:

```text
Current State
Relevant Context
Known Constraints
Dependencies
Risks
Unknowns
Initial Findings
```

Discovery does not necessarily require a formal document for every task.

The artifact requirements will be defined in Phase 2.

---

## Discovery Gate

Before moving forward, the agent should determine:

> **Do I understand enough to define the work safely?**

If yes:

```text
DISCOVER → DEFINE
```

If no:

```text
DISCOVER → MORE DISCOVERY
```

or, where human information is required:

```text
DISCOVER → BLOCKED / QUESTION
```

---

# 4.4 Stage 2 — DEFINE

## Objective

Convert the discovered problem into a clear, bounded engineering objective.

Define answers:

> **What exactly are we going to change, and what does success look like?**

---

## Required concepts

A meaningful task should establish, where applicable:

```text
Objective
Scope
Non-goals
Requirements
Acceptance Criteria
Constraints
Dependencies
Risks
```

---

## Scope

Scope defines what the task is expected to accomplish.

Example:

```text
Implement employee profile editing.

Included:
- Profile form
- Validation
- Update API integration
- Success/error states

Excluded:
- Employee creation
- Employee deletion
- Permission redesign
```

---

## Acceptance Criteria

Acceptance criteria define observable success.

They should be as testable as practical.

Poor:

```text
The page should be user friendly.
```

Better:

```text
A user can edit the employee's name and department,
submit the form, and see the updated values after a
successful response.
```

---

## Definition Gate

Before moving to planning:

```text
Is the desired outcome sufficiently clear?
Is the scope bounded?
Are critical unknowns resolved?
Can success be evaluated?
```

If not, the task returns to discovery or requests clarification.

---

# 4.5 Stage 3 — PLAN

## Objective

Determine the safest and most appropriate way to implement the defined change.

Planning answers:

> **How should this change be implemented?**

---

## Planning Activities

The agent may determine:

* implementation approach
* affected components
* affected files
* data flow
* API changes
* database changes
* integration changes
* testing strategy
* migration strategy
* risks
* rollback considerations

---

## Planning Depth

Planning must be proportional to risk.

### Simple

```text
Task
→ Implementation
```

### Moderate

```text
Task
→ Implementation approach
→ Affected areas
→ Validation
```

### Complex

```text
Requirement
→ Current architecture
→ Alternatives
→ Trade-offs
→ Risks
→ Recommended approach
→ Approval
→ Detailed implementation plan
```

---

## Plan Output

A plan should communicate:

```text
Approach
Affected Areas
Implementation Steps
Risks
Validation Strategy
Dependencies
```

It should not become a detailed prediction of every line of code.

The plan is an engineering direction, not a substitute for implementation.

---

# 4.6 Planning Gate

Human approval may be required when the plan introduces:

* significant architectural changes
* high-risk migrations
* security-sensitive changes
* destructive operations
* major infrastructure changes
* material business-rule changes
* large change-surface increases

Otherwise, the agent may proceed autonomously when project rules permit it.

---

# 4.7 Stage 4 — EXECUTE

## Objective

Implement the approved change within the defined scope.

Execution is where the AI agent modifies the actual project.

---

## Execution Rules

The agent must:

1. Follow project rules.
2. Follow the approved task scope.
3. Prefer existing patterns.
4. Minimize change surface.
5. Avoid unrelated modifications.
6. Preserve existing behaviour unless intentionally changed.
7. Maintain code quality.
8. Add or update appropriate tests.
9. Surface newly discovered risks.
10. Stop when safe execution becomes impossible.

---

## Incremental Execution

Complex tasks should be implemented incrementally.

Instead of:

```text
Build entire feature
```

prefer:

```text
Task 1 → Validate
Task 2 → Validate
Task 3 → Validate
Task 4 → Validate
```

This creates smaller failure domains and easier recovery.

---

## Execution State

During execution the project may enter:

```text
IN PROGRESS
BLOCKED
NEEDS DECISION
FAILED
READY FOR VERIFICATION
```

The current state should remain recoverable.

---

# 4.8 Stage 5 — VERIFY

## Objective

Determine whether the implementation actually satisfies the defined requirements without introducing unacceptable regressions.

Verification answers:

> **Did we build the right thing, and did we build it correctly?**

---

## Verification Layers

AICF defines a layered validation model:

```text
L1  Syntax / Build
 ↓
L2  Type Safety
 ↓
L3  Static Analysis / Lint
 ↓
L4  Unit Tests
 ↓
L5  Integration Tests
 ↓
L6  Functional Validation
 ↓
L7  Regression Validation
 ↓
L8  Security Validation
 ↓
L9  Performance Validation
 ↓
L10 Architecture / Compliance Validation
```

Not every task requires every layer.

The required verification depth should be determined by:

* task type
* risk
* affected systems
* project requirements
* existing project standards

---

## Verification Results

The agent must explicitly distinguish:

```text
PASSED
FAILED
PARTIALLY PASSED
NOT RUN
NOT APPLICABLE
BLOCKED
```

The agent must never imply that a validation step occurred when it did not.

---

## Verification Failure

When verification fails:

```text
VERIFY
  ↓
FAILURE
  ↓
DIAGNOSE
  ↓
REASSESS
  ↓
CORRECTIVE PLAN
  ↓
EXECUTE
  ↓
VERIFY
```

Repeated failures should trigger reassessment of the approach rather than uncontrolled patching.

---

# 4.9 Stage 6 — RECORD

## Objective

Persist the knowledge generated during the development cycle.

Record answers:

> **What changed, what did we learn, and what must the next agent know?**

---

## Information That May Be Recorded

Depending on significance:

```text
Current State
Task Status
Decisions
Assumptions
Known Issues
Validation Results
Architecture Changes
Important Discoveries
Remaining Work
```

---

## Avoid Documentation Noise

Not every implementation detail should become permanent documentation.

Record information when it has future engineering value.

For example:

### Worth recording

```text
The system uses asynchronous event processing because
the external payment provider can take several seconds
to return.
```

### Usually not worth recording

```text
Changed line 47 in EmployeeForm.tsx.
```

unless that information is relevant to future work.

---

# 4.10 Completion Gate

A task is considered complete only when:

```text
Requirement satisfied
        +
Implementation complete
        +
Appropriate validation passed
        +
Relevant state recorded
```

Therefore:

```text
CODE GENERATED ≠ DONE
```

and:

```text
COMPILES ≠ DONE
```

---

# 4.11 Human Interaction Model

AICF does not require human involvement at every stage.

Instead, human involvement is based on:

```text
Risk
+
Uncertainty
+
Impact
+
Reversibility
```

This creates three autonomy levels.

---

## Level A — Autonomous

The agent can:

* inspect
* implement
* test
* document

without requiring approval.

Typical examples:

* typo fixes
* isolated UI changes
* straightforward bug fixes
* tests
* low-risk refactoring

---

## Level B — Supervised

The agent can investigate and prepare implementation but should obtain confirmation for material decisions.

Typical examples:

* moderate architectural changes
* API changes
* database modifications
* cross-module changes
* significant refactoring

---

## Level C — Human Controlled

The agent should not independently execute the consequential operation.

Typical examples:

* destructive migrations
* production data deletion
* major security changes
* authentication architecture changes
* payment logic changes
* irreversible infrastructure operations

The exact classification will be defined in the AICF Change & Validation Model.

---

# 4.12 Lifecycle Adaptation by Task Type

The six-stage lifecycle remains constant, but the emphasis changes.

| Task            | Primary emphasis                               |
| --------------- | ---------------------------------------------- |
| Greenfield      | Discover → Define → Plan                       |
| Existing system | Discover → Inspect → Define                    |
| Feature         | Define → Plan → Execute                        |
| Bug fix         | Discover → Diagnose → Verify                   |
| Refactor        | Discover → Plan → Regression                   |
| Migration       | Discover → Plan → Incremental Execute → Verify |
| Optimization    | Measure → Plan → Execute → Measure             |
| Integration     | Discover → Define → Plan → Verify              |

This allows AICF to remain a single framework rather than becoming a collection of unrelated workflows.

---

# 4.13 Re-entry and Feedback

AICF is intentionally non-linear.

Any stage may cause re-entry into an earlier stage.

Examples:

### Discovery reveals unclear requirements

```text
DISCOVER
   ↓
DEFINE
   ↓
UNKNOWN
   ↓
DISCOVER / QUESTION
```

### Planning reveals architecture conflict

```text
PLAN
 ↓
CONFLICT
 ↓
DISCOVER
 ↓
REDEFINE
 ↓
PLAN
```

### Verification exposes wrong assumptions

```text
VERIFY
 ↓
FAIL
 ↓
REASSESS
 ↓
DEFINE / PLAN
```

This prevents the agent from blindly continuing down an invalid path.

---

# 4.14 The AICF Development Loop

The complete operating model is therefore:

```text
                     ┌───────────────┐
                     │    DISCOVER   │
                     │ What exists?  │
                     │ What's known? │
                     │ What's missing│
                     └───────┬───────┘
                             ↓
                     ┌───────────────┐
                     │     DEFINE    │
                     │ What changes? │
                     │ What's scope? │
                     └───────┬───────┘
                             ↓
                     ┌───────────────┐
                     │      PLAN     │
                     │ How to change?│
                     │ What are risks│
                     └───────┬───────┘
                             ↓
                     ┌───────────────┐
                     │    EXECUTE    │
                     │ Make changes  │
                     └───────┬───────┘
                             ↓
                     ┌───────────────┐
                     │     VERIFY    │
                     │ Does it work? │
                     │ Any regression│
                     └───────┬───────┘
                             ↓
                     ┌───────────────┐
                     │    RECORD     │
                     │ Preserve state│
                     │ & knowledge   │
                     └───────┬───────┘
                             ↓
                        NEXT TASK
```

---

# 4.15 Operating Principle

The AICF operating model can be summarized as:

> **Don't code from a prompt. Develop from a controlled engineering cycle.**

The agent should continuously move between:

```text
Understanding
    ↕
Decision
    ↕
Implementation
    ↕
Evidence
```

until the defined outcome is achieved and the resulting project state is preserved.

---

# 4.16 Relationship to Other AICF Sections

The Operating Model defines **when and how work progresses**.

It will be complemented by:

```text
Section 2 — Core Principles
        ↓
Why the framework behaves this way

Section 3 — AI Behaviour Contract
        ↓
How the agent behaves

Section 4 — Operating Model
        ↓
How development progresses

Section 5 — Context & Memory Model
        ↓
What information the agent receives

Section 6 — Truth, Uncertainty & Decision Model
        ↓
How the agent handles incomplete knowledge

Section 7 — Change & Validation Model
        ↓
How changes and quality are controlled
```

Together these form the core AICF engineering system.
