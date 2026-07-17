#!/usr/bin/env python3
"""Minimal reproduction for timm 1.0.18 on Python 3.9.

The bug is the import-time evaluation of this annotation in
codebase/timm/layers/typing.py:

    def nullwrap(fn: F | None = None):
"""

from pathlib import Path
from typing import Callable, TypeVar


def main() -> None:
    source = Path("codebase/timm/layers/typing.py").read_text(encoding="utf-8")
    for line in source.splitlines():
        if line.startswith("def nullwrap("):
            print(f"Source line: {line}")
            break

    F = TypeVar("F", bound=Callable[..., object])

    # Python 3.9 evaluates this annotation at function definition time and
    # raises: TypeError: unsupported operand type(s) for |: 'TypeVar' and 'NoneType'
    def nullwrap(fn: F | None = None):
        return fn

    print(nullwrap)


if __name__ == "__main__":
    main()
