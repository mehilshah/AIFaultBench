#!/usr/bin/env python3
"""Reproduce Apex issue 1823: build isolation imports setup.py without torch."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
STDOUT_LOG = ROOT / "repro_stdout.log"
STDERR_LOG = ROOT / "repro_stderr.log"
RESULT_JSON = ROOT / "reproduction.json"


def run_install() -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-v",
        "--disable-pip-version-check",
        "--no-cache-dir",
        "--global-option=--cpp_ext",
        "--global-option=--cuda_ext",
        ".",
    ]
    env = os.environ.copy()
    env.setdefault("PIP_NO_INPUT", "1")
    return subprocess.run(
        cmd,
        cwd=CODEBASE,
        env=env,
        text=True,
        capture_output=True,
    )


def write_result(proc: subprocess.CompletedProcess[str]) -> None:
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    STDOUT_LOG.write_text(stdout, encoding="utf-8")
    STDERR_LOG.write_text(stderr, encoding="utf-8")

    combined = stdout + "\n" + stderr
    torch_missing = "ModuleNotFoundError: No module named 'torch'" in combined
    reproducible = proc.returncode != 0 and torch_missing

    if reproducible:
        evidence = (
            "pip install failed during build-isolation with ModuleNotFoundError: No module named 'torch'."
        )
        blocking_reason = ""
    else:
        evidence = f"pip install exited with return code {proc.returncode}."
        blocking_reason = "The reported torch import failure was not reproduced."

    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Run `bash run_repro.sh` from the standardized bug folder.",
            "The script runs `pip install -v --disable-pip-version-check --no-cache-dir --global-option=--cpp_ext --global-option=--cuda_ext .` in `codebase/`.",
            "The build backend imports `setup.py` in an isolated environment that does not contain `torch`.",
        ],
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2))


def main() -> int:
    proc = run_install()
    write_result(proc)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
