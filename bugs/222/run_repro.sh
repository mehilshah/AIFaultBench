#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-/tmp/repro_towhee_triton_222_venv}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

source "$VENV_DIR/bin/activate"
export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

set +e
python "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
status=$?
set -e

cat "$ROOT/repro_stdout.log"
cat "$ROOT/repro_stderr.log" >&2

exit "$status"
