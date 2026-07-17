#!/usr/bin/env python3
"""Minimal reproduction harness for bug 288."""

from __future__ import annotations

import importlib
import pathlib
import sys
import traceback


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
VIDEO_FILE = CODEBASE / "vllm" / "multimodal" / "video.py"


def show_video_guard() -> None:
    print(f"video file: {VIDEO_FILE}")
    for line_no, line in enumerate(VIDEO_FILE.read_text().splitlines(), start=1):
        if 34 <= line_no <= 39:
            print(f"{line_no:4d}: {line}")


def try_import(name: str) -> None:
    print(f"\n== import {name} ==")
    try:
        mod = importlib.import_module(name)
        print(f"OK: {name} -> {getattr(mod, '__file__', '<builtin>')}")
    except Exception as exc:  # pragma: no cover - exercised in repro runs
        print(f"FAIL: {name}: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        raise


def main() -> int:
    show_video_guard()

    print(f"\npython: {sys.version}")
    print(f"sys.path[0]: {sys.path[0]}")

    failures = 0

    try:
        try_import("torchcodec")
    except Exception:
        failures += 1

    try:
        try_import("torchcodec.decoders")
    except Exception:
        failures += 1

    sys.path.insert(0, str(CODEBASE))
    try:
        try_import("vllm.multimodal.video")
    except Exception:
        failures += 1

    if failures:
        print(f"\nrepro status: blocked ({failures} failing import path(s))")
        return 1

    print("\nrepro status: no failure observed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
