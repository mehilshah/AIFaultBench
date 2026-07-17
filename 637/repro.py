#!/usr/bin/env python3
"""Run the accelerate 0.14.0 SageMaker config repro."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "sagemaker_default_config.yaml"


def main() -> int:
    if not CONFIG_FILE.exists():
        print(f"Missing config file: {CONFIG_FILE}", file=sys.stderr)
        return 2

    cmd = ["accelerate", "test", "--config_file", str(CONFIG_FILE)]
    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, text=True, capture_output=True)

    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)

    reproduced = "AttributeError: 'Namespace' object has no attribute 'use_cpu'" in proc.stderr
    summary = {
        "command": cmd,
        "returncode": proc.returncode,
        "reproduced": reproduced,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
