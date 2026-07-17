#!/usr/bin/env python3
import os
import sys
import traceback


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

from lark import Lark  # noqa: E402


GRAMMAR = r"""
start: char+
char: /(?s)./
"""


def main() -> int:
    parser = Lark(GRAMMAR, lexer="basic")
    print("constructed parser")
    try:
        tokens = list(parser.lex("\n"))
        print(tokens)
        return 0
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
