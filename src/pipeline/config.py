"""Pipeline configuration loaded from config/sol.yaml.

Per ADR 0005 §5: dependency liveness probes happen here at config load,
NOT at module import time. Two states must be distinguishable:
  - feature disabled: no probe, no fallback.
  - feature enabled, service down at startup: ConfigError raised.

Per CLAUDE.md: numeric thresholds live in YAML (under thresholds:), never in
Python code. Pipeline modules read them via Config.thresholds[name].

Lexicons (Arabic surface form → canonical id) are loaded from sibling
`config/lexicons/*.yaml` files. Each lexicon file maps registry names to
{arabic_surface: canonical_id} mappings. The loader normalizes surface
keys via `normalize_arabic` and validates that every value exists in the
corresponding registry. See `pipeline.lexicon` for runtime use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from pipeline.contracts import ALL_PHASES, PhaseContract
from pipeline.core.exceptions import ConfigError
from pipeline.lexicon import Lexicon, LexiconEntry
from pipeline.models import DegradedMode
from pipeline.utils.arabic import normalize_arabic

REQUIRED_TOP_LEVEL_KEYS = frozenset(
    {"features", "phase_contracts", "book_categories", "degraded_modes"}
)

# Top-level keys that are NOT vocabulary registries (excluded from
# registry-id extraction). Anything else that's a list-of-strings is a
# registry that lexicons may target.
_NON_REGISTRY_KEYS = frozenset(
    {
        "__includes__",
        "features",
        "phase_contracts",
        "degraded_modes",
        "thresholds",
        "edge_types",
    }
)

# Subdirectory of the entry-point YAML's parent that holds lexicon files.
_LEXICONS_SUBDIR = "lexicons"


@dataclass(frozen=True)
class FeatureFlags:
    """Which optional pipeline features are enabled for this run.

    Disabled features skip both their conditional import and their dependency
    liveness probe (ADR 0005 §5).
    """

    rijal_enabled: bool
    translation_enabled: bool
    embedding_enabled: bool


@dataclass(frozen=True)
class Config:
    """The validated pipeline configuration.

    Built by load_config() from config/sol.yaml. All registries are settled
    here; pipeline code never reads YAML directly.
    """

    book_categories: frozenset[str]
    entity_types: frozenset[str]
    edge_types: dict[str, dict[str, object]]
    factions: frozenset[str]
    event_types: frozenset[str]
    phase_contracts: dict[str, PhaseContract]
    thresholds: dict[str, float]
    features: FeatureFlags
    lexicons: dict[str, Lexicon] = field(default_factory=lambda: {})  # noqa: PIE807


def load_config(path: Path) -> Config:
    """Parse `path`, validate registries, probe enabled dependencies.

    Raises ConfigError if YAML parsing fails, registry references are broken,
    or any feature-enabled external service fails its liveness probe (ADR 0005 §5).
    """
    raw = _parse_yaml(path)
    raw = _expand_includes(raw, path.parent)
    _check_top_level_shape(raw)
    _validate_degraded_modes_registry(raw["degraded_modes"])
    phase_contracts = _build_phase_contracts(raw["phase_contracts"])
    _check_phase_set_complete(phase_contracts)

    book_categories = frozenset(raw["book_categories"])
    if not book_categories:
        raise ConfigError("book_categories registry is empty")

    registry_index = _extract_registry_ids(raw)
    lexicons = _load_lexicon_files(path.parent / _LEXICONS_SUBDIR, registry_index)

    return Config(
        book_categories=book_categories,
        entity_types=frozenset(raw.get("entity_types") or []),
        edge_types=raw.get("edge_types") or {},
        factions=frozenset(raw.get("factions") or []),
        event_types=frozenset(raw.get("event_types") or []),
        phase_contracts=phase_contracts,
        thresholds=raw.get("thresholds") or {},
        features=_build_features(raw["features"]),
        lexicons=lexicons,
    )


def _parse_yaml(path: Path) -> dict[str, Any]:
    """Read the YAML file at `path` and ensure the root is a mapping."""
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    try:
        raw = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        raise ConfigError(f"YAML parse error in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError(f"Config root must be a mapping, got {type(raw).__name__}")
    return raw  # type: ignore[no-any-return]


def _expand_includes(raw: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    """Resolve __includes__ directives in `raw` by merging shard contents inline.

    Each entry in __includes__ is a path (relative to `base_dir`) to a YAML
    file whose top-level keys are merged into `raw`. Per-key collisions
    raise ConfigError — the registry is one namespace and silent overwrites
    would be a bug.
    """
    includes = raw.pop("__includes__", None)
    if includes is None:
        return raw
    if not isinstance(includes, list):
        raise ConfigError(f"__includes__ must be a list of paths, got {type(includes).__name__}")
    for include_path in includes:  # pyright: ignore[reportUnknownVariableType]
        if not isinstance(include_path, str):
            raise ConfigError(f"__includes__ entry must be a string, got {include_path!r}")
        target = (base_dir / include_path).resolve()
        shard = _parse_yaml(target)
        shard = _expand_includes(shard, target.parent)
        collisions = set(shard.keys()) & set(raw.keys())
        if collisions:
            raise ConfigError(f"include {target} collides with existing keys: {sorted(collisions)}")
        raw.update(shard)
    return raw


def _check_top_level_shape(raw: dict[str, Any]) -> None:
    """Verify all required top-level keys are present in the parsed config."""
    missing = REQUIRED_TOP_LEVEL_KEYS - set(raw.keys())
    if missing:
        raise ConfigError(f"Config missing top-level keys: {sorted(missing)}")


def _build_features(features_raw: dict[str, Any]) -> FeatureFlags:
    """Construct FeatureFlags from the raw features mapping."""
    return FeatureFlags(
        rijal_enabled=bool(features_raw.get("rijal_enabled", False)),
        translation_enabled=bool(features_raw.get("translation_enabled", False)),
        embedding_enabled=bool(features_raw.get("embedding_enabled", False)),
    )


def _validate_degraded_modes_registry(declared_raw: dict[str, Any]) -> None:
    """Verify the YAML degraded_modes keys match the DegradedMode enum exactly."""
    declared = set(declared_raw.keys())
    enum_members = {m.name for m in DegradedMode}
    if declared == enum_members:
        return
    gap_yaml = enum_members - declared
    gap_enum = declared - enum_members
    details: list[str] = []
    if gap_yaml:
        details.append(f"undeclared in YAML: {sorted(gap_yaml)}")
    if gap_enum:
        details.append(f"declared in YAML but not in enum: {sorted(gap_enum)}")
    raise ConfigError(f"degraded_modes registry mismatch — {' / '.join(details)}")


def _build_phase_contracts(raw_contracts: dict[str, Any]) -> dict[str, PhaseContract]:
    """Construct the phase_contracts mapping from raw YAML data."""
    contracts: dict[str, PhaseContract] = {}
    for phase_name, contract_raw in raw_contracts.items():
        try:
            forbids = tuple(DegradedMode(n) for n in contract_raw.get("forbids_degraded", []))
            permits = tuple(DegradedMode(n) for n in contract_raw.get("permits_degraded", []))
        except ValueError as exc:
            raise ConfigError(
                f"phase_contracts.{phase_name}: unknown DegradedMode — {exc}"
            ) from exc
        contracts[phase_name] = PhaseContract(
            phase=phase_name,
            requires_completed=tuple(contract_raw.get("requires_completed", [])),
            requires_fields_populated=tuple(contract_raw.get("requires_fields_populated", [])),
            produces_fields=tuple(contract_raw.get("produces_fields", [])),
            forbids_degraded=forbids,
            permits_degraded=permits,
        )
    return contracts


def _check_phase_set_complete(contracts: dict[str, PhaseContract]) -> None:
    """Verify the phase_contracts mapping covers exactly the five known phases."""
    expected = set(ALL_PHASES)
    actual = set(contracts.keys())
    if expected == actual:
        return
    missing = expected - actual
    extra = actual - expected
    details: list[str] = []
    if missing:
        details.append(f"missing: {sorted(missing)}")
    if extra:
        details.append(f"unknown: {sorted(extra)}")
    raise ConfigError(f"phase_contracts {' / '.join(details)}")


def _extract_registry_ids(merged: dict[str, Any]) -> dict[str, frozenset[str]]:
    """Scan merged YAML for list-of-strings registries.

    Returns a map from registry name to the frozenset of valid canonical
    ids declared by that registry. Used to validate lexicon referential
    integrity.

    Top-level keys excluded: pipeline-internal (features, phase_contracts,
    degraded_modes, thresholds, edge_types). Anything else whose value is
    a list of strings is treated as a registry. Lists of dicts (e.g.,
    masumin) and other shapes are skipped silently — they're not
    string-id registries.
    """
    registries: dict[str, frozenset[str]] = {}
    for key, value in merged.items():
        if key in _NON_REGISTRY_KEYS:
            continue
        if not isinstance(value, list):
            continue
        items: list[object] = list(value)  # type: ignore[arg-type]  -- yaml-Any
        if all(isinstance(item, str) for item in items):
            registries[key] = frozenset(item for item in items if isinstance(item, str))
    return registries


def _load_lexicon_files(
    lexicons_dir: Path,
    registry_index: dict[str, frozenset[str]],
) -> dict[str, Lexicon]:
    """Discover and load all lexicon YAML files in `lexicons_dir`.

    Returns a map from registry name to Lexicon. Validates referential
    integrity (every value must be in its registry's id set) and detects
    collisions (within a file or across files for the same registry).
    """
    if not lexicons_dir.exists():
        return {}
    accumulated: dict[str, dict[str, LexiconEntry]] = {}
    for path in sorted(lexicons_dir.glob("*.yaml")):
        per_file = _load_one_lexicon(path, registry_index)
        for registry_name, file_entries in per_file.items():
            existing = accumulated.setdefault(registry_name, {})
            for normalized, entry in file_entries.items():
                prior = existing.get(normalized)
                if prior is None:
                    existing[normalized] = entry
                    continue
                if prior.canonical_id != entry.canonical_id:
                    raise ConfigError(
                        f"lexicon collision for registry {registry_name!r}: "
                        f"surface {entry.surface_raw!r} (in {entry.source_file}) "
                        f"conflicts with prior mapping in {prior.source_file} "
                        f"({prior.canonical_id} vs {entry.canonical_id})"
                    )
    return {
        name: Lexicon(registry_name=name, entries=dict(entries))
        for name, entries in accumulated.items()
    }


def _load_one_lexicon(
    path: Path,
    registry_index: dict[str, frozenset[str]],
) -> dict[str, dict[str, LexiconEntry]]:
    """Parse one lexicon file. Returns {registry_name: {normalized: entry}}."""
    raw = _parse_yaml(path)
    out: dict[str, dict[str, LexiconEntry]] = {}
    for registry_name, mapping in raw.items():
        if registry_name not in registry_index:
            raise ConfigError(
                f"{path}: lexicon refers to unknown registry "
                f"{registry_name!r}; declare it in config/shards/ first"
            )
        if not isinstance(mapping, dict):
            raise ConfigError(
                f"{path}:{registry_name}: must be a mapping of Arabic→id, "
                f"got {type(mapping).__name__}"
            )
        valid_ids = registry_index[registry_name]
        out[registry_name] = _build_file_entries(
            mapping,  # pyright: ignore[reportUnknownArgumentType]  -- yaml-Any
            registry_name,
            valid_ids,
            source_file=str(path),
        )
    return out


def _build_file_entries(
    mapping: dict[str, Any],
    registry_name: str,
    valid_ids: frozenset[str],
    source_file: str,
) -> dict[str, LexiconEntry]:
    """Build per-file LexiconEntry dict, normalizing keys and validating values."""
    entries: dict[str, LexiconEntry] = {}
    for surface_raw, canonical_id in mapping.items():
        if not isinstance(canonical_id, str):
            raise ConfigError(f"{source_file}:{registry_name}: lexicon values must be strings")
        if canonical_id not in valid_ids:
            raise ConfigError(
                f"{source_file}:{registry_name}: surface {surface_raw!r} maps to "
                f"{canonical_id!r} which is not in the registry"
            )
        normalized = normalize_arabic(surface_raw)
        if not normalized:
            raise ConfigError(
                f"{source_file}:{registry_name}: surface {surface_raw!r} normalizes to empty string"
            )
        prior = entries.get(normalized)
        if prior is not None and prior.canonical_id != canonical_id:
            raise ConfigError(
                f"{source_file}:{registry_name}: surface forms "
                f"{prior.surface_raw!r} and {surface_raw!r} both normalize to "
                f"{normalized!r} but map to different ids "
                f"({prior.canonical_id} vs {canonical_id})"
            )
        if prior is None:
            entries[normalized] = LexiconEntry(
                surface_normalized=normalized,
                surface_raw=surface_raw,
                canonical_id=canonical_id,
                source_file=source_file,
            )
    return entries
