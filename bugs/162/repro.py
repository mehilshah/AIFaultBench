#!/usr/bin/env python3
"""Reproduce the missing Quay tag reported for jupyter/scipy-notebook."""

from __future__ import annotations

import subprocess
import sys


IMAGE = "quay.io/jupyter/scipy-notebook:hub-4.1.6"


def main() -> int:
    cmd = ["docker", "pull", IMAGE]
    print(f"Running: {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd, text=True, capture_output=True)

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)

    if proc.returncode == 0:
        print("Unexpected success: the image tag exists.", flush=True)
        return 1

    print(f"docker pull exited with {proc.returncode}", flush=True)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
