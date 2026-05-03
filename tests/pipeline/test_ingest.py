"""Phase 1 (INGEST) tests.

Covers contract enforcement, golden-path ingest of a real sample book, and
specific failure modes from ADR 0005's data-integrity stance (fail loudly,
no silent fallbacks).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.config import Config, load_config
from pipeline.contracts import PHASE_INGEST, validate_manuscript_for_phase
from pipeline.core.constants import ENTITY_NAMESPACE, make_id
from pipeline.core.exceptions import ContractError, PhaseError
from pipeline.models import Manuscript
from pipeline.phases.ingest import ingest

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "sol.yaml"
SAMPLE_BOOK_DIR = REPO_ROOT / "data" / "books"


@pytest.fixture(scope="module")
def config() -> Config:
    """Loaded pipeline config (module-scoped — read once, share across tests)."""
    return load_config(CONFIG_PATH)


@pytest.fixture
def sample_book_path() -> Path:
    """Path to a deterministically-chosen sample book under data/books/."""
    candidates = sorted((SAMPLE_BOOK_DIR / "sunni-tafsir").glob("*.json"))
    if not candidates:
        pytest.skip("no sample books under data/books/sunni-tafsir/")
    return candidates[0]


def _build_manuscript_for(book_path: Path) -> Manuscript:
    """Mimic the CLI bootstrap: read frontmatter for sol_id and build a stub."""
    raw = json.loads(book_path.read_text())
    sol_id = raw["frontmatter"]["sol_id"]
    return Manuscript(
        id=make_id("manuscript", sol_id),
        urn=f"urn:sol:book:{sol_id}",
        title="(pending ingest)",
        source_path=book_path,
    )


def test_should_load_config_from_yaml(config: Config) -> None:
    """Config loads with all five phase contracts and a non-empty book-categories registry."""
    expected_phases = {"ingest", "segment", "extract", "enrich", "graph"}
    assert set(config.phase_contracts.keys()) == expected_phases
    assert len(config.book_categories) > 0
    assert "sunni-tafsir" in config.book_categories
    assert config.features.rijal_enabled is False


def test_should_raise_contract_error_when_source_path_missing(config: Config) -> None:
    """Phase 1's input contract requires manuscript.source_path; absence raises."""
    manuscript = Manuscript(
        id=make_id("manuscript", "test-no-source"),
        urn="urn:sol:book:test-no-source",
        title="test",
    )
    with pytest.raises(ContractError):
        validate_manuscript_for_phase(manuscript, PHASE_INGEST, config)


def test_should_ingest_real_book_and_populate_pages(
    config: Config, sample_book_path: Path
) -> None:
    """Golden path: real sample book ingests into a populated Manuscript."""
    raw = json.loads(sample_book_path.read_text())
    book_id_str = str(raw["frontmatter"]["book_id"])
    expected_pages = len(raw["content"][book_id_str])

    manuscript = _build_manuscript_for(sample_book_path)
    result = ingest(manuscript, config)

    assert result is manuscript
    assert len(manuscript.pages) == expected_pages
    assert manuscript.title == raw["frontmatter"]["title"]
    assert manuscript.author == raw["frontmatter"]["author"]
    assert manuscript.category == raw["frontmatter"]["book_type"]
    assert PHASE_INGEST in manuscript.completed_phases
    for page in manuscript.pages:
        assert page.manuscript_id == manuscript.id
        assert isinstance(page.text, str)


def test_should_produce_deterministic_page_ids_when_run_twice(
    config: Config, sample_book_path: Path
) -> None:
    """Running ingest on the same input twice produces identical Page IDs (ADR 0005 §6)."""
    first = ingest(_build_manuscript_for(sample_book_path), config)
    second = ingest(_build_manuscript_for(sample_book_path), config)
    first_ids = [p.id for p in first.pages]
    second_ids = [p.id for p in second.pages]
    assert first_ids == second_ids
    assert first.id == second.id


def test_should_raise_phase_error_when_source_file_missing(config: Config) -> None:
    """A manuscript pointing at a non-existent file raises PhaseError, not silent skip."""
    missing = REPO_ROOT / "data" / "books" / "definitely_does_not_exist_xyz123.json"
    manuscript = Manuscript(
        id=make_id("manuscript", "missing-file-test"),
        urn="urn:sol:book:missing-file-test",
        title="test",
        source_path=missing,
    )
    with pytest.raises(PhaseError) as exc_info:
        ingest(manuscript, config)
    assert exc_info.value.phase == PHASE_INGEST


def test_should_raise_phase_error_when_book_type_unknown(
    config: Config, tmp_path: Path
) -> None:
    """A book whose frontmatter.book_type is not in the registry raises."""
    fake_book = tmp_path / "fake.json"
    fake_book.write_text(json.dumps({
        "frontmatter": {
            "sol_id": "FAKE0001",
            "book_id": 1,
            "title": "fake",
            "author": "fake",
            "book_type": "this-category-does-not-exist",
        },
        "content": {"1": []},
    }))
    manuscript = Manuscript(
        id=make_id("manuscript", "FAKE0001"),
        urn="urn:sol:book:FAKE0001",
        title="(pending)",
        source_path=fake_book,
    )
    with pytest.raises(PhaseError) as exc_info:
        ingest(manuscript, config)
    assert "book_type" in str(exc_info.value)


def test_should_use_frozen_entity_namespace() -> None:
    """ENTITY_NAMESPACE is frozen — regenerating it would invalidate every existing ID."""
    expected = "a37f29c7-8b2e-4d6f-9c1a-7e8b3f5d2a1c"
    assert str(ENTITY_NAMESPACE) == expected
