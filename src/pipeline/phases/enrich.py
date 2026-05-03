"""Phase 4: ENRICH — translations, embeddings, grading, entity resolution.

Per ADR 0005 §3 (purity):
  Does: translate Units to English, embed Units, look up rijal grades per
        narrator, compute per-Sanad grades from per-narrator assessments
        and chain defects, aggregate cross-chain Hadith verdicts, resolve
        and canonicalize Entity mention candidates.
  Does NOT: create new mention entities (only resolves), write graph.

This is the phase where chain grading lives — not Phase 3.

Per ADR 0005 §3 side-effect authorization: this phase is the ONLY caller of
the embedding and translation APIs and the rijal database.
"""

from __future__ import annotations

from pipeline.config import Config
from pipeline.contracts import (
    PHASE_ENRICH,
    validate_manuscript_for_phase,
)
from pipeline.models import Manuscript


def enrich(manuscript: Manuscript, config: Config) -> Manuscript:
    """Run Phase 4: translate, embed, grade chains, resolve entities."""
    validate_manuscript_for_phase(manuscript, PHASE_ENRICH, config)
    # Implementation goes here. Before returning, record completion via
    # validate_manuscript_after_phase using the same manuscript/phase/config.
    raise NotImplementedError
