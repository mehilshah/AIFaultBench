#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"

if [ ! -x "$PYTHON_BIN" ]; then
  bash "$ROOT_DIR/setup_env.sh"
fi

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing interpreter: $PYTHON_BIN" >&2
  exit 2
fi

"$PYTHON_BIN" repro.py > repro_stdout.log 2> repro_stderr.log
exit $?
