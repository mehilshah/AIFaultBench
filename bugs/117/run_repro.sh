#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${VENV_DIR}/bin/python"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"
RESULT_JSON="${ROOT_DIR}/reproduction.json"

"${ROOT_DIR}/setup_env.sh"

set +e
"${PYTHON_BIN}" "${ROOT_DIR}/repro.py" multiply --x 2 --y 10 --verbose >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
EXIT_CODE=$?
set -e

if grep -q "PatchFire.__CallAndUpdateTrace() missing 1 required positional argument: 'target'" "${STDERR_LOG}"; then
  REPRODUCIBLE=true
  BLOCKING_REASON=""
else
  REPRODUCIBLE=false
  if [[ "${EXIT_CODE}" -eq 0 ]]; then
    BLOCKING_REASON="The script completed successfully instead of reproducing the ClearML Fire crash."
  else
    BLOCKING_REASON="The run failed, but not with the expected ClearML Fire TypeError."
  fi
fi

export REPRODUCIBLE BLOCKING_REASON
export RESULT_JSON

python3 - <<'PY'
import json
import os
from pathlib import Path

result = {
    "reproducible": os.environ["REPRODUCIBLE"].lower() == "true",
    "evidence": "stderr contains the ClearML Fire patch failure: PatchFire.__CallAndUpdateTrace() missing 1 required positional argument: 'target'",
    "steps": [
        "Install the local ClearML source from codebase/ into a virtualenv.",
        "Run `python repro.py multiply --x 2 --y 10 --verbose`.",
        "Observe the TypeError raised from clearml/binding/frameworks/__init__.py while Fire is resolving the command."
    ],
    "blocking_reason": os.environ["BLOCKING_REASON"],
    "reproduction_command": "./run_repro.sh"
}
Path(os.environ["RESULT_JSON"]).write_text(json.dumps(result, indent=2) + "\n")
PY

exit "${EXIT_CODE}"
