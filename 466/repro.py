#!/usr/bin/env python3
"""Check whether the reported tag mention exists in the checked-out repo."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
REPORTED_USER_NEEDLES = ("@Blaizzy", "Blaizzy")
CONTEXT_NEEDLES = ("ethanwharris",)


def run_git_grep(pattern: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "git",
            "-C",
            str(CODEBASE),
            "grep",
            "-n",
            pattern,
            "--",
            ".github",
            "docs",
            "src",
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    print(f"Working directory: {ROOT}")
    print(f"Codebase path: {CODEBASE}")
    print()

    if not CODEBASE.exists():
        print("codebase/ is missing, so the repro cannot be evaluated.")
        return 2

    reported_hits = []
    context_hits = []
    for needle in REPORTED_USER_NEEDLES:
        result = run_git_grep(needle)
        if result.returncode == 0 and result.stdout.strip():
            for line in result.stdout.splitlines():
                reported_hits.append(line)

    for needle in CONTEXT_NEEDLES:
        result = run_git_grep(needle)
        if result.returncode == 0 and result.stdout.strip():
            for line in result.stdout.splitlines():
                context_hits.append(line)

    if reported_hits:
        print("Found the reported user name in the repo:")
        for line in reported_hits:
            print(line)
        print()
        print("This would be relevant to the report, but it is not the same as")
        print("the local Lightning state described in bug_report.txt.")
        reproducible = False
    else:
        print("No local @Blaizzy/Blaizzy mention exists in the checked-out repo.")
        reproducible = False

    if context_hits:
        print()
        print("Related non-repro context found for @ethanwharris:")
        for line in context_hits:
            print(line)

    print()
    print(f"reproducible={str(reproducible).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
