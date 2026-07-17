#!/usr/bin/env python3
"""Reproduce the non-deterministic parse tree selection from the bug report."""

from __future__ import annotations

import collections
import os
import subprocess
import sys
from pathlib import Path


GRAMMAR = r'''
start: factor+

?factor: atom quantifier?

quantifier: "*" | "+" | "?"

?atom: DOT | printable_char

printable_char: /[ -~]/

DOT: "."
'''

INPUT = r"a.?"


def run_once(repo_root: Path) -> str:
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH", "")
    codebase_path = str(repo_root / "codebase")
    env["PYTHONPATH"] = codebase_path if not pythonpath else f"{codebase_path}:{pythonpath}"
    env.pop("PYTHONHASHSEED", None)

    script = f"""
from lark import Lark

parser = Lark({GRAMMAR!r})
print(parser.parse({INPUT!r}).pretty(), end="")
"""

    proc = subprocess.run(
        [sys.executable, "-c", script],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    attempts = 40
    counts: collections.Counter[str] = collections.Counter()

    for _ in range(attempts):
        counts[run_once(repo_root)] += 1

    print(f"attempts: {attempts}")
    print(f"unique_trees: {len(counts)}")
    for idx, (tree, count) in enumerate(counts.items(), start=1):
        print(f"tree_{idx}_count: {count}")
        print(tree, end="" if tree.endswith("\n") else "\n")
        if not tree.endswith("\n"):
            print()

    if len(counts) < 2:
        print("result: not reproduced")
        return 1

    print("result: reproduced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
