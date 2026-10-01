# AICF Tooling (Planned)

## Overview

The `tooling/` directory contains developer tools, automation scripts, and command-line interfaces for creating and maintaining AICF-compliant codebases.

## Structure

- **`bootstrap/`**: AICF-004 Phase 1 Bootstrap & Context Population engine (`bootstrap_phase1.py`).
  - `init`: Template generation for `.aicf/`.
  - `analyze`: Evidence-based stack and convention discovery.
  - `apply`: Non-destructive artifact population based on user selection.
  - `govern`: Context ingestion and rule conflict verification.
- **`cli/`**: Future unified AICF CLI (`aicf`). Planned capabilities include packaging the bootstrap engine alongside mature multi-agent adapters and characterization schemas.

