#!/usr/bin/env python3
"""Reproduce the MIRNet typo reported in keras-io issue #1160.

The bug is source-level: the second SKFF call in multi_scale_residual_block()
uses level3_dau_2 twice and never consumes level2_dau_2.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "examples" / "vision" / "mirnet.py"


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    lines = text.splitlines()

    level2_assignment = None
    skff_line = None
    for idx, line in enumerate(lines, start=1):
        if "level2_dau_2 =" in line:
            level2_assignment = (idx, line.rstrip())
        if "skff_ = selective_kernel_feature_fusion" in line:
            skff_line = (idx, line.rstrip())

    if level2_assignment is None or skff_line is None:
        print("Could not locate expected MIRNet source lines.", file=sys.stderr)
        return 2

    bug_present = (
        "level3_dau_2, level3_dau_2" in skff_line[1]
        and "level2_dau_2" not in skff_line[1]
    )
    level2_refs = len(re.findall(r"\blevel2_dau_2\b", text))
    level3_refs = len(re.findall(r"\blevel3_dau_2\b", text))

    print(f"Source file: {SOURCE}")
    print(f"level2_dau_2 assignment: line {level2_assignment[0]} -> {level2_assignment[1]}")
    print(f"SKFF call: line {skff_line[0]} -> {skff_line[1]}")
    print(f"Occurrences of level2_dau_2 in file: {level2_refs}")
    print(f"Occurrences of level3_dau_2 in file: {level3_refs}")

    if bug_present:
        print("BUG REPRODUCED: the final SKFF call ignores level2_dau_2 and reuses level3_dau_2 twice.")
        return 0

    print("BUG NOT REPRODUCED: the cited typo is not present in this source snapshot.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
