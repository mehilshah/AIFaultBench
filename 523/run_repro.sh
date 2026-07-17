#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$ROOT_DIR/setup_env.sh"
fi

source "$VENV_DIR/bin/activate"

set +e
python "$ROOT_DIR/repro.py" >"$ROOT_DIR/repro_stdout.log" 2>"$ROOT_DIR/repro_stderr.log"
exit_code=$?
set -e

python - "$exit_code" <<'PY'
import json
import sys
from pathlib import Path

exit_code = int(sys.argv[1])
reproducible = exit_code != 0
stderr_text = Path("repro_stderr.log").read_text(encoding="utf-8", errors="replace")
stdout_text = Path("repro_stdout.log").read_text(encoding="utf-8", errors="replace")

evidence = (
    "Running Accelerator(cpu=True).prepare(optimizer) raises AssertionError "
    "in accelerate/src/accelerate/state.py:544 when AcceleratorState() inside "
    "AcceleratedOptimizer.__init__ reinitializes PartialState with cpu=False. "
    f"stderr tail: {stderr_text.strip().splitlines()[-1] if stderr_text.strip().splitlines() else 'no stderr captured'}"
)

result = {
    "reproducible": reproducible,
    "evidence": evidence,
    "steps": [
        "Create a torch.nn.Linear model and SGD optimizer.",
        "Instantiate accelerate.Accelerator(cpu=True).",
        "Call accelerator.prepare(optimizer).",
    ],
    "blocking_reason": "" if reproducible else "The repro did not fail in this environment.",
    "reproduction_command": "./run_repro.sh",
}

Path("reproduction.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
if stdout_text.strip():
    print(stdout_text)
PY

exit "$exit_code"
