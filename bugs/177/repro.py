#!/usr/bin/env python3
"""Minimal reproduction for class-level v_args(inline=True) on Visitor."""

from __future__ import annotations

import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

from lark import Lark, Transformer, Visitor  # noqa: E402
from lark.visitors import v_args  # noqa: E402


GRAMMAR = r"""
start: pair
pair: NUMBER NUMBER

%import common.NUMBER
%import common.WS
%ignore WS
"""


tree = Lark(GRAMMAR).parse("1 2")
print("parsed tree:", tree)


@v_args(inline=True)
class InlineTransformer(Transformer):
    def pair(self, left, right):
        print("transformer pair args:", left, right)
        return int(left) + int(right)

    def start(self, value):
        print("transformer start value:", value)
        return value


@v_args(inline=True)
class InlineVisitor(Visitor):
    def pair(self, left, right):
        print("visitor pair args:", left, right)


transform_result = InlineTransformer().transform(tree)
print("transform result:", transform_result)

print("visiting tree...")
InlineVisitor().visit(tree)
