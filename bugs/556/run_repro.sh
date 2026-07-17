#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN=".venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  bash setup_env.sh
fi

PYTHONNOUSERSITE=1 "$PYTHON_BIN" -u repro.py >repro_stdout.log 2>repro_stderr.log || true

PYTHONNOUSERSITE=1 "$PYTHON_BIN" - <<'PY'
import json
from pathlib import Path

stdout_path = Path("repro_stdout.log")
stderr_path = Path("repro_stderr.log")
stdout = stdout_path.read_text() if stdout_path.exists() else ""
stderr = stderr_path.read_text() if stderr_path.exists() else ""

reproducible = "AttributeError" in stderr and "_timesfm_moving_average" in stderr
blocking_reason = None if reproducible else "The expected TimesFM 2.5 AttributeError did not occur."
evidence = stderr.strip() if stderr.strip() else stdout.strip()
result = {
    "reproducible": reproducible,
    "evidence": evidence,
    "steps": [
        "Install dependencies with setup_env.sh",
        "Run repro.py against the local codebase/ checkout",
        "Pass window_size=5 into TimesFm2_5ModelForPrediction.forward()",
    ],
    "blocking_reason": blocking_reason,
    "reproduction_command": "bash run_repro.sh",
}
Path("reproduction.json").write_text(json.dumps(result, indent=2) + "\n")
PY
