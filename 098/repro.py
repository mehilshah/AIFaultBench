#!/usr/bin/env python3
"""Minimal repro for SinusoidalPosEmb NameError.

This script executes the exact buggy class body from the local codebase and
calls forward() on a dummy input. The failure happens before any torch math,
so no third-party dependencies are needed for the reproduction.
"""

from __future__ import annotations

import math
import traceback
from dataclasses import dataclass
from pathlib import Path


CODEBASE_FILE = Path(__file__).resolve().parent / "codebase" / "denoising_diffusion_pytorch" / "denoising_diffusion_pytorch.py"


def extract_buggy_class_source(text: str) -> str:
    start_marker = "class SinusoidalPosEmb(nn.Module):"
    end_marker = "class RandomOrLearnedSinusoidalPosEmb(nn.Module):"
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[start:end].rstrip()


class _DummyModule:
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)


class _NNNamespace:
    Module = _DummyModule


@dataclass
class DummyInput:
    device: str = "cpu"


def main() -> int:
    source = CODEBASE_FILE.read_text()
    buggy_class_source = extract_buggy_class_source(source)

    print(f"Loaded buggy class from {CODEBASE_FILE}")
    print("Executing SinusoidalPosEmb.forward() with dummy input...")

    namespace = {
        "math": math,
        "nn": _NNNamespace(),
    }
    exec(buggy_class_source, namespace)

    emb = namespace["SinusoidalPosEmb"](dim=4)

    try:
        emb(DummyInput())
    except Exception as exc:  # noqa: BLE001 - we want the exact runtime failure
        traceback.print_exc()
        return 1 if isinstance(exc, NameError) and "theta" in str(exc) else 2

    print("Unexpected success: the bug did not reproduce.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
