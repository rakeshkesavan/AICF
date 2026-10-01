# AICF Adapters (Planned)

## Overview

Adapters translate canonical AICF project context into native configuration, prompt files, and instruction artifacts tailored to specific AI coding agents and editor environments.

## Structure

- **`cursor/`**: Adapters for Cursor IDE (e.g., `.cursorrules`, `.cursor/rules/`).
- **`claude/`**: Adapters for Anthropic Claude (Claude Code, workspace memory, custom system prompts).
- **`gemini/`**: Adapters for Google Gemini developer environments and CLI tooling.
- **`antigravity/`**: Adapters for Google Antigravity IDE, custom skills, rules, and agents.

---

> [!NOTE]
> **Status: Planned**  
> Adapters ensure vendor neutrality: a single `.aicf/` folder can be seamlessly utilized across multiple AI coding assistants without altering underlying project truth.
