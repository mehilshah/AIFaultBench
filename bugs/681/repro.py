#!/usr/bin/env python3
"""Reproduce mem0-cli's crashes on explicit null memory fields."""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "codebase" / "cli" / "python" / "src"))

from rich.console import Console
from mem0_cli.output import format_memories_table, format_memories_text


RECORDS = [{"id": None, "memory": None, "created_at": None, "categories": None}]


def expect_null_crash(name: str, formatter: object, expected_message: str) -> str:
    try:
        formatter(Console(file=io.StringIO(), force_terminal=False), RECORDS)  # type: ignore[operator]
    except TypeError as exc:
        assert str(exc) == expected_message, f"{name} raised unexpected TypeError: {exc!s}"
        return f"{name}: TypeError: {exc}"
    except Exception as exc:
        raise AssertionError(f"{name} raised unexpected {type(exc).__name__}: {exc}") from exc
    raise AssertionError(f"{name} accepted explicit null fields; the bug is not present")


def main() -> None:
    observations = [
        expect_null_crash(
            "format_memories_text",
            format_memories_text,
            "'NoneType' object is not subscriptable",
        ),
        expect_null_crash(
            "format_memories_table",
            format_memories_table,
            "object of type 'NoneType' has no len()",
        ),
    ]
    print("BUG REPRODUCED: " + "; ".join(observations))
    raise SystemExit(1)


if __name__ == "__main__":
    main()
