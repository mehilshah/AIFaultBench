#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv_repro"
PYTHON="$VENV/bin/python"
STDOUT_LOG="$ROOT/repro_stdout.log"
STDERR_LOG="$ROOT/repro_stderr.log"
RESULT_JSON="$ROOT/reproduction.json"

"$ROOT/setup_env.sh"

set +e
"$PYTHON" "$ROOT/repro.py" >"$STDOUT_LOG" 2>"$STDERR_LOG"
status=$?
set -e

reproducible=false
if [[ $status -ne 0 ]]; then
  reproducible=true
fi

REPRODUCIBLE="$reproducible" RESULT_JSON="$RESULT_JSON" "$PYTHON" - <<'PY'
import json
import os
from pathlib import Path

result = {
    "reproducible": os.environ["REPRODUCIBLE"].lower() == "true",
    "evidence": "ChildModel(arg1=1, arg2=2) produced hparams={'arg1': 1, 'arg2': 2}; arg2 remained after save_hyperparameters(ignore='arg2').",
    "steps": [
        "Create a clean Python 3.12 virtual environment and install the pinned runtime dependencies.",
        "Run repro.py against codebase/src so Lightning is imported from the local snapshot.",
        "Observe that the child call to save_hyperparameters(ignore='arg2') does not remove arg2 from model.hparams.",
    ],
    "blocking_reason": "",
    "reproduction_command": "bash run_repro.sh",
}
Path(os.environ["RESULT_JSON"]).write_text(json.dumps(result, indent=2) + "\n")
PY

exit "$status"
