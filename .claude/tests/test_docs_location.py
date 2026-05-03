"""Tests for the docs_location handler."""

from __future__ import annotations

from pathlib import Path

from lib import paths
from lib.context import HookContext
from lib.handlers import docs_location


def _ctx(file_path: Path, content: str = "# x") -> HookContext:
    return HookContext(
        tool_name="Write",
        file_path=file_path.resolve(),
        command=None,
        new_content=content,
        old_content=None,
    )


def test_should_allow_when_writing_to_docs_dir(tmp_path: Path, monkeypatch) -> None:
    """Files inside docs/ pass."""
    repo = tmp_path / "repo"
    target = repo / "docs/architecture.md"
    target.parent.mkdir(parents=True)
    monkeypatch.setattr(paths, "REPO_ROOT", repo)
    assert docs_location.check(_ctx(target)).severity == "allow"


def test_should_allow_root_readme(tmp_path: Path, monkeypatch) -> None:
    """Root README.md is allowed (entry point)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.setattr(paths, "REPO_ROOT", repo)
    assert docs_location.check(_ctx(repo / "README.md")).severity == "allow"


def test_should_block_when_md_in_lib(tmp_path: Path, monkeypatch) -> None:
    """A README inside lib/ is rejected — must move to docs/."""
    repo = tmp_path / "repo"
    target = repo / "src/frontend/lib/design-system/README.md"
    target.parent.mkdir(parents=True)
    monkeypatch.setattr(paths, "REPO_ROOT", repo)
    assert docs_location.check(_ctx(target)).severity == "block"
