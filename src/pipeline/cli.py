"""CLI entry point for the pipeline.

Run a book through Phase 1:

    python -m src.pipeline.cli run path/to/book.json --config config/sol.yaml

The CLI is the boundary that creates the initial Manuscript from a path,
loads config, and dispatches phase functions in order. Phase functions
themselves take a Manuscript (per ADR 0005 §1) — the path-to-Manuscript
bootstrap lives here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import structlog

from pipeline.config import load_config
from pipeline.core.constants import make_id
from pipeline.core.exceptions import PipelineError
from pipeline.models import Manuscript
from pipeline.phases.ingest import ingest

DEFAULT_CONFIG_PATH = Path("config/sol.yaml")
EXIT_SUCCESS = 0
EXIT_PIPELINE_ERROR = 1
EXIT_UNEXPECTED = 2


def _configure_logging() -> None:
    """Configure structlog for human-readable CLI output."""
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
        ]
    )


def bootstrap_manuscript(book_path: Path) -> Manuscript:
    """Build a Manuscript stub from a book file path with deterministic id and urn.

    Reads only the frontmatter to derive identity (sol_id is the stable handle).
    Phase 1 (INGEST) re-reads the full file to populate pages and metadata.
    """
    parsed: object = json.loads(book_path.read_text())
    if not isinstance(parsed, dict):
        raise PipelineError(f"book file at {book_path} has no JSON object root")
    raw: dict[str, object] = {str(k): v for k, v in parsed.items()}  # type: ignore[misc]
    frontmatter_raw: object = raw.get("frontmatter", {})
    if not isinstance(frontmatter_raw, dict):
        raise PipelineError(f"book file at {book_path} frontmatter is not a mapping")
    frontmatter: dict[str, object] = {str(k): v for k, v in frontmatter_raw.items()}  # type: ignore[misc]
    sol_id = frontmatter.get("sol_id")
    if not isinstance(sol_id, str) or not sol_id:
        raise PipelineError(f"book file at {book_path} has no frontmatter.sol_id")
    raw_title = frontmatter.get("title")
    title: str = raw_title if isinstance(raw_title, str) and raw_title else "(untitled)"
    return Manuscript(
        id=make_id("manuscript", sol_id),
        urn=f"urn:sol:book:{sol_id}",
        title=title,
        source_path=book_path,
    )


def run(book_path: Path, config_path: Path) -> int:
    """Run a single book through Phase 1 (INGEST). Returns CLI exit code."""
    log = structlog.get_logger()
    config = load_config(config_path)
    manuscript = bootstrap_manuscript(book_path)
    manuscript = ingest(manuscript, config)
    log.info(
        "ingest_complete",
        urn=manuscript.urn,
        pages=len(manuscript.pages),
        category=manuscript.category,
        author=manuscript.author,
        title=manuscript.title,
        completed_phases=sorted(manuscript.completed_phases),
    )
    return EXIT_SUCCESS


def main(argv: list[str] | None = None) -> int:
    """Argparse-based entry point. Subcommands: `run`."""
    _configure_logging()
    parser = argparse.ArgumentParser(prog="sol-pipeline", description="sol-next1 pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run_p = sub.add_parser("run", help="ingest a single book through Phase 1")
    run_p.add_argument("book_path", type=Path, help="path to a book JSON file")
    run_p.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH, help="config/sol.yaml")
    args = parser.parse_args(argv)

    log = structlog.get_logger()
    try:
        if args.cmd == "run":
            return run(args.book_path, args.config)
    except PipelineError as exc:
        log.exception("pipeline_error", error=str(exc), kind=type(exc).__name__)
        return EXIT_PIPELINE_ERROR
    except Exception as exc:
        log.exception("unexpected_error", error=str(exc), kind=type(exc).__name__)
        return EXIT_UNEXPECTED
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
