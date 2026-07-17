#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  bash "$ROOT_DIR/setup_env.sh"
fi

set +e
"$VENV_DIR/bin/python" "$ROOT_DIR/repro.py" >"$ROOT_DIR/repro_stdout.log" 2>"$ROOT_DIR/repro_stderr.log"
status=$?
set -e

echo "repro_exit_code=$status"
exit "$status"
