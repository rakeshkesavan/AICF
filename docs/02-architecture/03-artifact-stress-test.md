
# Artifact Stress Test

We'll test the foundational artifacts against four very different engineering situations:

1. Greenfield project
2. Existing-system bug fix
3. Large migration
4. Long-running feature development across AI sessions

The test is not whether every scenario looks identical. The test is whether **the same AICF information model remains valid**.

---

# 1. Scenario A — Greenfield

### Request

> Build a SaaS application for managing equipment rentals. Users can browse equipment, reserve items, and receive email confirmations.

There is no existing codebase.

### Initial artifacts

```text
.aicf/
├── rules.md
├── project.md
└── state.md
```

The AI discovers the project requirements and architecture.

Eventually:

```text
.aicf/
├── rules.md
├── project.md
├── state.md
├── requirements/
├── decisions/
├── domains/
├── features/
└── tasks/
```

### What happens?

`project.md` establishes:

* product purpose
* stack
* architecture
* major components

`rules.md` establishes:

* engineering conventions
* testing requirements
* architecture constraints

`state.md` establishes:

> Architecture foundation in progress.

A decision record might capture:

> PostgreSQL selected for transactional reservation data.

A task might be:

> Implement equipment catalog.

A feature artifact might describe:

> Equipment browsing and reservation workflow.

### Does the model hold?

**Yes.**

The key observation is that greenfield work doesn't require a fundamentally different artifact system.

It simply produces more architecture and decision knowledge early.

---

# 2. Scenario B — Existing-System Bug Fix

### Request

> Users occasionally get logged out while submitting a form. Fix it without changing the authentication architecture.

The agent starts with:

```text
rules.md
project.md
state.md
```

Then discovers:

```text
domain: identity
feature: authentication
task: logout bug
source
tests
logs
```

The task becomes:

```text
Objective
Fix unexpected logout during form submission.

Non-goals
Do not change authentication architecture.

Acceptance
Form submission must not invalidate the session.
Existing login/logout behaviour must remain unchanged.
```

The agent investigates.

Suppose it discovers that a token refresh race condition causes the problem.

It fixes it and adds a regression test.

### What happens to the artifacts?

`task.md` records the bounded work.

`validation/` records the regression evidence.

`state.md` records that the issue is resolved.

Possibly a decision isn't needed at all.

### This is important.

AICF does **not require a decision record for every task**.

That keeps the framework lightweight.

---

# 3. Scenario C — Large Migration

### Request

> Migrate the application from Framework A to Framework B.

This is where we really pressure-test the architecture.

The project may have:

```text
project.md
state.md
rules.md
environment.md

domains/
features/
requirements/

decisions/
tasks/
validation/
```

The migration gets its own task structure.

For example:

```text
TASK-100 migration strategy
TASK-101 compatibility layer
TASK-102 module migration
TASK-103 API migration
TASK-104 test migration
TASK-105 cutover
```

A major decision might be:

> Use a strangler migration rather than a big-bang rewrite.

Another:

> Maintain Framework A and Framework B simultaneously during transition.

Each decision is persistent.

`state.md` might say:

```text
Migration: 42% complete

Current state:
- Identity migrated
- Catalog migrated
- Billing still on legacy framework

Known issue:
- Legacy billing adapter has performance degradation

Next action:
- Resolve billing adapter before next migration stage
```

### Does the architecture break?

No.

In fact, migration exposes why **state.md + tasks + decisions + validation** are important.

---

# 4. Scenario D — Long-Running Feature

This is the most important scenario for AI-assisted development.

Suppose:

> Build a complete analytics dashboard.

This work takes six weeks.

During that period:

* 15 AI sessions occur
* different agents are used
* requirements change
* bugs appear
* architecture decisions are made
* developers take over manually
* work pauses for several days

This is where AICF should shine.

---

## Session 1

Agent reads:

```text
rules
project
state
task
```

It works on dashboard foundation.

At the end:

```text
state.md
```

says:

```text
Dashboard foundation completed.

Current work:
Analytics query layer.

Open decision:
Caching strategy.

Known issue:
Large date ranges produce slow queries.
```

---

## Session 4

A different AI agent starts.

It does not need the previous conversation.

It reads:

```text
rules
project
state
task
```

Then discovers:

> Caching strategy is unresolved.

It investigates.

The agent proposes Redis.

Human approves.

A decision record is created.

Now the decision becomes persistent knowledge.

---

## Session 9

Requirement changes:

> Dashboard must now support export to CSV and PDF.

Instead of silently modifying the existing task, AICF forces a question:

Is this:

**Supporting change?**

or

**New scope?**

Suppose it's new scope.

A new task is created.

The original task remains traceable.

---

## Session 12

A bug appears in the analytics query layer.

The agent switches:

```text
FEATURE → BUGFIX
```

The framework doesn't change.

The agent diagnoses the issue, fixes it, validates regression, and updates state.

---

## Session 15

The original AI conversation is gone.

A new agent arrives.

It reads:

```text
rules.md
project.md
state.md
active tasks
relevant decisions
```

And understands:

* what's already completed
* what's currently active
* what decisions were made
* what remains unresolved
* what the next action is

### This is the real success criterion.

Not:

> "Can AI remember a conversation?"

But:

> **"Can the repository explain the engineering state?"**

---

# 5. Stress-Test Results

| Capability      | Greenfield |   Bugfix | Migration | Long-running |
| --------------- | ---------: | -------: | --------: | -----------: |
| Rules           |          ✓ |        ✓ |         ✓ |            ✓ |
| Project         |          ✓ |        ✓ |         ✓ |            ✓ |
| State           |          ✓ |        ✓ |        ✓✓ |           ✓✓ |
| Task            |          ✓ |       ✓✓ |        ✓✓ |           ✓✓ |
| Decision        |          ✓ | Optional |        ✓✓ |           ✓✓ |
| Domain          |     Useful |   Useful |    Useful |            ✓ |
| Feature         |          ✓ | Optional |         ✓ |           ✓✓ |
| Requirement     |          ✓ |        ✓ |        ✓✓ |           ✓✓ |
| Validation      |          ✓ |       ✓✓ |        ✓✓ |           ✓✓ |
| Environment     |     Useful |   Useful |        ✓✓ |            ✓ |
| Mode adaptation |          ✓ |        ✓ |         ✓ |            ✓ |

The architecture holds.

---

# 6. One Important Discovery

The stress test reveals that we need a distinction between:

### Artifact

Persistent knowledge or state.

and

### Record

An instance of an artifact.

For example:

```text
tasks/
    TASK-001.md
    TASK-002.md
```

`task` is the **artifact type**.

`TASK-001` is a **task record**.

Likewise:

```text
decisions/
    DEC-001.md
```

This distinction will be useful when we define schemas.

---

# 7. Another Discovery — Not Everything Needs Persistence

This is equally important.

Consider:

> "Should this function use a `for` loop or `map()`?"

That may be an implementation decision.

It does **not** necessarily deserve:

```text
DEC-247.md
```

AICF should distinguish:

### Temporary implementation choice

Conversation/task context.

### Material engineering decision

Persistent decision record.

This prevents artifact explosion.

---

# 8. Another Discovery — State is the Most Critical Artifact

If I rank the five foundational artifacts for **session recovery**, I'd put them:

```text
1. state.md
2. task.md
3. project.md
4. rules.md
5. decision records
```

But for **safe execution**, the priority changes:

```text
1. rules.md
2. task.md
3. requirements
4. project.md
5. relevant decisions
```

This tells us something important:

> **There isn't one universal context order.**

The retrieval sequence should depend on the agent's purpose.

We should therefore avoid hard-coding a rigid:

> "Always read files A → B → C → D."

Instead, Phase 2 should define a **default startup sequence plus context escalation rules**.

---

# 9. Proposed Context Retrieval Model

Instead of:

```text
Always load:
A → B → C → D → E → F
```

we define:

```text
START
  ↓
Identify Mode + Objective
  ↓
Load Governance
  ↓
Load Project State
  ↓
Load Task
  ↓
Determine Context Needs
  ↓
Load Relevant Knowledge
  ↓
Inspect Source
  ↓
Assess Sufficiency
```

This is more adaptive.

For example, a bugfix may need:

```text
state → task → bug context → logs → source → tests
```

A greenfield task may need:

```text
project → requirements → architecture decisions → source
```

A migration may need:

```text
project → state → migration task → decisions → environment → source
```

Same framework. Different context path.

---

# 10. Final Stress-Test Verdict

### Foundational artifact architecture

**PASS**

### Five foundational artifacts

**PASS**

### Multiple project modes

**PASS**

### Long-session continuity

**PASS conceptually**

### New-agent recovery

**PASS conceptually**

### Tool independence

**PASS**

### Risk of documentation explosion

**Controlled**, provided we maintain the persistence rules.

### Main design requirement going forward

**Keep context retrieval adaptive rather than mechanically sequential.**

---

# 11. What This Means for the Next Step

I think we have enough evidence to start defining the **actual Markdown schemas**.

But I recommend we do it in this order:

### Phase 2.3

**Define the canonical schema for each artifact**

First:

1. `rules.md`
2. `project.md`
3. `state.md`
4. `task.md`
5. `decision.md`

Then:

6. `requirement.md`
7. `domain.md`
8. `feature.md`
9. `validation.md`
10. `environment.md`

Then:

### Phase 2.4

Define:

* IDs
* naming conventions
* cross-references
* statuses
* lifecycle transitions
* metadata
* mandatory vs optional fields

Then:

### Phase 2.5

Build the actual **AICF starter repository structure**.

That gives us a clean progression:

> **Framework → Architecture → Artifact Specification → Schema → Starter Repository**

And only after that should we start thinking about **AI-tool adapters** or the benchmark project.
