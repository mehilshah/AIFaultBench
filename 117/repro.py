#!/usr/bin/env python3
"""Minimal reproduction for ClearML's Fire patching bug."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from clearml import Task  # noqa: F401  # Import triggers ClearML's Fire patching.
import fire


class Add:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, verbose: bool = False):
        res = self.x + self.y
        if verbose:
            print(f"x = {self.x}")
            print(f"y = {self.y}")
            print(f"x + y = {res}")
        return res


class Mult:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, verbose: bool = False):
        res = self.x * self.y
        if verbose:
            print(f"x = {self.x}")
            print(f"y = {self.y}")
            print(f"x * y = {res}")
        return res


if __name__ == "__main__":
    fire.Fire(
        {
            "add": Add,
            "multiply": Mult,
        }
    )
