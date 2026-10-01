# AICF Tool Adapters & Integrations (Planned)

## Purpose

The **Tool Adapters Layer** translates canonical AICF context, rules, and task lifecycles into native instruction mechanisms and configuration formats required by individual AI developer environments.

### Core Areas
1. **Universal Adapter Contract:** Standard specifications for how adapters read `.aicf/`, formulate system prompts, bind tools, and record session state back to project memory.
2. **Cursor Integration:** Adapter mapping `.aicf/rules.md` and `.aicf/project.md` to `.cursorrules` / `.cursor/rules/` and editor prompts.
3. **Claude Integration:** System prompts, project knowledge loading, and tool definition contracts for Claude Code and Claude Workspaces.
4. **Gemini Integration:** Adapter mapping for Gemini CLI, Google Cloud Code, and Gemini developer extensions.
5. **Antigravity Integration:** Adapter mapping for Google Antigravity custom rules, skills, agents, and IDE workflows.

---

## Status

> [!NOTE]
> **Status: Planned**  
> As defined in [10-core-project-and-tool-layer.md](../02-architecture/10-core-project-and-tool-layer.md), tool adapters optimize *how* AICF is executed without altering *what AICF means*. Detailed adapter contracts will be defined following Bootstrap & Discovery.
