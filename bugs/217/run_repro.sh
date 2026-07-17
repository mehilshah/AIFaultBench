#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"
STDOUT_LOG="${ROOT}/repro_stdout.log"
STDERR_LOG="${ROOT}/repro_stderr.log"
RESULT_JSON="${ROOT}/reproduction.json"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  bash "${ROOT}/setup_env.sh"
fi

source "${VENV_DIR}/bin/activate"
export STANZA_RESOURCES_DIR="${ROOT}/stanza_resources"
mkdir -p "${STANZA_RESOURCES_DIR}"

: >"${STDOUT_LOG}"
: >"${STDERR_LOG}"

set +e
python "${ROOT}/repro.py" >"${STDOUT_LOG}" 2>"${STDERR_LOG}"
status=$?
set -e

python - "${status}" "${STDOUT_LOG}" "${STDERR_LOG}" "${RESULT_JSON}" <<'PY'
import json
import pathlib
import sys

status = int(sys.argv[1])
stdout_path = pathlib.Path(sys.argv[2])
stderr_path = pathlib.Path(sys.argv[3])
result_path = pathlib.Path(sys.argv[4])

stdout = stdout_path.read_text(errors="replace")
stderr = stderr_path.read_text(errors="replace")

reproducible = status != 0 and "KeyError: 'bert_finetune'" in stderr

if reproducible:
    evidence = "Pipeline('en', package='mimic', processors={'ner': 'i2b2'}) fails in codebase/stanza/models/pos/trainer.py with KeyError: 'bert_finetune'."
    blocking_reason = ""
else:
    evidence = "The repro script did not hit the reported KeyError."
    blocking_reason = "The bug did not reproduce in this environment."

result = {
    "reproducible": reproducible,
    "evidence": evidence,
    "steps": [
        "Create and activate the isolated Python 3.11 environment with setup_env.sh.",
        "Run repro.py with STANZA_RESOURCES_DIR pointing at the local stanza_resources/ directory.",
        "Observe the POS trainer initialization crash with KeyError: 'bert_finetune'.",
    ],
    "blocking_reason": blocking_reason,
    "reproduction_command": "bash run_repro.sh",
}

result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

print(stdout, end="")
print(stderr, end="", file=sys.stderr)
PY

exit "${status}"
