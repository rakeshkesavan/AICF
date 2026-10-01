"""
AICF Phase 1 Bootstrap & Context Population Package.
Implements the workflow: init -> analyze -> select -> populate -> govern.
Normative Specification: AICF-004 (docs/03-bootstrap/09-aicf-004-bootstrap-and-context-population-phase-1-specification-v0.1.0.md).
"""

from .bootstrap_phase1 import (
    init,
    analyze,
    propose,
    apply,
    read_context,
    check_rule_conflict,
    AICFBootstrapError,
    SELECTABLE_ARTIFACTS,
    CANONICAL_PHASE1_FILES,
)

__all__ = [
    "init",
    "analyze",
    "propose",
    "apply",
    "read_context",
    "check_rule_conflict",
    "AICFBootstrapError",
    "SELECTABLE_ARTIFACTS",
    "CANONICAL_PHASE1_FILES",
]
