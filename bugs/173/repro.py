#!/usr/bin/env python3
"""Reproduce the resolver failure for kfp and kubeflow-katib."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def run_install() -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "kfp==2.7.0",
        "kubeflow-katib==0.17.0rc0",
    ]
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, text=True, capture_output=True)


def main() -> int:
    proc = run_install()

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    reproducible = proc.returncode != 0 and "ResolutionImpossible" in stderr
    evidence = (
        "pip failed to resolve kfp==2.7.0 and kubeflow-katib==0.17.0rc0 together "
        "because kfp requires kubernetes<27 and kubeflow-katib requires kubernetes>=27.2.0."
    )
    steps = [
        "Create a virtual environment.",
        "Run `python -m pip install kfp==2.7.0 kubeflow-katib==0.17.0rc0`.",
        "Observe pip's ResolutionImpossible error on the kubernetes dependency.",
    ]
    blocking_reason = "" if reproducible else "pip did not emit the expected dependency conflict."
    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
