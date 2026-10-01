# AICF Phase 1 Bootstrap & Context Population

This directory contains the Phase 1 bootstrap implementation, extended for **AICF-004B** (`docs/03-bootstrap/AICF-004B-Agent-Driven-Repository-Characterization-Specification-v0.1.0.md`). The original Phase 1 behavior remains available.

## Workflow

```text
init  ──>  analyze  ──>  select  ──>  populate (apply)  ──>  govern
```

## Canonical Phase 1 Template

```text
.aicf/
├── README.md
├── rules.md
├── project.md
├── environment.md
└── state.md
```

## CLI Usage

### 1. Initialize AICF Template
Creates the `.aicf/` directory with the 5 canonical files only if `.aicf/` does not already exist:
```bash
python tooling/bootstrap/bootstrap_phase1.py init [--path <repo-path>]
```

### 2. Analyze Repository
Passively inspects the repository and proposes structured content for selectable artifacts:
```bash
python tooling/bootstrap/bootstrap_phase1.py analyze [--path <repo-path>] [--json]
```

### 3. Agent Characterization and Apply

The agent-neutral handoff contract is [`aicf-characterization-result.schema.json`](../../schemas/characterization/aicf-characterization-result.schema.json). The tool validates an agent result; it does not call an agent or execute repository commands.

```bash
python tooling/bootstrap/bootstrap_phase1.py characterize --path . --input characterization.json --output proposal.json
```

The input must contain the required characterization fields, proposed `project.md` and `rules.md`, and repository-relative evidence. Evidence paths must exist and remain inside the repository. Absolute paths, `file://` references, and detected secrets are rejected. The output includes deterministic analysis for reference and possible conflicts with existing `.aicf/rules.md`. Review the candidate JSON and Markdown before applying.

Apply only the selected initial artifacts:

```bash
python tooling/bootstrap/bootstrap_phase1.py apply --proposal-file proposal.json --select project.md
python tooling/bootstrap/bootstrap_phase1.py apply --proposal-file proposal.json --select rules.md,project.md
```

Applying a proposal uses conservative section merging. Existing content is preserved; possible rule conflicts are surfaced in the proposal for user review. Characterization does not write repository files; apply writes only selected files under `.aicf/`.

The legacy deterministic proposal flow remains available:
```bash
# Populate Tier 1 artifacts (default)
python tooling/bootstrap/bootstrap_phase1.py apply --select rules.md,project.md

# Populate all 4 artifacts
python tooling/bootstrap/bootstrap_phase1.py apply --all
```

### 4. Governance & Rule Conflict Detection
Reads local context to ground agent development, and evaluates tasks against `rules.md`:
```bash
# View context
python tooling/bootstrap/bootstrap_phase1.py govern

# Check a proposed task for rule violations
python tooling/bootstrap/bootstrap_phase1.py govern --check-task "Add Redux for state caching"
```

## Programmatic API

```python
from tooling.bootstrap import init, analyze, propose, apply, read_context, check_rule_conflict

# Initialize
init(repo_path)

# Analyze & propose
analysis = analyze(repo_path)
proposed = propose(analysis)

# Apply selected artifacts
apply(repo_path, selected_artifacts=["rules.md", "project.md"], proposed_content=proposed)

# Read context for agent tasks
context = read_context(repo_path)

# Verify task conformance
conflicts = check_rule_conflict(repo_path, "Task description")
```

## Safety Guarantees

1. **Path Neutrality:** Generated artifacts never contain absolute workstation paths (e.g. `D:\...`, `file:///...`).
2. **Credential Sanitization:** Generated artifacts never store API keys, tokens, passwords, or secrets.
3. **Conservative Merging:** User-authored rules and customizations are preserved and never silently overwritten.
4. **Git Safety:** Does not perform automatic commits, allowing human review via `git diff`.
