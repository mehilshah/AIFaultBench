#!/usr/bin/env python3
"""Source-based reproduction for the torch_compile tutorial timing helper bug."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
TUTORIAL = ROOT / "codebase" / "intermediate_source" / "torch_compile_tutorial.py"
FIXED_EXAMPLE = ROOT / "codebase" / "intermediate_source" / "torch_compile_full_example.py"


def find_line_number(text: str, needle: str) -> int:
    for idx, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return idx
    raise ValueError(f"Missing line containing: {needle!r}")


def main() -> int:
    tutorial_text = TUTORIAL.read_text(encoding="utf-8")
    fixed_text = FIXED_EXAMPLE.read_text(encoding="utf-8")

    bad_line = "return result, start.elapsed_time(end) / 1024"
    good_line = "return result, start.elapsed_time(end) / 1000"

    tutorial_line_no = find_line_number(tutorial_text, bad_line)
    fixed_line_no = find_line_number(fixed_text, good_line)

    elapsed_ms = 1024.0
    reported_seconds = elapsed_ms / 1024.0
    expected_seconds = elapsed_ms / 1000.0
    delta = expected_seconds - reported_seconds

    print("Tutorial helper line:", f"{TUTORIAL}:{tutorial_line_no}")
    print("Fixed example line:", f"{FIXED_EXAMPLE}:{fixed_line_no}")
    print("Tutorial helper source:", bad_line)
    print("Corrected helper source:", good_line)
    print("Example event duration:", f"{elapsed_ms:.1f} ms")
    print("Tutorial helper reports:", f"{reported_seconds:.3f} s")
    print("Correct value is:", f"{expected_seconds:.3f} s")
    print("Absolute error:", f"{delta:.3f} s")

    if bad_line not in tutorial_text:
        print("Expected bug is missing from the tutorial source.")
        return 1

    if good_line not in fixed_text:
        print("Expected fixed helper is missing from the comparison example.")
        return 1

    if abs(reported_seconds - expected_seconds) < 1e-12:
        print("Unexpectedly, dividing by 1024 matches the correct seconds value.")
        return 1

    print("Result: reproducible.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
