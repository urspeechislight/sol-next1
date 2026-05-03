"""Pipeline domain models — the data flowing through the five phases.

Per ADR 0004 (graph ontology) and ADR 0005 (phase contracts):
- One `Span` type, populated progressively across phases (sol-next pattern, kept).
- Stance/alignment lives on edges to Faction nodes, not as properties.
- Non-structural entities and edges carry EvidenceAnchor + ExtractionProvenance.
- Entity IDs are deterministic: uuid5(ENTITY_NAMESPACE, canonical_string).

This module covers the data-flow and control-plane types that all phases share.
Domain entity types (Person, Faction, Event, Place, Verse, Hadith, Sanad,
ChainDefect, Work, Root, Lemma per ADR 0004 §1) are added as their extractors
are implemented and as the controlled-vocabulary fills (Task #2) settle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from uuid import UUID

# === Provenance and degradation ====================================


@dataclass(frozen=True)
class EvidenceAnchor:
    """Where in the source manuscript a claim is grounded.

    Required on every non-structural entity and edge (ADR 0004 §7).
    """

    span_id: UUID
    page_start: int
    page_end: int
    hierarchy_path: tuple[str, ...]
    context_before: str
    context_after: str


@dataclass(frozen=True)
class ExtractionProvenance:
    """Which extractor produced an entity, in which phase, via which patterns.

    Populated automatically by the entity-creation helper; never hand-written
    by extractor code.
    """

    extractor_id: str
    phase: str
    pattern_ids: tuple[str, ...]
    extracted_at: datetime


class DegradedMode(Enum):
    """Recoverable degradations a phase may produce. Per ADR 0005 §4.

    Members are declared in config/sol.yaml under degraded_modes: with their
    owning phase and downstream effect. Every fallback path adds the matching
    member to manuscript.degraded_modes.
    """

    NER_UNAVAILABLE = "NER_UNAVAILABLE"
    GAZETTEER_UNAVAILABLE = "GAZETTEER_UNAVAILABLE"
    RIJAL_UNAVAILABLE = "RIJAL_UNAVAILABLE"
    TRANSLATION_FAILED = "TRANSLATION_FAILED"
    EMBEDDING_PARTIAL = "EMBEDDING_PARTIAL"


@dataclass(frozen=True)
class ValidationIssue:
    """Per-instance context for a degradation or contract concern.

    Logged into manuscript.validation_issues whenever a DegradedMode is added,
    so the operator can see *which* span or narrator triggered each entry.
    """

    phase: str
    kind: str
    span_id: UUID | None
    cause: str


# === Document structure ============================================


@dataclass(frozen=True)
class HierarchyPath:
    """A span's position in the document's Kitab/Bab/Fasl structure.

    `path` holds the human-readable level names (e.g. ("Kitab al-Iman",
    "Bab al-Niyya")). `path_ids` holds the corresponding span IDs.
    """

    path: tuple[str, ...]
    path_ids: tuple[UUID, ...]
    depth: int


# === Core text-bearing types =======================================


@dataclass
class Page:
    """One page of an input manuscript. Produced by Phase 1."""

    id: UUID
    manuscript_id: UUID
    page_number: int
    text: str
    footnote_text: str | None = None


@dataclass
class Span:
    """A structural text segment, populated progressively across phases.

    Phase 2 (SEGMENT) sets patterns/behavior/hierarchy; Phase 3 (EXTRACT)
    sets entity_ids/unit_ids. Later phases reference but do not restructure.
    """

    id: UUID
    page_start: int
    page_end: int
    text: str

    # Phase 2 (SEGMENT):
    patterns: list[str] = field(default_factory=lambda: [])  # noqa: PIE807
    behavior: str | None = None
    hierarchy: HierarchyPath | None = None

    # Phase 3 (EXTRACT):
    entity_ids: list[UUID] = field(default_factory=lambda: [])  # noqa: PIE807
    unit_ids: list[UUID] = field(default_factory=lambda: [])  # noqa: PIE807


@dataclass
class Unit:
    """One atomic semantic unit extracted from a Span.

    Phase 3 produces (text, unit_type); Phase 4 enriches (translation_en,
    embedding). Per ADR 0005 §3, embedding is Phase 4 work — never Phase 3.
    """

    id: UUID
    span_id: UUID
    text: str
    unit_type: str

    # Phase 4 (ENRICH):
    translation_en: str | None = None
    embedding: tuple[float, ...] | None = None


@dataclass
class Entity:
    """A mention candidate produced in Phase 3 and resolved in Phase 4.

    `entity_type` is validated against config.entity_types at extraction time
    (ADR 0004 §1). `mention_status` distinguishes pre-merge candidates from
    canonicalized entities; valid values are "candidate" | "canonical" |
    "merged_into:<uuid>".
    """

    id: UUID
    entity_type: str
    surface_form: str
    evidence: EvidenceAnchor
    provenance: ExtractionProvenance
    mention_status: str = "candidate"


@dataclass
class Edge:
    """A knowledge-graph edge produced by Phase 5.

    Validated against the edge-type registry per ADR 0004 §3 before write.
    Non-structural edges must populate all five provenance fields per §7;
    Phase 5's emit path raises GraphSchemaError if any are missing on a
    non-structural edge.
    """

    edge_type: str
    source_id: UUID
    target_id: UUID
    properties: dict[str, object]
    source_work_id: UUID | None = None
    source_passage_id: UUID | None = None
    evidence: EvidenceAnchor | None = None
    extractor_id: str | None = None
    confidence: float | None = None


# === The phase-flow container ======================================


@dataclass
class Manuscript:
    """The container passed through all five phases. Mutated in-place.

    Per ADR 0005 §1: each phase populates the fields it owns; never overwrites
    a previous phase's output; never writes out of band. completed_phases
    tracks which phases have run successfully (used by the contract validator).
    """

    id: UUID
    urn: str
    title: str
    source_path: Path | None = None
    author: str | None = None
    category: str | None = None

    # Phase 1 (INGEST):
    pages: list[Page] = field(default_factory=lambda: [])  # noqa: PIE807

    # Phase 2 (SEGMENT):
    spans: list[Span] = field(default_factory=lambda: [])  # noqa: PIE807

    # Phase 3 (EXTRACT):
    units: list[Unit] = field(default_factory=lambda: [])  # noqa: PIE807
    entities: list[Entity] = field(default_factory=lambda: [])  # noqa: PIE807

    # Phase 5 (GRAPH):
    edges: list[Edge] = field(default_factory=lambda: [])  # noqa: PIE807

    # Cross-phase tracking:
    completed_phases: set[str] = field(default_factory=lambda: set())  # noqa: PLW0108
    degraded_modes: set[DegradedMode] = field(default_factory=lambda: set())  # noqa: PLW0108
    validation_issues: list[ValidationIssue] = field(default_factory=lambda: [])  # noqa: PIE807
