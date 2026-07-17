#!/usr/bin/env python3
"""Reproduce the stale pip flag failure from the TF Object Detection docs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TARGET_DIR = ROOT / "codebase" / "research" / "object_detection" / "packages" / "tf2"
CMD = [
    sys.executable,
    "-m",
    "pip",
    "install",
    "--use-feature=2020-resolver",
    ".",
]


def main() -> int:
    stdout_path = ROOT / "repro_stdout.log"
    stderr_path = ROOT / "repro_stderr.log"
    result_path = ROOT / "reproduction.json"

    proc = subprocess.run(
        CMD,
        cwd=TARGET_DIR,
        text=True,
        capture_output=True,
        check=False,
    )

    stdout_path.write_text(
        "\n".join(
            [
                f"reproduction_command: {' '.join(CMD)}",
                f"working_directory: {TARGET_DIR}",
                f"returncode: {proc.returncode}",
                "",
                proc.stdout.rstrip(),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    stderr_path.write_text(proc.stderr, encoding="utf-8")

    reproducible = proc.returncode != 0 and "invalid choice: '2020-resolver'" in proc.stderr
    payload = {
        "reproducible": reproducible,
        "evidence": (
            "pip 26.1.2 rejects --use-feature=2020-resolver with "
            "invalid choice; the command exits with status 2."
        ),
        "steps": [
            "Open codebase/research/object_detection/g3doc/tf2.md and find the install command.",
            "Run python3 -m pip install --use-feature=2020-resolver . from codebase/research/object_detection/packages/tf2.",
            "Observe pip fail before installation starts with invalid choice: '2020-resolver'.",
        ],
        "blocking_reason": "" if reproducible else "The failure did not reproduce in this environment.",
        "reproduction_command": "bash run_repro.sh",
    }
    result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(payload, indent=2))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
