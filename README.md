# AICF

## AI Coding Framework

AICF (AI Coding Framework) is a structured framework for using AI coding agents consistently across software engineering.

It provides a common way to give AI agents the right context, rules, project knowledge, state, requirements, and workflows so that AI-assisted development becomes more predictable, repeatable, and maintainable.

AICF is designed to work across different AI coding tools and agents such as Claude, Gemini, Cursor, Antigravity, and similar tools.

---

## Why AICF?

AI-assisted development is increasingly becoming part of the engineering workflow, but teams often use different prompts, rules, context, and practices for the same type of work.

This can result in:

- Inconsistent code quality
- Repeated prompting and context setup
- Hallucinations and incorrect assumptions
- Loss of architectural context
- Agents making changes without understanding project constraints
- Different results across AI coding tools
- Difficulty reviewing or reproducing AI-assisted work
- High token usage caused by repeatedly providing the same context

AICF addresses this by introducing a **standardized context and operating model for AI-assisted software development**.

---

## Core Idea

AICF separates the information an AI agent needs into structured layers.

```text
                    ┌─────────────────────┐
                    │       AICF          │
                    │  AI Coding Framework │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
        AICF Core          Project Context     Tool Layer
             │                 │                 │
       Rules & principles   Architecture      Agent adapters
       Standards            Requirements      Workflows
       Governance           State             Integrations
       Security             Decisions
       Testing              Tasks
