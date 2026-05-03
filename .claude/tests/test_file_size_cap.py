"""Tests for the file_size_cap handler."""

from __future__ import annotations

from pathlib import Path

from lib.context import HookContext
from lib.handlers import file_size_cap


def _ctx(content: str) -> HookContext:
    return HookContext(
        tool_name="Write",
        file_path=Path("/tmp/x.py").resolve(),
        command=None,
        new_content=content,
        old_content=None,
    )


def test_should_allow_when_file_is_small() -> None:
    """A 50-line file passes."""
    decision = file_size_cap.check(_ctx("line\n" * 50))
    assert decision.severity == "allow"


def test_should_advise_when_file_above_warn_cap() -> None:
    """A 350-line file emits an advisory but allows."""
    decision = file_size_cap.check(_ctx("x = 1\n" * 350))
    assert decision.severity == "advisory"


def test_should_block_when_file_above_hard_cap() -> None:
    """A 600-line file blocks."""
    decision = file_size_cap.check(_ctx("x = 1\n" * 600))
    assert decision.severity == "block"
    assert decision.rule_id == "QUAL-010"
