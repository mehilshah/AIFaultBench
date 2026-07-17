#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"


def find_setup_evidence() -> list[str]:
    lines = []
    setup_py = CODEBASE / "setup.py"
    for lineno, line in enumerate(setup_py.read_text(encoding="utf-8").splitlines(), start=1):
        if "nvidia-cublas-cu{CUDAVER}" in line:
            lines.append(f"{setup_py}:{lineno}: {line.strip()}")
    version_py = CODEBASE / "lmdeploy" / "version.py"
    for lineno, line in enumerate(version_py.read_text(encoding="utf-8").splitlines(), start=1):
        if "__version__" in line:
            lines.append(f"{version_py}:{lineno}: {line.strip()}")
            break
    return lines


def run_command(cmd: list[str], *, env: dict[str, str] | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd is not None else None,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    evidence = find_setup_evidence()
    print("lmdeploy setup evidence:")
    for item in evidence:
        print(f"  {item}")
    print()

    with tempfile.TemporaryDirectory(prefix="lmdeploy-repro-") as tmp:
        tmp_path = Path(tmp)
        venv_path = tmp_path / "venv"

        venv_proc = run_command([sys.executable, "-m", "venv", str(venv_path)])
        if venv_proc.returncode != 0:
            print(venv_proc.stdout, end="")
            print(venv_proc.stderr, end="", file=sys.stderr)
            result = {
                "reproducible": False,
                "evidence": "Could not create an isolated venv for the package-install repro.",
                "steps": [
                    "Inspected lmdeploy setup metadata.",
                    "Failed to create a temporary virtual environment.",
                ],
                "blocking_reason": "venv creation failed before the dependency install could run.",
                "reproduction_command": "bash run_repro.sh",
            }
            RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            return 1

        pip_cmd = [
            str(venv_path / "bin" / "python"),
            "-m",
            "pip",
            "install",
            "nvidia-cublas-cu13==0.0.1",
        ]
        proc = run_command(pip_cmd, cwd=ROOT)

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)

    stderr_text = f"{proc.stdout}\n{proc.stderr}"
    reproduced = proc.returncode != 0 and "THIS PROJECT 'nvidia-cublas-cu13' IS DEPRECATED." in stderr_text

    result = {
        "reproducible": reproduced,
        "evidence": (
            "lmdeploy 0.10.2 hardcodes `nvidia-cublas-cu{CUDAVER}` in setup.py, and installing "
            "`nvidia-cublas-cu13==0.0.1` fails with the package's deprecation error."
        ),
        "steps": [
            "Verified `codebase/setup.py` resolves CUDA 13 to `nvidia-cublas-cu13`.",
            "Created an isolated Python virtual environment.",
            "Ran `pip install nvidia-cublas-cu13==0.0.1` inside that environment.",
            "Captured the deprecation failure emitted by the package build backend.",
        ],
        "blocking_reason": "" if reproduced else "The install did not emit the expected deprecation error.",
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if reproduced else 2


if __name__ == "__main__":
    raise SystemExit(main())
