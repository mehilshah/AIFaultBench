#!/usr/bin/env python3
"""Minimal reproduction harness for a documentation-only diffusers issue."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent


def main() -> int:
    bug_report = (ROOT / "bug_report.txt").read_text(encoding="utf-8")
    codebase = ROOT / "codebase"

    print("Bug 465 repro harness")
    print(f"bug_report.txt present: {(ROOT / 'bug_report.txt').exists()}")
    print(f"codebase/ present: {codebase.exists()}")
    print("issue states reproduction is N/A:", "N/A: This is a documentation-only improvement." in bug_report)

    if not codebase.exists():
        print("No executable source tree is available in this standardized folder.")
        print("This issue is documentation-only, so there is no runtime failure to trigger.")
        return 0

    target = codebase / "src" / "diffusers" / "schedulers" / "scheduling_euler_discrete.py"
    print(f"target file present: {target.exists()}")
    if target.exists():
        text = target.read_text(encoding="utf-8", errors="replace")
        if "typo" in text.lower():
            print("source contains a docstring typo-related string; verify manually")
        else:
            print("target file found, but the current text does not show an obvious typo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
