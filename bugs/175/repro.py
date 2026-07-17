#!/usr/bin/env python3
import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

from lark import Lark, Transformer  # noqa: E402


GRAMMAR = r"""
?start: acos_func
?acos_func: ("acos" | "ACOS") "(" NUMBER ")"
NUMBER: /-?\d+(\.\d+)?/
%import common.WS
%ignore WS
"""


class MyTransformer(Transformer):
    def acos_func(self, args):
        return "ACOS called with argument: " + str(args[0])


def main():
    parser = Lark(GRAMMAR, parser="lalr", transformer=MyTransformer())
    result = parser.parse("ACOS(1.0)")

    print(f"result_type={type(result).__name__}")
    print(f"result_repr={result!r}")
    print(f"result_str={result}")
    expected = "ACOS called with argument: 1.0"
    print(f"expected={expected!r}")

    assert str(result) == expected, "Transformer callback was not applied"


if __name__ == "__main__":
    main()
