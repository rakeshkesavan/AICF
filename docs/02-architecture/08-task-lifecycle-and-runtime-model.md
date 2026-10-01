# AICF Task Lifecycle & Runtime Model

## 1. Purpose

The AICF Task Lifecycle defines how an engineering request moves through the AICF system from initial intent to verified completion.

It is the operational runtime model connecting:

* user intent
* project context
* requirements
* tasks
* AI reasoning
* implementation
* validation
* persistent state

The lifecycle must work across:

* greenfield development
* existing systems
* feature development
* bug fixes
* refactoring
* migrations
* integrations
* optimization
* maintenance

The same lifecycle applies to all modes.

Project mode changes the emphasis and controls, not the fundamental process.

---

# 2. Core Lifecycle

The canonical AICF lifecycle is:

```text
REQUEST
   ↓
ORIENT
   ↓
DISCOVER
   ↓
DEFINE
   ↓
PLAN
   ↓
AUTHORIZE
   ↓
EXECUTE
   ↓
VERIFY
   ↓
RECORD
   ↓
REPORT
   ↓
COMPLETE
```

The lifecycle is iterative.

Failures, discoveries, conflicts, or requirement changes may return the task to an earlier stage.

```text
             ┌─────────────────────┐
             │                     ↓
REQUEST → ORIENT → DISCOVER → DEFINE → PLAN
                              ↑      ↓
                              │  AUTHORIZE
                              │      ↓
                              │   EXECUTE
                              │      ↓
                              │   VERIFY
                              │      ↓
                              └── RECORD
                                     ↓
                                   REPORT
                                     ↓
                                  COMPLETE
```

---

# 3. Stage 0 — REQUEST

## Purpose

Receive an engineering intent.

A request may come from:

* developer
* product owner
* engineering manager
* issue tracker
* another AI agent
* automated system
* operational event

Examples:

> Add search filtering.

> Fix the checkout timeout.

> Migrate the database.

> Improve API performance.

The request is **intent**, not yet a fully executable task.

---

# 4. Request Normalization

The agent translates the request into an initial understanding.

It identifies:

* requested outcome
* apparent scope
* project mode
* affected area if known
* ambiguity
* likely risk

At this point, the agent should avoid premature implementation decisions.

Example:

```text id="l9p6xj"
Request:
"Make the dashboard faster."

Initial interpretation:
Optimization

Known:
Dashboard performance is perceived as slow.

Unknown:
- Which operation is slow?
- Under what workload?
- Current baseline?
- Target performance?

Next:
DISCOVER
```

---

# 5. Stage 1 — ORIENT

## Purpose

Establish sufficient project context to understand the request.

The agent loads the minimum relevant AICF context.

Default:

```text
rules.md
project.md
state.md
```

Then:

```text
active task
relevant domain
relevant feature
requirements
decisions
environment
```

as required.

---

## 5.1 Orientation Questions

The agent should determine:

```text
What project?
What objective?
What mode?
What is the current state?
What rules apply?
What work is already active?
What authority exists?
What relevant context exists?
```

---

# 6. Stage 2 — DISCOVER

## Purpose

Establish the actual situation before defining the work.

Discovery differs by project mode.

### Existing system

Inspect:

* architecture
* source
* tests
* runtime behaviour
* dependencies

### Bugfix

Establish:

* reproduction
* observed behaviour
* expected behaviour
* probable root cause

### Migration

Establish:

* current state
* target state
* compatibility
* dependencies
* rollback

### Optimization

Establish:

* baseline
* workload
* bottleneck
* target

### Greenfield

Establish:

* requirements
* constraints
* domain
* architecture options

---

# 7. Discovery Output

Discovery should produce enough evidence to answer:

```text
Current State
Relevant Components
Relevant Behaviour
Constraints
Dependencies
Risks
Unknowns
Evidence
```

Discovery does not need to produce a formal document every time.

Material findings should be persisted when they have durable value.

---

# 8. Stage 3 — DEFINE

## Purpose

Convert discovered information into a bounded engineering objective.

The task should establish:

```text
Objective
Scope
Non-goals
Requirements
Constraints
Acceptance Criteria
Dependencies
Validation Requirements
```

---

# 9. Definition Gate

The task should not proceed to implementation until the agent can reasonably answer:

### What?

What are we changing?

### Why?

Why is it needed?

### What not?

What is outside scope?

### Success?

How will we know it works?

### Constraints?

What must remain true?

### Authority?

Who/what permits the change?

### Risk?

What could go wrong?

If these cannot be established and the uncertainty materially affects correctness, the agent should investigate or ask.

---

# 10. Task Creation

A meaningful request becomes a persistent task.

Example:

```text id="c4h0h8"
TASK-042 — Add Search Filtering

Status:
DEFINED

Mode:
FEATURE

Objective:
Allow users to filter search results by category.

Scope:
- Filter UI
- Search API parameters
- Query filtering
- Tests

Non-goals:
- Search ranking changes
- Search engine migration
```

The task becomes the execution boundary.

---

# 11. Stage 4 — PLAN

## Purpose

Determine how the task should be implemented safely.

The plan should identify:

* affected components
* implementation approach
* dependencies
* expected change surface
* risks
* validation
* rollback where appropriate

---

# 12. Proportional Planning

Planning depth should depend on:

```text
Complexity
Risk
Change Surface
Uncertainty
Irreversibility
```

### Small task

```text
Affected file
Approach
Validation
```

### Medium task

```text
Components
Approach
Dependencies
Tests
Risks
```

### High-risk task

```text
Architecture
Options
Trade-offs
Migration
Rollback
Validation
Approval
```

---

# 13. Stage 5 — AUTHORIZE

## Purpose

Determine whether the planned work may proceed.

Authorization is distinct from planning.

An AI may produce an excellent plan without having authority to execute it.

---

## 13.1 Authorization Levels

### Autonomous

AI may execute.

Typical low-risk work.

### Supervised

AI may execute with appropriate oversight.

Typical moderate-risk work.

### Human Controlled

Human authorization is required.

Typical:

* destructive migrations
* production data changes
* major security changes
* payment changes
* irreversible infrastructure
* major public API changes

---

# 14. Authorization Gate

Before execution, verify:

```text
Scope authorized?
Change boundary clear?
Risk acceptable?
Required decisions resolved?
Required approvals obtained?
```

If not:

> Stop or request clarification/approval.

---

# 15. Stage 6 — EXECUTE

## Purpose

Implement the approved task.

Execution rules:

1. Stay within scope.
2. Follow project rules.
3. Use established patterns.
4. Minimize change surface.
5. Preserve unrelated behaviour.
6. Validate incrementally where appropriate.
7. Record material discoveries.
8. Reassess when assumptions fail.

---

# 16. Execution Loop

Implementation may produce new information.

Therefore:

```text id="7wxv0a"
EXECUTE
   ↓
DISCOVERY
   ↓
Does new information matter?
   │
   ├── NO → Continue
   │
   └── YES
         ↓
      ASSESS
         ↓
   Does scope change?
      /       \
    NO         YES
    │           │
    ↓           ↓
Continue    Re-plan /
            authorize
```

This prevents blind continuation.

---

# 17. Change Boundary Enforcement

During execution, compare actual change against:

* task scope
* expected change surface
* change budget
* project rules
* protected boundaries

If the change exceeds expectations:

```text id="5e8ncr"
Investigate
     ↓
Justified?
   /     \
 YES      NO
  ↓        ↓
Re-plan   Stop
```

---

# 18. Stage 7 — VERIFY

## Purpose

Determine whether the implementation is correct and complete.

Verification has two dimensions:

### Positive verification

Did we implement what was requested?

### Regression verification

Did we preserve what should continue working?

---

# 19. Validation Selection

Validation should be selected based on risk and task type.

Example:

### UI change

* build
* type check
* unit tests
* functional verification

### Database migration

* schema validation
* data integrity
* migration test
* rollback test
* regression

### Authentication change

* unit
* integration
* functional
* security
* regression

### Optimization

* functional tests
* performance baseline
* post-change measurement

---

# 20. Verification Gate

A task is not complete merely because implementation exists.

The agent must establish:

```text
Requirement satisfied?
Acceptance criteria satisfied?
Required validation completed?
Regression risk addressed?
Known limitations disclosed?
```

If not:

```text
COMPLETE
```

must not be declared.

---

# 21. Stage 8 — RECORD

## Purpose

Persist material knowledge generated by the work.

Potential updates:

```text
Task
State
Validation
Decision
Requirement
Feature
Domain
Environment
```

Only relevant artifacts should be updated.

---

# 22. Record Decision Tree

After meaningful work:

```text id="y1h4gj"
Did project state change?
        │
       YES → Update state

Did task state change?
        │
       YES → Update task

Was a material decision made?
        │
       YES → Record decision

Was meaningful validation performed?
        │
       YES → Record validation

Did durable project knowledge change?
        │
       YES → Update appropriate artifact
```

---

# 23. Stage 9 — REPORT

The agent provides a concise result.

Recommended:

```text
Result
Changes
Validation
Known Limitations
Artifacts Updated
Next Action
```

The report should describe facts and evidence.

---

# 24. Stage 10 — COMPLETE

A task reaches `COMPLETED` only when:

```text
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

Formally:

> **DONE = Scope + Implementation + Validation + Disclosure + State**

---

# 25. Failure States

A task may end in:

```text
COMPLETED
PARTIALLY_COMPLETED
BLOCKED
FAILED
CANCELLED
```

### PARTIALLY_COMPLETED

Some intended work is complete but meaningful work remains.

### BLOCKED

Progress cannot safely continue due to dependency, missing information, authorization, environment, or external condition.

### FAILED

The intended implementation could not be achieved.

### CANCELLED

The work is intentionally no longer required.

---

# 26. Failure Recovery

Failure should not automatically create a new task.

First determine whether the failure is:

* implementation defect
* incorrect assumption
* requirement issue
* architecture issue
* environment issue
* external dependency
* insufficient validation
* scope problem

Then return to the appropriate lifecycle stage.

Example:

```text id="l7qg7g"
Validation failure
       ↓
Diagnosis
       ↓
Implementation defect?
   /          \
 YES           NO
 ↓              ↓
EXECUTE      DISCOVER / DEFINE
```

---

# 27. Requirement Change During Execution

Requirements may change while work is underway.

AICF should not silently incorporate the change.

Process:

```text id="qf4j79"
New Requirement
      ↓
Assess
      ↓
Does it change scope?
   /          \
 NO            YES
 │              │
 ↓              ↓
Continue     Re-define
                ↓
             Re-plan
                ↓
            Re-authorize
                ↓
             Execute
```

This preserves traceability.

---

# 28. Decision Discovery During Execution

If implementation reveals that a material decision is required:

```text id="zex6as"
Discover decision
       ↓
Collect evidence
       ↓
Evaluate options
       ↓
Recommend
       ↓
Obtain authority
       ↓
Record decision
       ↓
Update plan
       ↓
Continue
```

The agent must not silently make high-impact architectural choices.

---

# 29. Scope Expansion

Scope expansion can occur legitimately.

Examples:

* required supporting change
* dependency discovered
* compatibility requirement
* necessary security fix

But it must be distinguished from opportunistic improvement.

### Required supporting change

May remain within the task if authorized.

### Unrelated improvement

Should normally become a separate task.

---

# 30. Task Splitting

A task should be split when:

* scope becomes materially larger
* independent outcomes emerge
* risk differs substantially
* different authorization is required
* validation becomes independent
* multiple teams/owners are involved

Example:

```text
TASK-042
Search filtering
      │
      ├── TASK-043 API filtering
      ├── TASK-044 UI filtering
      └── TASK-045 Performance optimization
```

The parent task may track the overall objective.

---

# 31. Task Merging

Tasks may be merged when:

* their objectives are tightly coupled
* separate execution provides no benefit
* validation is inseparable
* splitting creates unnecessary overhead

The framework should favour useful boundaries rather than artificial decomposition.

---

# 32. Context Loss Recovery

If the agent loses context during execution:

```text
STOP
 ↓
Read rules
 ↓
Read project
 ↓
Read state
 ↓
Read task
 ↓
Read relevant context
 ↓
Inspect current implementation
 ↓
Reconstruct position
 ↓
Continue
```

The agent should never continue based on unreliable memory.

---

# 33. Session Boundary

A task may span multiple AI sessions.

The task lifecycle does not reset when the conversation ends.

For example:

```text
Session 1
DISCOVER → DEFINE → PLAN
       ↓
     state

Session 2
RECOVER → EXECUTE
       ↓
     state

Session 3
RECOVER → VERIFY → RECORD → COMPLETE
```

The repository maintains continuity.

---

# 34. Tool Change

A task may also move between AI tools.

Example:

```text
Claude
   ↓
implementation
   ↓
Codex
   ↓
validation
   ↓
Gemini
   ↓
analysis
```

The AICF state remains unchanged.

The new agent recovers from the repository.

Tool identity is not part of project truth.

---

# 35. Lifecycle Invariants

Regardless of task type, the following invariants must hold:

### I1 — No implementation without sufficient understanding

### I2 — No silent scope expansion

### I3 — No unsupported assumptions presented as facts

### I4 — No unauthorized high-risk change

### I5 — No false validation claim

### I6 — No completion without required validation

### I7 — No material decision without persistent rationale

### I8 — No session dependency for essential state

### I9 — No unnecessary artifact creation

### I10 — No concealment of failure

These invariants form the safety backbone of the runtime model.

---

# 36. Runtime State Machine

Conceptually:

```text id="1n3gzu"
                    ┌──────────────┐
                    │    REQUEST   │
                    └──────┬───────┘
                           ↓
                       ORIENTED
                           ↓
                       DISCOVERING
                           ↓
                        DEFINED
                           ↓
                        PLANNED
                           ↓
                      AUTHORIZED
                           ↓
                       EXECUTING
                           ↓
                      VERIFYING
                      /       \
                 PASS          FAIL
                  ↓              ↓
               RECORD       DIAGNOSE
                  ↓              │
               REPORT           └──→ REPLAN
                  ↓
              COMPLETED
```

At almost every stage:

```text
UNKNOWN / CONFLICT / AUTHORIZATION ISSUE
                ↓
              PAUSE
                ↓
       INVESTIGATE / ESCALATE
```

---

# 37. Runtime Model by Project Mode

The lifecycle remains constant, but emphasis changes.

| Mode         | Strongest Stages                  |
| ------------ | --------------------------------- |
| Greenfield   | Discover, Define, Plan            |
| Existing     | Orient, Discover, Verify          |
| Feature      | Define, Execute, Verify           |
| Bugfix       | Discover, Diagnose, Verify        |
| Refactor     | Discover, Plan, Regression Verify |
| Migration    | Discover, Plan, Verify, Recovery  |
| Integration  | Discover, Define, Verify          |
| Optimization | Measure, Diagnose, Verify         |
| Maintenance  | Define, Execute, Verify           |

This demonstrates the purpose of Project Modes.

---

# 38. Runtime Model

The complete AICF runtime can therefore be represented as:

```text id="2uh9qm"
USER INTENT
     ↓
┌─────────────────────┐
│       ORIENT        │
│ Context + State     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│      DISCOVER       │
│ Evidence + Unknowns │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       DEFINE        │
│ Scope + Acceptance  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│        PLAN         │
│ Approach + Risk     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│      AUTHORIZE      │
│ Authority + Bounds  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       EXECUTE       │
│ Controlled Change   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       VERIFY        │
│ Evidence + Quality  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       RECORD        │
│ State + Knowledge   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       REPORT        │
│ Result + Limitations│
└──────────┬──────────┘
           ↓
        COMPLETE
```

---

# 39. Core Principle

> **AICF turns an AI coding request into a controlled engineering lifecycle: understand the intent, establish the truth, bound the work, authorize the change, execute deliberately, prove the result, and leave the project recoverable.**
