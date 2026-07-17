#!/usr/bin/env python3
"""Reproduce the Vision Transformer CIFAR-10 num_classes default bug."""

from __future__ import annotations

import ast
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parent
TARGET = ROOT / "codebase" / "vision_transformer" / "main.py"


def find_num_classes_default(source: str) -> tuple[int | None, str | None]:
    tree = ast.parse(source, filename=str(TARGET))
    default_value = None
    help_text = None

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute) or func.attr != "add_argument":
            continue

        if not node.args:
            continue
        first_arg = node.args[0]
        if not isinstance(first_arg, ast.Constant) or first_arg.value != "--num-classes":
            continue

        for keyword in node.keywords:
            if keyword.arg == "default" and isinstance(keyword.value, ast.Constant):
                default_value = keyword.value.value
            elif keyword.arg == "help" and isinstance(keyword.value, ast.Constant):
                help_text = keyword.value.value

    return default_value, help_text


def main() -> int:
    source = TARGET.read_text(encoding="utf-8")
    default_value, help_text = find_num_classes_default(source)

    print(f"target_file={TARGET}")
    print(f"num_classes_default={default_value}")
    print(f"num_classes_help={help_text!r}")

    expected = 10
    if default_value != expected:
        print(
            f"BUG: expected default num_classes={expected} for CIFAR10, "
            f"but code sets {default_value}.",
            file=sys.stderr,
        )
        return 1

    print("No bug reproduced: default matches CIFAR10 expectation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
