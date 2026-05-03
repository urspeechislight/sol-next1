"""Hook dispatcher.

Reads a JSON payload from stdin, runs a chain of handlers, emits the first
deny (or all advisories), audits the result, and exits with code 0 (allow)
or 2 (block).

Used by every script under ``.claude/hooks/``::

    from harness_lib import dispatcher
    dispatcher.run(event="PreToolUse:Write", handlers=[ ... ])
"""

from __future__ import annotations

import json
import sys
import traceback
from collections.abc import Callable
from typing import Any

from . import audit
from .context import HookContext
from .decision import Decision, emit_advisory, emit_block

Handler = Callable[[HookContext], Decision]


def _read_payload() -> dict[str, Any]:
    """Read the stdin JSON payload. On any failure, return an empty dict."""
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def run(*, event: str, handlers: list[Handler]) -> None:
    """Execute the handler chain. Exits the process when done.

    Order of operations:
      1. Read payload.
      2. Build :class:`HookContext`.
      3. Run handlers in order. First block wins. Advisories accumulate.
      4. Audit the decision set.
      5. Emit advisories (if any), then block (if any), then exit.
    """
    payload = _read_payload()
    ctx = HookContext.from_payload(payload)

    decisions: list[Decision] = []
    block: Decision | None = None

    for handler in handlers:
        try:
            verdict = handler(ctx)
        except Exception:  # noqa: BLE001  — handler crashes are fail-closed
            tb = traceback.format_exc(limit=3).strip().splitlines()[-1]
            verdict = Decision.deny(
                handler=getattr(handler, "__name__", "unknown"),
                rule_id="HARNESS-CRASH",
                why=f"Handler raised: {tb}",
                fix="File a bug — handlers must never crash. The harness fails closed.",
            )
        decisions.append(verdict)
        if verdict.is_block():
            block = verdict
            break

    # Emit advisories first so the user sees them even if a deny follows.
    for d in decisions:
        if d.is_advisory():
            emit_advisory(d)

    audit.append(
        event=event,
        tool_name=ctx.tool_name,
        payload=payload,
        decisions=decisions,
        blocked=block is not None,
    )

    if block is not None:
        emit_block(block)

    sys.exit(0)
