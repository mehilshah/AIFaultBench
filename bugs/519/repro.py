#!/usr/bin/env python3
"""Reproduce the GraphGym import failure from the bug report.

This script builds an isolated sandbox package tree that mirrors the relevant
`torch_geometric.graphgym` layout but omits `imports.py`, which is the module
reported as missing.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def build_sandbox() -> Path:
    sandbox = Path(tempfile.mkdtemp(prefix="graphgym_repro_"))
    pkg_root = sandbox / "torch_geometric"
    graphgym_root = pkg_root / "graphgym"
    graphgym_src = CODEBASE / "torch_geometric" / "graphgym"

    pkg_root.mkdir(parents=True, exist_ok=True)
    graphgym_root.mkdir(parents=True, exist_ok=True)

    # Keep the package surface minimal so the repro does not depend on torch
    # or any other third-party package.
    (pkg_root / "__init__.py").write_text("", encoding="utf-8")
    # The real package's `graphgym/__init__.py` pulls in torch through a large
    # import tree. For this repro we only need the package path itself; making
    # the package initializer empty isolates the missing-submodule failure.
    (graphgym_root / "__init__.py").write_text("", encoding="utf-8")

    for path in graphgym_src.iterdir():
        if path.name in {"__init__.py", "imports.py"}:
            continue
        target = graphgym_root / path.name
        if path.is_dir():
            shutil.copytree(path, target)
        else:
            shutil.copy2(path, target)

    return sandbox


def main() -> int:
    sandbox = build_sandbox()
    sys.path.insert(0, str(sandbox))

    print(f"sandbox={sandbox}")
    print("expecting: ModuleNotFoundError: No module named 'torch_geometric.graphgym.imports'")

    try:
        from torch_geometric.graphgym.imports import pl  # noqa: F401
    except ModuleNotFoundError as exc:
        print(f"raised={exc.__class__.__name__}")
        print(f"message={exc}")
        return 0
    finally:
        # Leave the sandbox on disk for inspection if desired.
        pass

    print("unexpected: import succeeded")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
