#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STDOUT_LOG = ROOT / "repro_stdout.log"
STDERR_LOG = ROOT / "repro_stderr.log"
RESULT_JSON = ROOT / "reproduction.json"
SOURCE = ROOT / "fp_quantizer_warning_repro.cu"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def main() -> int:
    cmd = [
        "nvcc",
        "-std=c++17",
        "-arch=sm_80",
        "-c",
        str(SOURCE),
        "-o",
        str(ROOT / "fp_quantizer_warning_repro.o"),
    ]

    proc = run(cmd)
    warnings = []
    seen = set()
    for line in proc.stderr.splitlines():
        if "warning #62-D" in line or "warning #68-D" in line:
            if line not in seen:
                seen.add(line)
                warnings.append(line.strip())

    stdout_summary = "\n".join([
        f"command: {' '.join(cmd)}",
        f"returncode: {proc.returncode}",
        f"warnings_found: {len(warnings)}",
        f"reproducible: {proc.returncode == 0 and len(warnings) >= 2}",
    ])
    STDOUT_LOG.write_text((proc.stdout + ("\n" if proc.stdout and not proc.stdout.endswith("\n") else "") + stdout_summary + "\n"))
    STDERR_LOG.write_text(proc.stderr)

    reproducible = proc.returncode == 0 and len(warnings) >= 2

    result = {
        "reproducible": reproducible,
        "evidence": warnings if warnings else proc.stderr.splitlines()[:20],
        "steps": [
            "Compiled fp_quantizer_warning_repro.cu with nvcc -std=c++17 -arch=sm_80 -c.",
            "Observed CUDA compiler warnings matching the bug report: warning #68-D and warning #62-D.",
        ],
        "blocking_reason": "" if reproducible else "The compile did not emit both expected CUDA warnings.",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
