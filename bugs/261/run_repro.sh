#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

cd "$ROOT_DIR"

bash "$ROOT_DIR/setup_env.sh"

PYTHONNOUSERSITE=1 PYTHONPATH="$ROOT_DIR/.venv/lib/python3.12/site-packages${PYTHONPATH:+:$PYTHONPATH}" \
  python3 "$ROOT_DIR/repro.py" > "$ROOT_DIR/repro_stdout.log" 2> "$ROOT_DIR/repro_stderr.log"
status=$?
printf 'exit_code=%s\n' "$status" >> "$ROOT_DIR/repro_stdout.log"
exit "$status"
