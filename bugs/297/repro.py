#!/usr/bin/env python3
"""Reproduce the uv resolution failure reported for torch_geometric."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    cmd = ["uv", "sync", "--no-install-project"]
    print("Running:", " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
