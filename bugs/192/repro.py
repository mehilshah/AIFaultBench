#!/usr/bin/env python3
"""Reproduce the Real-IAD category mismatch from the bug report.

The bug is static: the hard-coded CATEGORIES tuple in
`codebase/src/anomalib/data/datasets/image/realiad.py` does not match the
category list published in the Real-IAD Hugging Face dataset card quoted in the
report.
"""

from __future__ import annotations

import ast
import difflib
import sys
from pathlib import Path


EXPECTED_CATEGORIES = (
    "audiojack",
    "bottle_cap",
    "button_battery",
    "end_cap",
    "eraser",
    "fire_hood",
    "mint",
    "mounts",
    "pcb",
    "phone_battery",
    "plastic_nut",
    "plastic_plug",
    "porcelain_doll",
    "regulator",
    "rolled_strip_base",
    "sim_card_set",
    "switch",
    "tape",
    "terminalblock",
    "toothbrush",
    "toy",
    "toy_brick",
    "transistor1",
    "u_block",
    "usb",
    "usb_adaptor",
    "vcpill",
    "wooden_beads",
    "woodstick",
    "zipper",
)


def load_categories(source_path: Path) -> tuple[str, ...]:
    """Extract the CATEGORIES tuple directly from the source file."""

    module = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "CATEGORIES" for target in node.targets):
            continue
        value = ast.literal_eval(node.value)
        if not isinstance(value, tuple) or not all(isinstance(item, str) for item in value):
            msg = f"Unexpected CATEGORIES value in {source_path}"
            raise TypeError(msg)
        return value
    msg = f"CATEGORIES assignment not found in {source_path}"
    raise LookupError(msg)


def main() -> int:
    root = Path(__file__).resolve().parent
    source_path = root / "codebase" / "src" / "anomalib" / "data" / "datasets" / "image" / "realiad.py"
    actual_categories = load_categories(source_path)

    print(f"Source file: {source_path}")
    print(f"Actual category count: {len(actual_categories)}")
    print(f"Expected category count: {len(EXPECTED_CATEGORIES)}")
    print("Actual categories:")
    print(actual_categories)
    print("Expected categories:")
    print(EXPECTED_CATEGORIES)

    if actual_categories == EXPECTED_CATEGORIES:
        print("No mismatch detected.")
        return 0

    print("Mismatch detected.")
    print("Unified diff:")
    diff = difflib.unified_diff(
        [f"{category}\n" for category in actual_categories],
        [f"{category}\n" for category in EXPECTED_CATEGORIES],
        fromfile="actual",
        tofile="expected",
        lineterm="",
    )
    for line in diff:
        print(line)

    missing = [category for category in EXPECTED_CATEGORIES if category not in actual_categories]
    extra = [category for category in actual_categories if category not in EXPECTED_CATEGORIES]
    print(f"Missing from source: {missing}")
    print(f"Extra in source: {extra}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
