#!/usr/bin/env python3
"""Minimal reproduction for the broken license badge link.

This script checks that the README badge targets `LICENCE` while the
repository only contains `LICENSE`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
FILES = [CODEBASE / "README.md", CODEBASE / "README_zh-CN.md"]


def extract_license_targets(readme_path: Path) -> List[str]:
    text = readme_path.read_text(encoding="utf-8")
    targets = re.findall(r"\]\(([^)]+)\)", text)
    return [target for target in targets if target.upper() in {"LICENCE", "LICENSE"}]


def main() -> int:
    summary: List[Tuple[str, List[str]]] = []
    broken = []
    for readme in FILES:
        targets = extract_license_targets(readme)
        summary.append((readme.name, targets))
        if "LICENCE" in targets and not (CODEBASE / "LICENCE").exists():
            broken.append(readme.name)

    payload = {
        "expected_file": "LICENSE",
        "missing_file": "LICENCE",
        "readme_targets": {name: targets for name, targets in summary},
        "repository_files": sorted(p.name for p in CODEBASE.iterdir() if p.is_file() and p.name.startswith("LICEN")),
        "reproducible": bool(broken),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))

    if broken:
        print(
            "BUG REPRODUCED: README badge links point to LICENCE, but the repository only contains LICENSE."
        )
        return 1

    print("No reproduction: the badge targets are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
