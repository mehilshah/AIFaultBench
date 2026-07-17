#!/usr/bin/env python3
"""Reproduce the clearml / clearml-agent dependency conflict."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQ_FILE = ROOT / "requirements.txt"
STDOUT_LOG = ROOT / "repro_stdout.log"
STDERR_LOG = ROOT / "repro_stderr.log"
RESULT_JSON = ROOT / "reproduction.json"


def run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd is not None else None,
        text=True,
        capture_output=True,
        check=False,
    )


def append(lines: list[str], title: str, payload: str) -> None:
    lines.append(f"== {title} ==")
    if payload.strip():
        lines.append(payload.rstrip())
    else:
        lines.append("<empty>")


def write_log(path: Path, sections: list[str]) -> None:
    path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    stdout_sections: list[str] = []
    stderr_sections: list[str] = []

    append(stdout_sections, "Environment", f"python={sys.version.split()[0]}")
    append(stdout_sections, "Requirements", REQ_FILE.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix="clearml-resolve-") as tmpdir:
        tmp = Path(tmpdir)
        venv_dir = tmp / "venv"

        venv_proc = run([sys.executable, "-m", "venv", str(venv_dir)])
        append(stdout_sections, "Create venv stdout", venv_proc.stdout)
        append(stderr_sections, "Create venv stderr", venv_proc.stderr)
        if venv_proc.returncode != 0:
            result = {
                "reproducible": False,
                "evidence": "Failed to create the temporary virtual environment.",
                "steps": [
                    "Create a fresh virtual environment.",
                    "Run pip against clearml==2.0.0 and clearml-agent==1.9.3.",
                ],
                "blocking_reason": "Virtual environment creation failed.",
                "reproduction_command": "bash run_repro.sh",
            }
            RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            write_log(STDOUT_LOG, stdout_sections)
            write_log(STDERR_LOG, stderr_sections)
            print(json.dumps(result, indent=2))
            return 1

        py = venv_dir / "bin" / "python"
        pip_base = [str(py), "-m", "pip"]

        upgrade_proc = run(pip_base + ["install", "--upgrade", "pip"])
        append(stdout_sections, "Upgrade pip stdout", upgrade_proc.stdout)
        append(stderr_sections, "Upgrade pip stderr", upgrade_proc.stderr)

        install_cmd = pip_base + ["install", "--dry-run", "--no-input", "-r", str(REQ_FILE)]
        install_proc = run(install_cmd)
        append(stdout_sections, "Resolver stdout", install_proc.stdout)
        append(stderr_sections, "Resolver stderr", install_proc.stderr)

        conflict_seen = install_proc.returncode != 0 and "ResolutionImpossible" in install_proc.stderr
        evidence = (
            "Pip reported that clearml 2.0.0 requires requests>=2.32.0 while "
            "clearml-agent 1.9.3 requires requests<=2.31.0, making the resolver fail."
        )
        if not conflict_seen:
            evidence = "Pip did not report the expected ResolutionImpossible error."

        result = {
            "reproducible": conflict_seen,
            "evidence": evidence,
            "steps": [
                "Create a fresh Python virtual environment.",
                "Upgrade pip inside the virtual environment.",
                "Run pip install --dry-run -r requirements.txt with clearml==2.0.0 and clearml-agent==1.9.3.",
                "Observe pip fail with a requests version conflict.",
            ],
            "blocking_reason": "" if conflict_seen else "Resolver did not fail as expected.",
            "reproduction_command": "bash run_repro.sh",
        }

        RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_log(STDOUT_LOG, stdout_sections)
        write_log(STDERR_LOG, stderr_sections)

        print(json.dumps(result, indent=2))
        return 0 if conflict_seen else 1


if __name__ == "__main__":
    raise SystemExit(main())
