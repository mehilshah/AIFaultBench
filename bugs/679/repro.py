#!/usr/bin/env python3
"""Reproduce camel-ai 0.2.85's Python-3.13 tiktoken installation failure."""

import os
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    if sys.version_info[:2] != (3, 13):
        raise AssertionError(f"expected Python 3.13, got {sys.version}")
    if shutil.which("rustc") is not None:
        raise AssertionError("expected no Rust compiler on the reference machine")

    # camel-ai at the pinned commit requires tiktoken>=0.7.0,<0.8.  Version
    # 0.7.0 has no CPython-3.13 wheel, so this normal pip install uses its
    # source distribution and hits the missing-Rust build failure.
    with tempfile.TemporaryDirectory(prefix="camel-tiktoken-repro-") as target:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-cache-dir",
                "--target",
                target,
                "tiktoken==0.7.0",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"},
        )

    expected = "can't find Rust compiler"
    if result.returncode == 0 or expected not in result.stdout:
        print("UNEXPECTED: tiktoken==0.7.0 did not fail with the missing-Rust build error")
        print(result.stdout)
        return 2

    pip_line = next(
        line.strip() for line in result.stdout.splitlines() if expected in line
    )
    print(f"OBSERVED: tiktoken==0.7.0 source build on Python 3.13 failed: {pip_line}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
