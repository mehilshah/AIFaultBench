#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PYTHON = ROOT / ".venv" / "bin" / "python"


def run(cmd: list[str], *, env: dict[str, str]) -> int:
    print(f"$ {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd, cwd=ROOT, env=env)
    return proc.returncode


def main() -> int:
    env = os.environ.copy()
    env["JAX_CHECK_TRACER_LEAKS"] = "1"
    env.setdefault("PYTHONUNBUFFERED", "1")

    pytest_targets = [
        "codebase/test/infer/test_mcmc.py::test_chain_inside_jit",
        "codebase/test/infer/test_mcmc.py::test_chain_jit_args_smoke",
        "codebase/test/infer/test_mcmc.py::test_reuse_mcmc_run",
        "codebase/test/infer/test_mcmc.py::test_model_with_multiple_exec_paths",
    ]

    for target in pytest_targets:
        rc = run(
            [
                str(PYTHON),
                "-m",
                "pytest",
                "-vs",
                target,
            ],
            env=env,
        )
        if rc != 0:
            return rc

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

