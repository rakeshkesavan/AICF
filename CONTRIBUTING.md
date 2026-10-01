# Contributing to AICF

Thank you for your interest in contributing to the **AI Companion Framework (AICF)**!

AICF is an open, vendor-neutral framework designed to standardize context, operating models, memory, and safety invariants for AI-assisted software development. We welcome contributions from developers, researchers, architects, and tooling builders.

---

## Code of Conduct

All contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the behavioral standards we expect across our community.

---

## How Can You Contribute?

As AICF is currently establishing its core specifications, contributions are particularly valuable in the following areas:

1. **Specification & Documentation Feedback**
   - Review the [Foundation specifications](docs/01-foundation/) and [Architecture documents](docs/02-architecture/).
   - Identify edge cases, ambiguities, or missing principles in the AI operating and behavior models.

2. **Artifact Schemas & Templates**
   - Provide feedback on the canonical starter template in `templates/default/.aicf/`.
   - Propose enhancements to markdown schemas, frontmatter conventions, and validation criteria.

3. **Tool Adapters (Planned)**
   - Contribute knowledge, patterns, and prototype configs for specific AI environments (Cursor, Claude, Gemini, Antigravity, Copilot, etc.).

4. **Reference Examples & Case Studies**
   - Propose realistic example repository setups across diverse software stacks (e.g., React/Node, Angular/Java, microservices, monorepos).

---

## Contribution Workflow

### 1. Issues & Discussions
- Before initiating major changes or drafting new specifications, please open an Issue to discuss the motivation and design.
- Label issues appropriately (`enhancement`, `bug`, `documentation`, `spec-proposal`).

### 2. Fork and Branch
- Fork the repository and create your feature branch from `main`:
  ```bash
  git checkout -b feature/my-proposal
  ```

### 3. File Naming & Documentation Style
- **Naming:** Use lowercase, `kebab-case` for all files and directories (e.g., `01-framework-charter.md`).
- **Formatting:** Write in clean, GitHub-flavored Markdown. Ensure all internal relative links resolve properly.
- **Independence:** Keep core framework definitions vendor-neutral and tool-agnostic.
- **Hygiene:** Do not commit local file paths, private URLs, API keys, tokens, or proprietary organization information.

### 4. Submitting a Pull Request
- Open a Pull Request against the `main` branch using the provided [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).
- Clearly describe:
  - What problem the change solves.
  - Which documents or templates are modified or added.
  - Any architectural decisions or trade-offs involved.

---

## Governance & Licensing Notes

> [!NOTE]
> **License & Contributor License Agreement (TODO/Review Item)**
> AICF repository licensing is currently pending finalization by the project maintainers. Contributions submitted during this initial phase will be subject to the open-source license selected upon formal release.
