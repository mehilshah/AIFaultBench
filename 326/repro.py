#!/usr/bin/env python3
"""Reproduce the Pyro mypy missing-import regression."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    env = os.environ.copy()
    env.pop("MYPYPATH", None)

    try:
        import importlib.util

        spec = importlib.util.find_spec("pyro")
        if spec is None or spec.origin is None:
            print("pyro import spec: not found")
        else:
            pyro_init = Path(spec.origin).resolve()
            pyro_dir = pyro_init.parent
            print(f"pyro import spec: {pyro_init}")
            print(f"py.typed present: {(pyro_dir / 'py.typed').exists()}")
    except Exception as exc:  # pragma: no cover - diagnostic only
        print(f"failed to inspect pyro package: {exc}")

    with tempfile.TemporaryDirectory(prefix="bug326-mypy-") as tmpdir:
        check_path = Path(tmpdir) / "check_pyro.py"
        check_path.write_text(
            "\n".join(
                [
                    "import pyro",
                    "import pyro.distributions as dist",
                    "import pyro.infer",
                    "import pyro.infer.autoguide",
                    "import pyro.optim",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        cmd = [sys.executable, "-m", "mypy", str(check_path)]
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            env=env,
            text=True,
            capture_output=True,
        )

        if proc.stdout:
            sys.stdout.write(proc.stdout)
        if proc.stderr:
            sys.stderr.write(proc.stderr)

        expected = [
            'Cannot find implementation or library stub for module named "pyro"',
            'Cannot find implementation or library stub for module named "pyro.distributions"',
            'Cannot find implementation or library stub for module named "pyro.infer"',
            'Cannot find implementation or library stub for module named "pyro.infer.autoguide"',
            'Cannot find implementation or library stub for module named "pyro.optim"',
        ]
        if all(item in proc.stdout for item in expected):
            return 0

        print("did not reproduce the expected mypy import-not-found errors", file=sys.stderr)
        return proc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
