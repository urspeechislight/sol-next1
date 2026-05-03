#!/usr/bin/env python3
"""SessionStart hook.

Prints a brief banner reminding the agent of the rules and pointing at the
docs. Exits 0 — never blocks. The banner content is short by design; the
authoritative rules live in ``CLAUDE.md`` and ``docs/quality-standards.md``.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401 — runs the Python version check
import sys

BANNER = """
╭─ sol-next1 harness active ──────────────────────────────────────────────╮
│  · Design tokens are SSOT (src/frontend/lib/design-system/tokens.css)   │
│  · No raw colors / inline styles / ad-hoc variant maps                  │
│  · Routes use design-system primitives, not raw <button>/<input>        │
│  · All docs go in docs/                                                 │
│  · See CLAUDE.md and docs/quality-standards.md for the full ruleset     │
╰─────────────────────────────────────────────────────────────────────────╯
""".strip()


def main() -> None:
    """Print the banner and exit 0."""
    print(BANNER, file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
