"""Tool-call context: typed view of the JSON payload passed via stdin.

Claude Code dispatches hooks with a JSON payload like::

    {
      "session_id": "...",
      "tool_name": "Edit",
      "tool_input": {"file_path": "/a/b/foo.svelte", "old_string": "...", "new_string": "..."},
      "tool_response": null
    }

Handlers receive a :class:`HookContext` constructed from this payload.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class HookContext:
    """Normalized view of a tool-call payload."""

    tool_name: str
    file_path: Path | None
    command: str | None
    new_content: str | None
    old_content: str | None
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def suffix(self) -> str:
        """File extension without the leading dot, lowercase."""
        return self.file_path.suffix.lstrip(".").lower() if self.file_path else ""

    @property
    def is_write(self) -> bool:
        """True if this is a Write/Edit/MultiEdit operation."""
        return self.tool_name in {"Write", "Edit", "MultiEdit"} and self.file_path is not None

    @property
    def is_bash(self) -> bool:
        """True if this is a Bash command."""
        return self.tool_name == "Bash" and self.command is not None

    @staticmethod
    def from_payload(payload: dict[str, Any]) -> HookContext:
        """Construct a HookContext from the raw stdin payload."""
        tool_name = str(payload.get("tool_name", ""))
        tool_input = payload.get("tool_input", {}) or {}
        if not isinstance(tool_input, dict):
            tool_input = {}
        fp_raw = tool_input.get("file_path")
        file_path = Path(fp_raw).resolve() if isinstance(fp_raw, str) and fp_raw else None
        command = tool_input.get("command") if isinstance(tool_input.get("command"), str) else None

        new_content: str | None = None
        if tool_name == "Write":
            content = tool_input.get("content")
            if isinstance(content, str):
                new_content = content
        elif tool_name == "Edit":
            new_string = tool_input.get("new_string")
            if isinstance(new_string, str):
                new_content = new_string
        elif tool_name == "MultiEdit":
            edits = tool_input.get("edits")
            if isinstance(edits, list):
                pieces = [e.get("new_string", "") for e in edits if isinstance(e, dict)]
                new_content = "\n".join(p for p in pieces if isinstance(p, str))

        old_content: str | None = None
        if tool_name == "Edit":
            old = tool_input.get("old_string")
            if isinstance(old, str):
                old_content = old

        return HookContext(
            tool_name=tool_name,
            file_path=file_path,
            command=command,
            new_content=new_content,
            old_content=old_content,
            raw=payload,
        )
