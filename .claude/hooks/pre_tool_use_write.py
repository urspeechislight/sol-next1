#!/usr/bin/env python3
"""PreToolUse hook for Write|Edit|MultiEdit.

Runs cheap, content-only checks BEFORE the file is written. Anything that
needs the file on disk runs in the post-tool-use hook.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401

from lib import dispatcher
from lib.handlers import (
    docs_location,
    external_refs,
    file_size_cap,
    function_size_cap,
    import_boundaries,
    magic_numbers,
    no_arbitrary_values,
    no_inline_styles,
    no_print,
    no_raw_colors,
    no_silent_except,
    primitive_usage,
    secret_scanner,
    test_naming,
    typed_python,
    variants_only,
)


def main() -> None:
    """Run all PreToolUse:Write handlers in order."""
    dispatcher.run(
        event="PreToolUse:Write",
        handlers=[
            secret_scanner.check,
            external_refs.check,
            no_raw_colors.check,
            no_arbitrary_values.check,
            no_inline_styles.check,
            primitive_usage.check,
            variants_only.check,
            import_boundaries.check,
            no_silent_except.check,
            no_print.check,
            typed_python.check,
            magic_numbers.check,
            function_size_cap.check,
            file_size_cap.check,
            test_naming.check,
            docs_location.check,
        ],
    )


if __name__ == "__main__":
    main()
