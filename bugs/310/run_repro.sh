#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

"$ROOT/setup_env.sh"

set +e
"$ROOT/.venv/bin/python" "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
status=$?
set -e

exit "$status"
