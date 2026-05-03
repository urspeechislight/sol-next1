"""The five-phase pipeline. Per ADR 0005 §3, each phase has a strict purity
contract — what it does and what it does NOT do."""

from pipeline.phases.enrich import enrich
from pipeline.phases.extract import extract
from pipeline.phases.graph import graph
from pipeline.phases.ingest import ingest
from pipeline.phases.segment import segment

__all__ = ["enrich", "extract", "graph", "ingest", "segment"]
