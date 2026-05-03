"""Project path helpers used by handlers.

Centralizes the rules for "what directory am I editing?" so handlers don't
duplicate path logic.
"""

from __future__ import annotations

from pathlib import Path

# The repo root. ``.claude/lib/paths.py`` -> ``.claude/lib`` -> ``.claude`` -> repo.
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def is_in(path: Path | None, *segments: str) -> bool:
    """True if ``path`` is inside any of the given repo-relative segments.

    Examples::

        is_in(p, "src/frontend/lib")           # one segment
        is_in(p, "src/backend", "src/pipeline") # any of several
    """
    if path is None:
        return False
    try:
        rel = path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return False
    rel_str = rel.as_posix()
    return any(rel_str.startswith(seg.rstrip("/") + "/") or rel_str == seg for seg in segments)


def relpath(path: Path | None) -> str:
    """Return the path relative to the repo root (or absolute string fallback)."""
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def is_design_token_file(path: Path | None) -> bool:
    """True if this path is the design tokens SSOT — these files may use raw colors."""
    return is_in(path, "src/frontend/lib/design-system/tokens.css") or is_in(
        path, "src/frontend/lib/design-system/internal"
    )
