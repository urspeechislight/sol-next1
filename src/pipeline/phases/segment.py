"""Phase 2: SEGMENT — Pages → Spans with patterns, behavior, hierarchy.

Per ADR 0005 §3 (purity):
  Does: split text into Spans, detect surface patterns, route patterns to
        behaviors via the routing table, run FSM trackers (KitabBabFasl,
        SanadMatn, ...) to assign HierarchyPath.
  Does NOT: create entities, grade chains, embed, translate, write graph.
"""

from __future__ import annotations

from pipeline.config import Config
from pipeline.contracts import (
    PHASE_SEGMENT,
    validate_manuscript_for_phase,
)
from pipeline.models import Manuscript


def segment(manuscript: Manuscript, config: Config) -> Manuscript:
    """Run Phase 2: split pages into spans, assign patterns / behavior / hierarchy."""
    validate_manuscript_for_phase(manuscript, PHASE_SEGMENT, config)
    # Implementation goes here. Before returning, record completion via
    # validate_manuscript_after_phase using the same manuscript/phase/config.
    raise NotImplementedError
