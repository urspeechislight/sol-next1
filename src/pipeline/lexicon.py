"""Lexicon registry — Arabic surface forms → canonical IDs.

Per the Option 2 lexicon-companion design: each registry under
`config/shards/` may have an optional companion file under
`config/lexicons/` of the same name. Lexicon files map registry names
to {arabic_surface: canonical_id}. load_config normalizes surface
keys at load time and validates that every value exists in the
corresponding registry.

Pipeline extractors call `config.lexicons[registry_name].lookup(text)`
where `text` is already normalized via `pipeline.utils.arabic.normalize_arabic`.
Lookup is dict access — no per-call normalization on the lexicon side.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LexiconEntry:
    """One Arabic surface form → canonical id mapping with provenance.

    `surface_normalized` is the dict key under which the entry is filed
    (the normalized form). `surface_raw` preserves the YAML-authored form
    for diagnostic messages.
    """

    surface_normalized: str
    surface_raw: str
    canonical_id: str
    source_file: str


@dataclass(frozen=True, slots=True)
class Lexicon:
    """All surface→id mappings for a single registry.

    `entries` is keyed by the *normalized* Arabic surface form. Callers
    must normalize their lookup input via the same `normalize_arabic`
    function used at load time.
    """

    registry_name: str
    entries: Mapping[str, LexiconEntry]

    def lookup(self, normalized_surface: str) -> str | None:
        """Resolve a normalized Arabic surface form to its canonical id.

        Returns None on miss. Callers handle unknowns according to their
        own policy (skip, log, raise).
        """
        entry = self.entries.get(normalized_surface)
        return entry.canonical_id if entry is not None else None
