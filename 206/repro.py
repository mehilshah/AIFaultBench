#!/usr/bin/env python3
"""Reproduce the POT unbalanced Sinkhorn regression from issue #691."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODE_SNIPPET = r"""
import numpy as np
import ot

a = [.5, .5]
b = [.5, .5]
M = [[0., 1.], [1., 0.]]
print("POT", ot.__version__)
print(np.array2string(ot.unbalanced.sinkhorn_knopp_unbalanced(a, b, M, 1., 1.), precision=8))
"""


def run_cmd(cmd, *, env=None, cwd=None):
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout.strip()


def matrix_only(output: str) -> str:
    lines = [line for line in output.splitlines() if line.strip()]
    return "\n".join(lines[1:])


def create_venv_and_run(version: str) -> str:
    with tempfile.TemporaryDirectory(prefix=f"pot_{version}_") as tmpdir:
        tmp = Path(tmpdir)
        venv_dir = tmp / "venv"
        run_cmd([sys.executable, "-m", "venv", str(venv_dir)], cwd=ROOT)
        python_bin = venv_dir / "bin" / "python"
        pip_bin = venv_dir / "bin" / "pip"
        run_cmd([str(pip_bin), "install", "--upgrade", "pip", "setuptools", "wheel"], cwd=ROOT)
        run_cmd(
            [
                str(pip_bin),
                "install",
                "numpy==1.26.4",
                "scipy==1.13.1",
                f"POT=={version}",
            ],
            cwd=ROOT,
        )
        return run_cmd([str(python_bin), "-c", CODE_SNIPPET], cwd=ROOT)


def run_local_checkout() -> str:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "codebase")
    return run_cmd([sys.executable, "-c", CODE_SNIPPET], env=env, cwd=ROOT)


def main() -> int:
    local_output = run_local_checkout()
    out_094 = create_venv_and_run("0.9.4")
    out_095 = create_venv_and_run("0.9.5")

    print("Local checkout output:")
    print(local_output)
    print()
    print("POT 0.9.4 output:")
    print(out_094)
    print()
    print("POT 0.9.5 output:")
    print(out_095)
    print()
    print("0.9.4 == 0.9.5:", out_094 == out_095)
    print("local matrix == 0.9.5 matrix:", matrix_only(local_output) == matrix_only(out_095))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
