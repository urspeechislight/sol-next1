"""Manuscript ingest + processing pipeline.

This is the heavy-compute service that consumes raw manuscript JSON and
produces structured entities, embeddings, and graph edges. It runs as an
out-of-band worker, not part of the FastAPI request path.

The pipeline is intentionally empty in the foundation — it is rebuilt on top
of this harness in subsequent work.
"""

__version__ = "0.0.0"
