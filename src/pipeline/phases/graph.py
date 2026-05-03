"""Phase 5: GRAPH — knowledge graph projection into Neo4j.

Per ADR 0005 §3 (purity):
  Does: emit structural edges (CONTAINS, NEXT, HAS_SECTION, HAS_FOOTNOTE,
        HAS_SANAD, HAS_MATN, INCLUDES_NARRATOR), emit cross-domain edges per
        ADR 0004 (HAS_STANCE, PARTICIPATED_IN, INTERPRETS_VERSE, MENTIONS_*),
        validate every edge against the registry before write, write batches
        atomically.
  Does NOT: create new entities, change grades, re-extract.

Per ADR 0005 §3 side-effect authorization: this phase is the ONLY writer to
Neo4j. Postgres updates for canonical entities/units happen at the end of
Phase 4, before this phase runs.

Per ADR 0003: Neo4j is a projection of the Postgres source-of-truth and is
deterministically rebuildable; this phase is the rebuild path.
"""

from __future__ import annotations

from pipeline.config import Config
from pipeline.contracts import (
    PHASE_GRAPH,
    validate_manuscript_for_phase,
)
from pipeline.models import Manuscript


def graph(manuscript: Manuscript, config: Config) -> Manuscript:
    """Run Phase 5: project the manuscript's entities and edges into Neo4j."""
    validate_manuscript_for_phase(manuscript, PHASE_GRAPH, config)
    # Implementation goes here. Before returning, record completion via
    # validate_manuscript_after_phase using the same manuscript/phase/config.
    raise NotImplementedError
