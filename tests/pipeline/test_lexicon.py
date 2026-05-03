"""Tests for lexicon loading and lookup (pipeline.lexicon + load_config)."""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.config import Config, load_config
from pipeline.core.exceptions import ConfigError
from pipeline.lexicon import Lexicon, LexiconEntry
from pipeline.utils.arabic import normalize_arabic

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "sol.yaml"


@pytest.fixture(scope="module")
def config() -> Config:
    """Loaded pipeline config (module-scoped — shared across tests)."""
    return load_config(CONFIG_PATH)


def test_should_load_rijal_lexicons_when_config_loads(config: Config) -> None:
    """Lexicon files in config/lexicons/ produce per-registry Lexicon objects."""
    assert "rijal_grades_sunni" in config.lexicons
    assert "rijal_grades_shia" in config.lexicons


def test_should_resolve_thiqa_when_arabic_form_looked_up(config: Config) -> None:
    """ثقة (with or without diacritics) resolves to THIQA in the Sunni registry."""
    sunni = config.lexicons["rijal_grades_sunni"]
    assert sunni.lookup(normalize_arabic("ثقة")) == "THIQA"
    assert sunni.lookup(normalize_arabic("ثِقَة")) == "THIQA"


def test_should_resolve_synonyms_to_same_id_when_distinct_arabic_terms(
    config: Config,
) -> None:
    """مستور (rank 7 synonym) and مجهول الحال resolve to distinct ids per Ibn Hajar.

    Per Nukhbat p.59, mastur and majhul al-hal are SYNONYMOUS but registered
    as separate canonical ids (MASTUR and MAJHUL_AL_HAL) — both ids exist in
    the registry. Each surface form maps to the matching id; the synonymy is
    documented at the registry level, not collapsed in the lexicon.
    """
    sunni = config.lexicons["rijal_grades_sunni"]
    assert sunni.lookup(normalize_arabic("مستور")) == "MASTUR"
    assert sunni.lookup(normalize_arabic("مجهول الحال")) == "MAJHUL_AL_HAL"


def test_should_distinguish_rank_7_majhul_from_rank_9_majhul(config: Config) -> None:
    """مجهول (single-transmitter, rank 9) maps to MAJHUL — not to MAJHUL_AL_HAL.

    Critical distinction in Ibn Hajar's scheme that the lexicon must preserve.
    """
    sunni = config.lexicons["rijal_grades_sunni"]
    assert sunni.lookup(normalize_arabic("مجهول")) == "MAJHUL"
    assert sunni.lookup(normalize_arabic("مجهول")) != "MAJHUL_AL_HAL"


def test_should_use_sunni_or_shia_registry_per_caller_when_homonym(
    config: Config,
) -> None:
    """ثقة exists in both Sunni and Shia registries — caller picks namespace."""
    sunni = config.lexicons["rijal_grades_sunni"]
    shia = config.lexicons["rijal_grades_shia"]
    assert sunni.lookup(normalize_arabic("ثقة")) == "THIQA"
    assert shia.lookup(normalize_arabic("ثقة")) == "THIQA"
    # Both happen to share the surface form AND the canonical id string,
    # but they live in distinct lexicons so the caller is in control.


def test_should_return_none_when_arabic_form_unknown(config: Config) -> None:
    """Unknown surface forms return None — extractor handles per its policy."""
    sunni = config.lexicons["rijal_grades_sunni"]
    assert sunni.lookup(normalize_arabic("ليس في القاموس")) is None


def test_should_raise_when_lexicon_value_not_in_registry(tmp_path: Path) -> None:
    """A lexicon value referencing an unknown id raises ConfigError at load."""
    sol = tmp_path / "sol.yaml"
    sol.write_text(_minimal_sol_yaml(includes=["shards/test.yaml"]))
    (tmp_path / "shards").mkdir()
    (tmp_path / "shards" / "test.yaml").write_text("test_grades:\n  - VALID_ID\n")
    (tmp_path / "lexicons").mkdir()
    (tmp_path / "lexicons" / "test.yaml").write_text(
        "test_grades:\n  ثقة: BOGUS_ID\n"
    )
    with pytest.raises(ConfigError) as exc_info:
        load_config(sol)
    assert "BOGUS_ID" in str(exc_info.value)


def test_should_raise_when_lexicon_collides_within_file(tmp_path: Path) -> None:
    """Two surface forms that normalize identically with different ids raises."""
    sol = tmp_path / "sol.yaml"
    sol.write_text(_minimal_sol_yaml(includes=["shards/test.yaml"]))
    (tmp_path / "shards").mkdir()
    (tmp_path / "shards" / "test.yaml").write_text(
        "test_grades:\n  - FIRST\n  - SECOND\n"
    )
    (tmp_path / "lexicons").mkdir()
    # ثِقَة and ثقة normalize identically (diacritics stripped) but map to different ids.
    (tmp_path / "lexicons" / "test.yaml").write_text(
        "test_grades:\n  ثِقَة: FIRST\n  ثقة: SECOND\n"
    )
    with pytest.raises(ConfigError) as exc_info:
        load_config(sol)
    assert "normalize" in str(exc_info.value)


def _minimal_sol_yaml(includes: list[str]) -> str:
    """Write a minimal-but-valid sol.yaml that only includes test shards."""
    includes_block = "".join(f"  - {p}\n" for p in includes)
    return (
        "__includes__:\n"
        + includes_block
        + "features:\n"
        "  rijal_enabled: false\n"
        "  translation_enabled: false\n"
        "  embedding_enabled: false\n"
        "thresholds: {}\n"
        "book_categories: [test-cat]\n"
        "phase_contracts:\n"
        "  ingest: {requires_completed: [], requires_fields_populated: [source_path],\n"
        "    produces_fields: [pages, title, author, category],\n"
        "    forbids_degraded: [], permits_degraded: []}\n"
        "  segment: {requires_completed: [ingest], requires_fields_populated: [pages],\n"
        "    produces_fields: [spans], forbids_degraded: [], permits_degraded: []}\n"
        "  extract: {requires_completed: [segment],\n"
        "    requires_fields_populated: [spans],\n"
        "    produces_fields: [entities, units], forbids_degraded: [],\n"
        "    permits_degraded: []}\n"
        "  enrich: {requires_completed: [extract],\n"
        "    requires_fields_populated: [entities, units],\n"
        "    produces_fields: [], forbids_degraded: [], permits_degraded: []}\n"
        "  graph: {requires_completed: [enrich],\n"
        "    requires_fields_populated: [entities],\n"
        "    produces_fields: [edges], forbids_degraded: [], permits_degraded: []}\n"
        "degraded_modes:\n"
        "  NER_UNAVAILABLE: {description: x, owner_phase: extract}\n"
        "  GAZETTEER_UNAVAILABLE: {description: x, owner_phase: extract}\n"
        "  RIJAL_UNAVAILABLE: {description: x, owner_phase: enrich}\n"
        "  TRANSLATION_FAILED: {description: x, owner_phase: enrich}\n"
        "  EMBEDDING_PARTIAL: {description: x, owner_phase: enrich}\n"
    )


def test_should_construct_lexicon_with_normalized_keys() -> None:
    """Lexicon dataclass stores entries keyed by normalized form."""
    entries = {
        "ثقه": LexiconEntry(
            surface_normalized="ثقه",
            surface_raw="ثقة",
            canonical_id="THIQA",
            source_file="<test>",
        ),
    }
    lex = Lexicon(registry_name="test", entries=entries)
    assert lex.lookup("ثقه") == "THIQA"
    assert lex.lookup("absent") is None
