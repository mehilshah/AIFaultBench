#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  bash "$ROOT_DIR/setup_env.sh"
fi

export PYTHONPATH="$ROOT_DIR:$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}"
stdout_log="$ROOT_DIR/repro_stdout.log"
stderr_log="$ROOT_DIR/repro_stderr.log"
"$VENV_DIR/bin/python" "$ROOT_DIR/repro.py" >"$stdout_log" 2>"$stderr_log"
