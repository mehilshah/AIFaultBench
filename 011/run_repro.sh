#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT/.venv311}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
python "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
