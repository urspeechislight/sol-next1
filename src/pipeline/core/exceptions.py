"""Exception hierarchy for the pipeline.

Flat hierarchy. Phase-specific error context is carried in the message and
structured fields, not in a class subtree (per sol-next's working pattern,
kept). Control-plane errors (ConfigError, ContractError, ...) are typed
because they have distinct semantics; phase-internal failures share PhaseError.
"""

from __future__ import annotations


class PipelineError(Exception):
    """Base class for all pipeline errors."""


class ConfigError(PipelineError):
    """Configuration is invalid or a declared dependency is unreachable at startup.

    Per ADR 0005 §5: liveness probes for feature-enabled external services run
    at config load. Failures raise this, not at module import time. This is
    distinct from runtime transient failures, which populate DegradedMode.
    """


class ContractError(PipelineError):
    """A phase's input or output contract was violated.

    Raised by validate_manuscript_for_phase() and
    validate_manuscript_after_phase() per ADR 0005 §2.
    """


class DegradedBudgetExceededError(PipelineError):
    """A phase cannot run because the manuscript's degraded modes intersect
    with this phase's forbids_degraded set (per ADR 0005 §4)."""


class PhaseAuthorizationError(PipelineError):
    """A phase attempted an unauthorized side effect.

    Per ADR 0005 §3 side-effect authorization table — e.g. a non-Phase-5
    function tried to write to Neo4j, or a non-Phase-4 function called the
    embedding API.
    """


class GraphSchemaError(PipelineError):
    """An edge does not match the declared edge-type registry.

    Per ADR 0004 §3: source/target labels not in the registry, edge type
    out of registry, or edge property not declared in the registry.
    """


class PhaseError(PipelineError):
    """A phase-internal failure: malformed input, FSM into an unexpected state,
    extractor invariant violated, etc.

    Carries the phase name and a structured reason as attributes for
    structured logging.
    """

    def __init__(self, phase: str, reason: str, **context: object) -> None:
        """Build a PhaseError with phase tag and structured context."""
        super().__init__(f"[{phase}] {reason}")
        self.phase = phase
        self.reason = reason
        self.context = context
