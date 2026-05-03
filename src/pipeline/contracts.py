"""Phase contracts and runtime validators.

Per ADR 0005 §2, every phase function calls validate_manuscript_for_phase()
as its first executable line and validate_manuscript_after_phase() as its
last before return. Contracts are loaded from config/sol.yaml under
phase_contracts: — never hard-coded in this file.

This module defines the data shape and validator entry points; the
config-loading wiring lives in src/pipeline/config.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pipeline.core.exceptions import ContractError, DegradedBudgetExceededError
from pipeline.models import DegradedMode, Manuscript

if TYPE_CHECKING:
    from pipeline.config import Config

PHASE_INGEST = "ingest"
PHASE_SEGMENT = "segment"
PHASE_EXTRACT = "extract"
PHASE_ENRICH = "enrich"
PHASE_GRAPH = "graph"

ALL_PHASES: tuple[str, ...] = (
    PHASE_INGEST,
    PHASE_SEGMENT,
    PHASE_EXTRACT,
    PHASE_ENRICH,
    PHASE_GRAPH,
)


@dataclass(frozen=True)
class PhaseContract:
    """Declared requirements and guarantees for one phase.

    Per ADR 0005 §2:
    - requires_completed: prior phases that must be in completed_phases.
    - requires_fields_populated: Manuscript field names that must be non-empty
      on input.
    - produces_fields: Manuscript field names this phase guarantees to populate.
    - forbids_degraded: degraded modes that disqualify this phase from running.
    - permits_degraded: degraded modes the phase tolerates and passes through.
    """

    phase: str
    requires_completed: tuple[str, ...] = ()
    requires_fields_populated: tuple[str, ...] = ()
    produces_fields: tuple[str, ...] = ()
    forbids_degraded: tuple[DegradedMode, ...] = ()
    permits_degraded: tuple[DegradedMode, ...] = ()


def _is_field_populated(manuscript: Manuscript, field_name: str) -> bool:
    """Return True if the named Manuscript field is non-None and non-empty.

    For sized values (lists, sets, dicts, strings), populated means len() > 0.
    For other values, populated means the value is not None.
    """
    value = getattr(manuscript, field_name, None)
    if value is None:
        return False
    if hasattr(value, "__len__"):
        return len(value) > 0
    return True


def validate_manuscript_for_phase(manuscript: Manuscript, phase: str, config: Config) -> None:
    """Verify the manuscript meets the input contract of `phase`.

    Per ADR 0005 §2 — first executable line of every phase function.
    The PhaseContract is read from config.phase_contracts[phase].
    Raises ContractError if any required invariant is unmet, or
    DegradedBudgetExceededError if degraded_modes intersects forbids_degraded.
    """
    contract = config.phase_contracts.get(phase)
    if contract is None:
        raise ContractError(f"No phase_contract defined for phase '{phase}'")

    missing_predecessors = set(contract.requires_completed) - manuscript.completed_phases
    if missing_predecessors:
        raise ContractError(
            f"Phase '{phase}' requires completed phases {sorted(missing_predecessors)}; "
            f"have {sorted(manuscript.completed_phases)}"
        )

    unpopulated = [
        f for f in contract.requires_fields_populated if not _is_field_populated(manuscript, f)
    ]
    if unpopulated:
        raise ContractError(
            f"Phase '{phase}' requires populated fields: {unpopulated} "
            f"on manuscript {manuscript.urn}"
        )

    forbidden_present = manuscript.degraded_modes & set(contract.forbids_degraded)
    if forbidden_present:
        forbidden_names = sorted(m.name for m in forbidden_present)
        raise DegradedBudgetExceededError(
            f"Phase '{phase}' cannot run with degraded modes "
            f"{forbidden_names} on manuscript {manuscript.urn}"
        )


def validate_manuscript_after_phase(manuscript: Manuscript, phase: str, config: Config) -> None:
    """Verify the manuscript meets the output contract of the just-finished `phase`.

    Per ADR 0005 §2 — last executable line of every phase function before return.
    Raises ContractError if any guaranteed field is unpopulated. On success,
    adds `phase` to manuscript.completed_phases.
    """
    contract = config.phase_contracts.get(phase)
    if contract is None:
        raise ContractError(f"No phase_contract defined for phase '{phase}'")

    unpopulated = [f for f in contract.produces_fields if not _is_field_populated(manuscript, f)]
    if unpopulated:
        raise ContractError(
            f"Phase '{phase}' did not populate guaranteed fields: {unpopulated} "
            f"on manuscript {manuscript.urn}"
        )

    manuscript.completed_phases.add(phase)


def validate_contract_chain(phases: tuple[str, ...], config: Config) -> None:
    """Verify a sequence of phases is internally consistent.

    Each phase's requires_completed must be satisfied by predecessors in the
    sequence. Used at pipeline startup to catch misconfigured runs before any
    work executes. Raises ContractError on inconsistency.
    """
    completed: set[str] = set()
    for phase in phases:
        contract = config.phase_contracts.get(phase)
        if contract is None:
            raise ContractError(f"No phase_contract defined for phase '{phase}'")
        missing = set(contract.requires_completed) - completed
        if missing:
            raise ContractError(
                f"Phase '{phase}' in chain {list(phases)} requires {sorted(missing)} "
                f"which are not in the prior chain prefix"
            )
        completed.add(phase)
