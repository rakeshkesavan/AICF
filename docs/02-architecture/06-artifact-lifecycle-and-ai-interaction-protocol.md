# AICF Artifact Lifecycle & AI Interaction Protocol

## 1. Purpose

This protocol defines when an AI agent should:

* read an artifact
* create an artifact
* update an artifact
* validate an artifact
* challenge an artifact
* avoid touching an artifact

The objective is to prevent both extremes:

**Too little persistence**

where important knowledge remains trapped in conversation.

**Too much persistence**

where every interaction creates documentation.

---

# 2. Fundamental Rule

> **The AI should read context before acting and persist knowledge when it has durable engineering value.**

The AI is not expected to maintain every artifact continuously.

Artifact interaction should be **need-driven**.

---

# 3. Artifact Interaction Types

Every interaction with an AICF artifact falls into one of six categories:

```text
READ
CREATE
UPDATE
VALIDATE
CHALLENGE
DEPRECATE
```

---

# 4. READ

The AI should read an artifact when its information is relevant to the current task.

Examples:

* `rules.md` → before meaningful engineering work
* `project.md` → when project context is needed
* `state.md` → when determining current project status
* `task.md` → before executing a bounded task
* `decision.md` → when a relevant architectural choice exists
* `requirement.md` → when determining intended behaviour
* `feature.md` → when working within that capability
* `domain.md` → when domain rules matter
* `environment.md` → when environment behaviour matters
* `validation.md` → when previous validation evidence matters

---

# 5. CREATE

The AI should create an artifact when:

1. the information has persistent value
2. an appropriate artifact type exists
3. no existing artifact already owns the information
4. creation improves future engineering work

Examples:

### Create a requirement

When an approved new requirement needs persistent representation.

### Create a task

When meaningful bounded engineering work begins.

### Create a decision

When a material engineering decision is accepted.

### Create validation

When meaningful validation needs persistent evidence.

### Create a domain

When a stable contextual boundary emerges.

### Create a feature

When a capability needs persistent contextual representation.

---

# 6. UPDATE

The AI should update an artifact when its authoritative information changes.

Examples:

```text
Requirement changed
→ Update requirement

Architecture changed
→ Update project/decision as appropriate

Project direction changed
→ Update state

Task progress changed
→ Update task

Decision superseded
→ Update decision status

Validation completed
→ Create/update validation

Environment changed
→ Update environment
```

---

# 7. UPDATE MUST BE PURPOSEFUL

The AI should not update artifacts merely because it performed an action.

For example:

Running:

```text
npm test
```

does not automatically require a state update.

But discovering:

> "The integration test suite fails because the QA environment uses an outdated API version."

may require:

* task update
* validation record
* known issue in state
* possibly environment update

The materiality of the discovery determines persistence.

---

# 8. CHALLENGE

An AI agent should challenge an artifact when evidence suggests it is:

* incorrect
* stale
* contradictory
* incomplete in a way that affects correctness
* inconsistent with implementation
* inconsistent with another authoritative artifact

The AI should not silently overwrite important knowledge.

Instead:

```text
Detect contradiction
      ↓
Identify sources
      ↓
Assess authority
      ↓
Assess freshness
      ↓
Determine impact
      ↓
Resolve or escalate
      ↓
Update artifact
```

---

# 9. DEPRECATE

An artifact should be deprecated when its knowledge is no longer valid but historical traceability remains useful.

Examples:

* obsolete architecture decision
* retired feature
* replaced requirement
* obsolete migration plan

Historical artifacts should generally remain identifiable rather than being silently deleted.

---

# 10. Artifact Ownership Rules

| Artifact    | AI May Create |            AI May Update |    AI May Decide |
| ----------- | ------------: | -----------------------: | ---------------: |
| Rules       |       Propose |           With authority |               No |
| Project     |           Yes |        Yes, when factual |               No |
| State       |           Yes |                      Yes |               No |
| Environment |           Yes |        Yes, when factual |               No |
| Domain      |           Yes |                      Yes |               No |
| Feature     |           Yes |                      Yes |               No |
| Requirement |       Propose |            If authorized |               No |
| Decision    |       Propose | Record accepted decision |               No |
| Task        |           Yes |                      Yes | Within authority |
| Validation  |           Yes |                      Yes |               No |

The distinction is important:

> **Creating or updating an artifact does not automatically grant decision authority.**

---

# 11. Agent Startup Protocol

When beginning meaningful work, the AI should perform:

```text
1. Identify objective
2. Identify project/task mode
3. Load applicable rules
4. Recover current state
5. Identify or create task
6. Determine required context
7. Load relevant knowledge
8. Inspect source
9. Assess uncertainty
10. Determine authority
11. Plan
12. Execute
13. Validate
14. Record
```

---

# 12. Context Escalation

The AI should progressively retrieve context.

```text
                    START
                      │
                      ↓
                   RULES
                      │
                      ↓
                   STATE
                      │
                      ↓
                    TASK
                      │
                      ↓
             Is context sufficient?
                 /           \
               YES            NO
                │              │
                ↓              ↓
              PLAN       Load relevant
                           context
                               │
                               ↓
                           Reassess
```

The agent should not load every AICF artifact by default.

---

# 13. Context Sufficiency Test

Before planning or executing, the AI should be able to answer:

### Objective

What are we trying to achieve?

### Scope

What is included and excluded?

### Truth

What do we know?

### Uncertainty

What remains unknown?

### Constraints

What must not be violated?

### Authority

What am I allowed to change?

### Validation

How will we know it worked?

If one of these is materially unknown, the AI should investigate or ask before proceeding.

---

# 14. Artifact Update During Execution

The agent should update artifacts when material discoveries occur.

Example:

```text
Implementation
     │
     ├── Discovery
     │      ↓
     │   Material?
     │      ↓
     │    Update
     │
     ├── Scope change
     │      ↓
     │   Reassess task
     │
     ├── Decision required
     │      ↓
     │   Propose / escalate
     │
     └── Validation
            ↓
        Record evidence
```

This allows the documentation system to evolve alongside engineering work without requiring continuous manual maintenance.

---

# 15. Completion Protocol

Before declaring a meaningful task complete, the AI should:

### 1. Confirm scope

Was the intended scope satisfied?

### 2. Confirm implementation

Was the required change actually made?

### 3. Confirm validation

Were required validations performed?

### 4. Confirm limitations

Are there known failures or untested areas?

### 5. Update task

Record outcome.

### 6. Update validation

Record evidence.

### 7. Update state

Reflect material project-state changes.

### 8. Record decisions

Persist any material new decisions.

---

# 16. Session Handoff Protocol

When a meaningful task is paused or a session ends, the AI should leave enough state for another agent to continue.

The persistent state should capture:

```text
Current objective
Completed work
Current work
Unresolved issues
Open unknowns
Decisions made
Validation status
Known limitations
Next action
```

The objective is:

> **The next agent should continue from repository state, not conversation memory.**

---

# 17. New Session Recovery

A new agent should begin with:

```text
RULES
  ↓
PROJECT
  ↓
STATE
  ↓
ACTIVE TASK
  ↓
RELEVANT CONTEXT
  ↓
SOURCE
  ↓
VALIDATE UNDERSTANDING
```

It should explicitly reassess whether the persistent state is sufficient and current.

---

# 18. Artifact Conflict Protocol

If artifacts disagree:

```text
CONFLICT
   ↓
Identify conflicting claims
   ↓
Identify sources
   ↓
Assess authority
   ↓
Assess freshness
   ↓
Inspect implementation/evidence
   ↓
Determine intended vs actual state
   ↓
Resolve
   ↓
Record material resolution
```

The AI must not silently choose whichever artifact it happened to read first.

---

# 19. Artifact Staleness

An artifact may become stale because:

* implementation changed
* requirements changed
* architecture changed
* environment changed
* decision was superseded
* project direction changed

The AI should flag material staleness when discovered.

It should not blindly trust documentation simply because it exists.

---

# 20. Artifact Minimality Test

Before creating or significantly expanding an artifact:

> **Will this information reduce future uncertainty, repeated discovery, risk, or context dependency?**

If not, keep it temporary.

---

# 21. Agent Protocol Summary

The AICF agent operates according to:

```text
READ before acting
CREATE when durable knowledge emerges
UPDATE when material truth changes
VALIDATE when evidence is required
CHALLENGE when sources conflict
DEPRECATE when knowledge becomes obsolete
```

And:

> **Never persist information merely because the AI generated it. Persist it because the project needs to remember it.**

---

# 22. Operational Loop

The complete AICF operational loop becomes:

```text
          ┌──────────────────────┐
          │   PERSISTENT STATE   │
          └──────────┬───────────┘
                     ↓
                  RETRIEVE
                     ↓
                  UNDERSTAND
                     ↓
                  PLAN
                     ↓
                  EXECUTE
                     ↓
                  VALIDATE
                     ↓
                   RECORD
                     │
                     └──────────────→ UPDATED STATE
```

The loop continues across:

* tasks
* sessions
* AI agents
* tools
* developers
* project phases

---

# 23. Core Principle

> **AICF artifacts are the persistent memory of engineering work, while AI sessions are temporary working environments.**

The agent's responsibility is therefore not to remember everything.

Its responsibility is to ensure that **important knowledge survives the session**.
