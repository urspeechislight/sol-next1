"""Phase 3: EXTRACT — Spans → Entities (mention candidates) + Units.

Per ADR 0005 §3 (purity):
  Does: run extractors per behavior; produce mention-candidate entities
        (Person, Event, Verse, ...) with provenance; atomicize spans into
        Units; emit unresolved CITATION_MENTION-style references.
  Does NOT: grade chains (Phase 4), embed (Phase 4), translate (Phase 4),
        resolve / canonicalize entities (Phase 4), write graph (Phase 5).

Explicit fix from sol-next: chain grading is NOT here. _apply_preliminary_chain_grades
in src/phases/extract.py:454-483 of the predecessor was a phasing leak.
"""

from __future__ import annotations

from pipeline.config import Config
from pipeline.contracts import (
    PHASE_EXTRACT,
    validate_manuscript_for_phase,
)
from pipeline.models import Manuscript


def extract(manuscript: Manuscript, config: Config) -> Manuscript:
    """Run Phase 3: produce mention-candidate entities and atomic units."""
    validate_manuscript_for_phase(manuscript, PHASE_EXTRACT, config)
    # Implementation goes here. Before returning, record completion via
    # validate_manuscript_after_phase using the same manuscript/phase/config.
    raise NotImplementedError
