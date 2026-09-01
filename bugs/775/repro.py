#!/usr/bin/env python3
"""Minimal reproduction for lark-parser/lark issue #1570.

The bundled `python.lark` grammar cannot parse Python's parenthesized
`with` statement (multiple context managers wrapped in parentheses),
which has been valid syntax since Python 3.9/3.10 and is common in
Python 3.13 code:

    with (open("a.txt") as a,
          open("b.txt") as b):
        pass

The grammar rule:

    with_stmt: "with" with_items ":" suite
    with_items: with_item ("," with_item)*
    with_item: test ["as" name]

only accounts for a single, unparenthesized `test` per `with_item`, so
the lexer/parser rejects the "as" token as soon as it appears inside a
parenthesized group. This script reproduces that failure deterministically
using the grammar file shipped in this checkout of lark.
"""

from __future__ import annotations

import sys
from pathlib import Path

from lark import Lark, UnexpectedToken
from lark.indenter import PythonIndenter

ROOT = Path(__file__).resolve().parent
GRAMMAR_PATH = ROOT / "codebase" / "lark" / "grammars" / "python.lark"


def build_parser() -> Lark:
    return Lark.open(
        str(GRAMMAR_PATH),
        parser="lalr",
        postlex=PythonIndenter(),
        start="file_input",
    )


def main() -> int:
    parser = build_parser()

    # Sanity check: the non-parenthesized form must still parse fine.
    unparenthesized = 'with open("a.txt") as a, open("b.txt") as b:\n    pass\n'
    parser.parse(unparenthesized)
    print("unparenthesized with-statement: parsed OK")

    # The bug: valid Python 3.9+/3.13 parenthesized with-statement fails.
    parenthesized = (
        'with (open("a.txt") as a,\n'
        '      open("b.txt") as b):\n'
        "    pass\n"
    )
    try:
        parser.parse(parenthesized)
    except UnexpectedToken as e:
        print("parenthesized with-statement: FAILED as expected")
        print("error =", str(e).splitlines()[0])
        return 0

    raise SystemExit(
        "Expected UnexpectedToken while parsing the parenthesized with-statement; "
        "the grammar may have been fixed upstream."
    )


if __name__ == "__main__":
    raise SystemExit(main())
