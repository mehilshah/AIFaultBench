#!/usr/bin/env bash
set -u -o pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"
RESULT_JSON="${ROOT_DIR}/reproduction.json"

"${ROOT_DIR}/setup_env.sh"

set +e
"${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
RC=$?
set -e

if grep -q "KeyError: \"\\['all_null_col'\\] not in index\"" "${STDERR_LOG}"; then
  REPRODUCIBLE=true
  EVIDENCE="PARSynthesizer.sample() raises KeyError for the all-null modeled column at codebase/sdv/sequential/par.py:509."
  BLOCKING_REASON=""
else
  REPRODUCIBLE=false
  EVIDENCE="The exact KeyError from the issue was not observed."
  BLOCKING_REASON="The repro did not reach the reported KeyError."
fi

"${ROOT_DIR}/.venv/bin/python" - "${RESULT_JSON}" "${REPRODUCIBLE}" "${EVIDENCE}" "${BLOCKING_REASON}" "bash run_repro.sh" <<'PY'
import json
import sys

path, reproducible, evidence, blocking_reason, command = sys.argv[1:]
payload = {
    "reproducible": reproducible == "true",
    "evidence": evidence,
    "steps": [
        "Create a local virtual environment with setup_env.sh.",
        "Install the runtime dependencies from requirements.txt and the local codebase in editable mode.",
        "Run repro.py against a table with an all-null modeled column and call PARSynthesizer.sample(num_sequences=2).",
    ],
    "blocking_reason": blocking_reason,
    "reproduction_command": command,
}
with open(path, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)
    f.write("\n")
PY

exit "${RC}"
