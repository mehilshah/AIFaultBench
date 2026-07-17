#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  bash "$ROOT_DIR/setup_env.sh"
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
fi

"$PYTHON_BIN" repro.py > repro_stdout.log 2> repro_stderr.log
