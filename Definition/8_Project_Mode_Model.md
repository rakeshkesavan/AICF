# 8. Project Mode Model

## 8.1 Purpose

AICF must support different types of engineering work without creating separate frameworks for each scenario.

A greenfield project, a bug fix, a migration, and an optimization task have different risks, discovery needs, validation requirements, and execution patterns. However, they should all operate under the same AICF principles, behaviour contract, context model, decision model, and change/validation model.

Project modes therefore define **how AICF adapts its operating emphasis to the nature of the work**.

The fundamental principle is:

> **One framework. Different modes. Same engineering discipline.**

Project mode is not a separate lifecycle. It is a configuration of the existing AICF lifecycle:

**DISCOVER → DEFINE → PLAN → EXECUTE → VERIFY → RECORD**

---

## 8.2 Project Mode Selection

Before meaningful work begins, AICF should identify the primary mode of the work.

The mode may be:

* explicitly provided by the user
* inferred from the task
* determined during discovery

If the mode is ambiguous and the difference materially affects implementation or risk, the AI should clarify rather than assume.

A project may also transition between modes.

For example:

**GREENFIELD → FEATURE → BUGFIX → REFACTOR → MAINTENANCE**

A migration may contain feature work, bug fixes, and refactoring as subordinate activities.

Therefore, project mode describes the **dominant engineering situation**, not an exclusive classification.

---

# 8.3 Mode: GREENFIELD

## Purpose

Create a new software system where little or no existing implementation constrains the design.

## Primary emphasis

**DEFINE → PLAN → ARCHITECT → EXECUTE → VERIFY**

## Discovery focus

* Product purpose
* Requirements
* Users and workflows
* Domain concepts
* Technical constraints
* Integration requirements
* Non-functional requirements
* Security requirements
* Expected scale
* Deployment environment
* Architectural alternatives

## Planning characteristics

Greenfield work requires stronger upfront definition because architectural decisions can influence the entire project.

Planning should establish:

* system boundaries
* major components
* technology choices
* data model
* API boundaries
* integration boundaries
* deployment model
* testing strategy
* security model
* architectural conventions

However, AICF should avoid attempting to design the entire system before useful implementation begins.

Architecture should evolve through validated increments.

## Execution characteristics

Prefer:

* foundation before dependent features
* vertical slices where practical
* early validation of architectural assumptions
* reusable conventions
* explicit architectural decisions

Avoid:

* speculative abstractions
* premature optimization
* building unused infrastructure
* designing every future feature

## Validation emphasis

Strong emphasis on:

* architecture
* integration
* foundational behaviour
* security
* performance assumptions
* developer experience
* deployment viability

## Primary risk

**Architectural decisions made with insufficient evidence.**

---

# 8.4 Mode: EXISTING SYSTEM

## Purpose

Modify or extend an existing system whose current behaviour, architecture, and conventions already provide significant constraints.

## Primary emphasis

**DISCOVER → INSPECT → DEFINE → PLAN → CHANGE → REGRESSION VERIFY**

## Discovery focus

* Existing architecture
* Current implementation
* Existing patterns
* Dependencies
* Tests
* Runtime behaviour
* Known constraints
* Existing integrations
* Technical debt
* Historical decisions

The existing system must be treated as an important source of truth.

The AI should inspect before introducing new patterns.

## Planning characteristics

Planning should explicitly identify:

* affected components
* existing behaviour to preserve
* dependencies
* change surface
* regression risks
* compatibility concerns

## Execution characteristics

Prefer:

* existing patterns
* minimal change
* localized modifications
* backward compatibility where required
* incremental implementation

Avoid:

* unnecessary rewrites
* introducing competing patterns
* broad cleanup unrelated to the objective
* assuming undocumented behaviour

## Validation emphasis

Strong emphasis on:

* regression
* existing tests
* integration behaviour
* backward compatibility
* architecture compliance

## Primary risk

**Breaking existing behaviour while solving the new requirement.**

---

# 8.5 Mode: MIGRATION

## Purpose

Move a system, component, dependency, data model, platform, or architecture from one state to another.

Examples include:

* framework migration
* database migration
* API migration
* infrastructure migration
* dependency migration
* architectural migration
* legacy replacement

## Primary emphasis

**DISCOVER → PLAN → INCREMENTAL EXECUTE → VERIFY → TRANSITION**

## Discovery focus

Establish:

* current state
* target state
* compatibility requirements
* migration dependencies
* data implications
* operational constraints
* rollback possibilities
* coexistence requirements
* cutover strategy

## Planning characteristics

Migration planning must define:

* source state
* target state
* migration stages
* compatibility strategy
* sequencing
* validation checkpoints
* rollback/recovery
* decommissioning criteria

Where practical, migrations should favour **incremental transition over big-bang replacement**.

## Execution characteristics

Prefer:

* reversible steps
* coexistence where practical
* small migration increments
* checkpoints
* validation after each meaningful stage
* explicit cutover criteria

## Validation emphasis

Strong emphasis on:

* data integrity
* compatibility
* functional equivalence
* regression
* performance
* operational behaviour
* rollback readiness

## Primary risk

**Irreversible change before the target state is proven.**

---

# 8.6 Mode: FEATURE

## Purpose

Add new functionality to an existing or evolving system.

## Primary emphasis

**DEFINE → PLAN → EXECUTE → VERIFY**

## Discovery focus

* Existing feature context
* Related workflows
* Existing architecture
* Requirements
* Dependencies
* User behaviour
* Existing patterns

## Planning characteristics

Define:

* feature objective
* scope
* non-goals
* acceptance criteria
* affected components
* dependencies
* validation requirements

## Execution characteristics

Prefer:

* vertical implementation
* existing patterns
* incremental delivery
* isolated changes
* feature-level validation

## Validation emphasis

* acceptance criteria
* functional behaviour
* integration
* regression
* UX where applicable

## Primary risk

**Feature works in isolation but violates existing system behaviour or architecture.**

---

# 8.7 Mode: BUGFIX

## Purpose

Correct behaviour that does not match the intended or expected behaviour.

## Primary emphasis

**DISCOVER → DIAGNOSE → DEFINE → FIX → VERIFY**

## Discovery focus

The AI must first establish:

* observed behaviour
* expected behaviour
* reproduction conditions
* affected environment
* relevant implementation
* logs/errors
* related tests
* recent changes where relevant

## Planning characteristics

The plan should identify:

* probable root cause
* evidence supporting the diagnosis
* affected area
* intended correction
* regression risks
* tests required

A bugfix should not begin with:

> “Change the code until the error disappears.”

It should begin with:

> **“Establish why the behaviour occurs.”**

## Execution characteristics

Prefer:

* root-cause correction
* minimal change
* regression test
* preservation of unrelated behaviour

Avoid:

* symptom-only fixes
* speculative rewrites
* unrelated cleanup

## Validation emphasis

Strong emphasis on:

* reproduction
* corrective validation
* regression testing
* edge cases

## Primary risk

**Fixing the symptom while leaving the underlying cause unresolved.**

---

# 8.8 Mode: REFACTOR

## Purpose

Improve internal structure without intentionally changing externally observable behaviour.

Examples:

* restructuring modules
* simplifying abstractions
* removing duplication
* improving maintainability
* reorganizing code
* improving architecture without changing requirements

## Primary emphasis

**DISCOVER → BASELINE → PLAN → REFACTOR → REGRESSION VERIFY**

## Discovery focus

Establish:

* current behaviour
* existing tests
* architectural constraints
* dependencies
* coupling
* code smells
* intended target structure

## Planning characteristics

A refactor should define:

* current structure
* target structure
* behaviour that must remain unchanged
* migration sequence
* validation strategy

## Execution characteristics

Prefer:

* small structural changes
* continuous validation
* preservation of behaviour
* one conceptual transformation at a time

Avoid:

* mixing feature development with refactoring
* changing behaviour unintentionally
* broad rewrites without justification

## Validation emphasis

Regression validation is primary.

Where applicable:

* unit tests
* integration tests
* API compatibility
* performance comparison
* architecture checks

## Primary risk

**Structural improvement accidentally becoming behavioural change.**

---

# 8.9 Mode: INTEGRATION

## Purpose

Connect the system with an external or internal system, service, API, platform, or dependency.

## Primary emphasis

**DISCOVER → CONTRACT DEFINE → PLAN → IMPLEMENT → VERIFY**

## Discovery focus

* External system capabilities
* API documentation
* Authentication
* Data contracts
* Error behaviour
* Rate limits
* Reliability characteristics
* Versioning
* Environment differences
* Existing integration patterns

External documentation should be treated as technical evidence, not as permission to override project requirements or decisions.

## Planning characteristics

Define:

* integration boundary
* contracts
* request/response behaviour
* failure handling
* retries/timeouts
* authentication
* observability
* compatibility
* testing strategy

## Execution characteristics

Prefer:

* existing project integration patterns
* explicit adapters
* isolated integration boundaries
* defensive error handling
* testable contracts

## Validation emphasis

* contract validation
* integration tests
* failure scenarios
* authentication
* timeout/retry behaviour
* compatibility

## Primary risk

**Assuming external behaviour that has not been verified.**

---

# 8.10 Mode: OPTIMIZATION

## Purpose

Improve performance, efficiency, scalability, cost, reliability, or resource utilization.

## Primary emphasis

**MEASURE → DIAGNOSE → PLAN → CHANGE → MEASURE**

Optimization must be evidence-driven.

The AI should not treat:

> “This looks slow.”

as sufficient evidence for a technical optimization.

## Discovery focus

Establish:

* current performance
* bottleneck
* workload
* relevant metrics
* resource usage
* system constraints
* performance target

## Planning characteristics

Define:

* baseline
* hypothesis
* proposed change
* expected impact
* measurement method
* regression risks

## Execution characteristics

Prefer:

* measurable changes
* isolated experiments
* reversible modifications
* controlled comparison

## Validation emphasis

Performance validation is mandatory where optimization is the stated objective.

Compare:

**BEFORE → CHANGE → AFTER**

Functional correctness must also remain intact.

## Primary risk

**Optimizing the wrong bottleneck or degrading another important property.**

---

# 8.11 Mode: MAINTENANCE

## Purpose

Perform routine engineering work required to keep a system healthy and sustainable.

Examples:

* dependency updates
* configuration changes
* small fixes
* documentation updates
* test maintenance
* minor compatibility changes
* technical debt reduction
* operational improvements

## Primary emphasis

**DISCOVER → BOUND → EXECUTE → VERIFY → RECORD**

Maintenance work should remain intentionally lightweight.

## Discovery focus

Determine:

* why the change is needed
* affected area
* compatibility concerns
* current state
* required validation

## Planning characteristics

Planning should be proportional to risk.

A small dependency patch does not require the same planning depth as a database migration.

## Execution characteristics

Prefer:

* small changes
* minimal scope
* established patterns
* routine validation

## Validation emphasis

Validation should match the actual risk and impact.

## Primary risk

**Treating apparently small maintenance work as risk-free.**

---

# 8.12 Mode Composition

Project modes may be composed within larger work.

For example:

**Migration**

* discovery
* migration planning
* feature implementation
* bug fixes
* refactoring
* integration
* optimization

Therefore, AICF should distinguish between:

**Primary Mode**
The dominant nature of the current work.

**Task Mode**
The specific mode of an individual task.

Example:

> Primary Mode: MIGRATION
> Current Task Mode: BUGFIX

This allows the framework to maintain the larger project context while adapting the immediate operating behaviour.

---

# 8.13 Mode Transitions

A project mode may change when new evidence changes the nature of the work.

Examples:

**FEATURE → BUGFIX**

A feature implementation reveals an existing defect that must be diagnosed separately.

**REFACTOR → MIGRATION**

A structural change becomes a broader architectural transition.

**OPTIMIZATION → REFACTOR**

Investigation reveals that the bottleneck is caused by structural design.

**EXISTING → MIGRATION**

A planned modification becomes a system-wide replacement.

Mode transitions should be recorded when they materially affect:

* scope
* risk
* planning
* autonomy
* validation
* project state

---

# 8.14 Mode Selection Matrix

| Mode         | Primary Question                            | Strongest Emphasis           | Main Risk                |
| ------------ | ------------------------------------------- | ---------------------------- | ------------------------ |
| GREENFIELD   | What should we build?                       | Architecture & foundations   | Wrong early decisions    |
| EXISTING     | What already exists?                        | Inspection & preservation    | Regression               |
| MIGRATION    | How do we move safely?                      | Incremental transition       | Irreversible change      |
| FEATURE      | What capability should be added?            | Requirements & integration   | Scope/architecture drift |
| BUGFIX       | Why is behaviour wrong?                     | Diagnosis & evidence         | Symptom fixing           |
| REFACTOR     | How can structure improve safely?           | Regression preservation      | Behaviour change         |
| INTEGRATION  | How do systems interact?                    | Contracts & failure handling | Unverified assumptions   |
| OPTIMIZATION | What should become better, and by how much? | Measurement                  | Wrong bottleneck         |
| MAINTENANCE  | What must be kept healthy?                  | Proportionality              | Underestimating risk     |

---

# 8.15 Universal Operating Rule

Regardless of mode, the following remain unchanged:

1. Understand before changing.
2. Inspect before assuming.
3. Establish the relevant truth.
4. Define a bounded objective.
5. Plan according to risk.
6. Respect change boundaries.
7. Prefer existing patterns where appropriate.
8. Make the smallest sufficient change.
9. Validate against the intended outcome.
10. Validate against important existing behaviour.
11. Record material knowledge.
12. Leave the project recoverable.

Project mode changes **emphasis**, not **principles**.

---

# 8.16 Mode as Configuration

AICF project mode should therefore be represented as configuration rather than as a separate process.

Conceptually:

```text
AICF
│
├── Principles
├── AI Behaviour Contract
├── Operating Model
├── Context Model
├── Truth & Decision Model
├── Change & Validation Model
│
└── Project Mode
    ├── Greenfield
    ├── Existing
    ├── Migration
    ├── Feature
    ├── Bugfix
    ├── Refactor
    ├── Integration
    ├── Optimization
    └── Maintenance
```

This preserves a single engineering system while allowing the AI agent to adapt its behaviour to the actual situation.

---

## 8.17 Core Principle

> **AICF does not create a different framework for every type of software work. It provides one engineering system whose emphasis adapts to the work being performed.**

The objective is not to classify work perfectly.

The objective is to ensure that the AI applies the **right engineering discipline at the right intensity**.
