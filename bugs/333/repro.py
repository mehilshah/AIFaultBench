#!/usr/bin/env python3
"""Deterministic repro for a tag-mutation report.

The bug report is about a force-pushed Git tag, so the only meaningful local
check is whether this standardized folder includes Git metadata that could
expose tag history.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
VERSION_FILE = CODEBASE / "src" / "version.info"


def read_snapshot_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def probe_git_metadata() -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(CODEBASE), "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True, completed.stdout.strip()
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        return False, message


def main() -> int:
    version = read_snapshot_version()
    has_git, git_status = probe_git_metadata()

    print("Bug report: GitHub tag immutability / force-push complaint")
    print(f"Local snapshot version: {version}")
    print(f"Git metadata present: {has_git}")
    print(f"Git probe output: {git_status}")

    if not has_git:
        print(
            "Result: not reproducible locally because this folder is not a Git checkout, "
            "so the tag history that the report refers to cannot be inspected here."
        )
        return 2

    print(
        "Result: a Git repository is present, but this bundle still does not replay the "
        "original remote force-push event."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
