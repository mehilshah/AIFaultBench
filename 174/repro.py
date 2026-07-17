#!/usr/bin/env python3
"""Minimal reproduction for Lark issue 1355."""

from __future__ import annotations

import sys
from pathlib import Path


GRAMMAR = r'''
start: pipesyn
pipesyn: ["any"i ("c"i ("a"i ("s"i ("e"i)? )? )? )? -> anycase]
 | [("mixed"i
 | "one"i ("s"i)?
 | "zero"i ("s"i)?) -> mask]
 | ["anyo"i ("f"i)? -> anyof]
'''


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(repo_root / "codebase"))

    import lark  # noqa: WPS433

    print(f"lark version: {lark.__version__}")
    print("loading grammar from issue 1355")
    try:
        lark.Lark(GRAMMAR, parser="lalr")
    except Exception as exc:  # noqa: BLE001
        print(type(exc).__name__)
        print(exc)
        print("BUG REPRODUCED")
        return 1

    print("BUG NOT REPRODUCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
