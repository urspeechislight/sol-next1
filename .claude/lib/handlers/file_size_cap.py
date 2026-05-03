"""Cap file size — warn at 300 LOC, block at 500 LOC.

Why: large files are a smell that the file is doing too much. Splitting up
front pays back in review velocity and reuse.
"""

from __future__ import annotations

from ..context import HookContext
from ..decision import Decision

HANDLER = "file_size_cap"
WARN_LOC = 300
BLOCK_LOC = 500
DOC = "docs/quality-standards.md#size-caps"


def _line_count(content: str) -> int:
    """Count non-blank, non-pure-comment lines."""
    return sum(
        1
        for line in content.splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "//", "/*", "*"))
    )


def check(ctx: HookContext) -> Decision:
    """Warn / block based on file LOC."""
    if not ctx.is_write or ctx.new_content is None:
        return Decision.allow(HANDLER)
    if ctx.suffix not in {"py", "ts", "tsx", "js", "jsx", "svelte"}:
        return Decision.allow(HANDLER)

    loc = _line_count(ctx.new_content)
    if loc >= BLOCK_LOC:
        return Decision.deny(
            handler=HANDLER,
            rule_id="QUAL-010",
            why=f"File is {loc} LOC; cap is {BLOCK_LOC}.",
            fix="Split this file into smaller modules with focused responsibilities.",
            doc=DOC,
        )
    if loc >= WARN_LOC:
        return Decision.advise(
            handler=HANDLER,
            rule_id="QUAL-010",
            why=f"File is {loc} LOC; cap is {BLOCK_LOC}, soft limit {WARN_LOC}.",
            fix="Consider splitting before it exceeds the hard cap.",
            doc=DOC,
        )
    return Decision.allow(HANDLER)
