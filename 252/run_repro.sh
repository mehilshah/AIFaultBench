#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$ROOT_DIR/setup_env.sh"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
export PYTHONPATH="$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}"

set +e
python "$ROOT_DIR/repro.py" >"$ROOT_DIR/repro_stdout.log" 2>"$ROOT_DIR/repro_stderr.log"
status=$?
set -e

printf 'repro_exit_status=%s\n' "$status"
exit "$status"
