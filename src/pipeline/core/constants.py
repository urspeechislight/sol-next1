"""Stable constants and deterministic-ID helpers for the pipeline.

Per CLAUDE.md and ADR 0005 §6:
- All NUMERIC THRESHOLDS live in config/sol.yaml under thresholds:, NOT here.
- This module only holds names that are stable, not user-tunable, and load-bearing
  for determinism (UUID namespaces, regex patterns).
"""

from __future__ import annotations

from uuid import UUID, uuid5

ENTITY_NAMESPACE: UUID = UUID("a37f29c7-8b2e-4d6f-9c1a-7e8b3f5d2a1c")
"""UUID namespace for deterministic entity ID generation (ADR 0005 §6).

All entity IDs derive from uuid5(ENTITY_NAMESPACE, canonical_string). Frozen
once; do not regenerate — every existing ID depends on this value.
"""


def make_id(*parts: str) -> UUID:
    """Generate a deterministic UUID from a sequence of string parts.

    Per ADR 0005 §6: entity IDs are deterministic functions of content.
    Re-running a phase on the same input must produce the same IDs.

    Parts are joined with `|` so order matters and ordering changes produce
    different IDs. Callers should pass parts in a stable order.
    """
    canonical = "|".join(parts)
    return uuid5(ENTITY_NAMESPACE, canonical)
