"""Phase 1: INGEST — JSON book file → normalized Manuscript with Pages.

Per ADR 0005 §3 (purity):
  Does: parse JSON, populate manuscript.pages, populate manuscript.title /
        author / category from frontmatter.
  Does NOT: span analysis, entity extraction, embedding, graph writes.

TOC parsing into HierarchyPath roots is deferred to Phase 2; the source TOC
remains readable from the source file when SEGMENT needs it. Phase 1 stays
narrow.

The phase reads from manuscript.source_path; on success populates pages and
adds 'ingest' to completed_phases via validate_manuscript_after_phase.
"""

from __future__ import annotations

import json

from pipeline.config import Config
from pipeline.contracts import (
    PHASE_INGEST,
    validate_manuscript_after_phase,
    validate_manuscript_for_phase,
)
from pipeline.core.constants import make_id
from pipeline.core.exceptions import PhaseError
from pipeline.models import Manuscript, Page


def ingest(manuscript: Manuscript, config: Config) -> Manuscript:
    """Run Phase 1: parse the book file at manuscript.source_path, populate pages.

    Per ADR 0005 §1, the input Manuscript carries identity (id, urn, title,
    source_path); this phase populates pages and metadata fields from the
    book's frontmatter and content blocks.
    """
    validate_manuscript_for_phase(manuscript, PHASE_INGEST, config)

    if manuscript.source_path is None:
        raise PhaseError(PHASE_INGEST, "manuscript.source_path is required")

    if not manuscript.source_path.exists():
        raise PhaseError(
            PHASE_INGEST,
            "source file not found",
            path=str(manuscript.source_path),
        )

    try:
        parsed: object = json.loads(manuscript.source_path.read_text())
    except json.JSONDecodeError as exc:
        raise PhaseError(
            PHASE_INGEST,
            "JSON parse failed",
            path=str(manuscript.source_path),
            cause=str(exc),
        ) from exc

    if not isinstance(parsed, dict) or "frontmatter" not in parsed or "content" not in parsed:
        raise PhaseError(
            PHASE_INGEST,
            "missing required keys 'frontmatter' or 'content'",
            path=str(manuscript.source_path),
        )
    raw: dict[str, object] = {str(k): v for k, v in parsed.items()}  # type: ignore[misc]
    frontmatter_raw = raw["frontmatter"]
    if not isinstance(frontmatter_raw, dict):
        raise PhaseError(PHASE_INGEST, "'frontmatter' is not a mapping")
    frontmatter: dict[str, object] = {str(k): v for k, v in frontmatter_raw.items()}  # type: ignore[misc]

    _populate_metadata(manuscript, frontmatter, config)
    _populate_pages(manuscript, frontmatter, raw["content"])

    validate_manuscript_after_phase(manuscript, PHASE_INGEST, config)
    return manuscript


def _populate_metadata(
    manuscript: Manuscript, frontmatter: dict[str, object], config: Config
) -> None:
    """Set title, author, category on the manuscript from frontmatter."""
    title = frontmatter.get("title")
    if not isinstance(title, str) or not title:
        raise PhaseError(PHASE_INGEST, "frontmatter.title is missing or empty")
    manuscript.title = title

    author = frontmatter.get("author")
    if not isinstance(author, str) or not author:
        raise PhaseError(PHASE_INGEST, "frontmatter.author is missing or empty")
    manuscript.author = author

    category = frontmatter.get("book_type")
    if not isinstance(category, str) or not category:
        raise PhaseError(PHASE_INGEST, "frontmatter.book_type is missing or empty")
    if category not in config.book_categories:
        raise PhaseError(
            PHASE_INGEST,
            f"unknown book_type: {category!r}",
            path=str(manuscript.source_path),
        )
    manuscript.category = category


def _populate_pages(
    manuscript: Manuscript, frontmatter: dict[str, object], content_block: object
) -> None:
    """Build Page records from the content block, keyed under frontmatter.book_id."""
    book_id = frontmatter.get("book_id")
    if book_id is None:
        raise PhaseError(PHASE_INGEST, "frontmatter.book_id is missing")
    book_id_str = str(book_id)

    sol_id = frontmatter.get("sol_id")
    if not isinstance(sol_id, str) or not sol_id:
        raise PhaseError(PHASE_INGEST, "frontmatter.sol_id is missing or empty")

    if not isinstance(content_block, dict):
        raise PhaseError(PHASE_INGEST, "'content' is not a mapping")
    content: dict[str, object] = {str(k): v for k, v in content_block.items()}  # type: ignore[misc]

    pages_raw = content.get(book_id_str)
    if pages_raw is None:
        raise PhaseError(
            PHASE_INGEST,
            f"content section has no entry for book_id {book_id_str!r}",
            keys=sorted(content.keys()),
        )
    if not isinstance(pages_raw, list):
        raise PhaseError(PHASE_INGEST, f"content[{book_id_str!r}] is not a list")
    pages_list: list[object] = list(pages_raw)  # type: ignore[arg-type]

    for index, page_raw in enumerate(pages_list):
        if not isinstance(page_raw, dict):
            raise PhaseError(PHASE_INGEST, f"content page #{index} is not a mapping")
        page_dict: dict[str, object] = {str(k): v for k, v in page_raw.items()}  # type: ignore[misc]
        page_number = page_dict.get("page_number")
        if not isinstance(page_number, int):
            raise PhaseError(
                PHASE_INGEST,
                f"content page #{index} missing or non-integer page_number",
            )
        text = page_dict.get("content", "")
        footnote = page_dict.get("footnote")
        page = Page(
            id=make_id("page", sol_id, str(page_number), str(index)),
            manuscript_id=manuscript.id,
            page_number=page_number,
            text=text if isinstance(text, str) else "",
            footnote_text=footnote if isinstance(footnote, str) else None,
        )
        manuscript.pages.append(page)
