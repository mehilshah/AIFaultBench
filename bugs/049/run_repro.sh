#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PYTHON_BIN=".venv/bin/python"
if [[ ! -x "$PYTHON_BIN" ]]; then
  bash setup_env.sh
fi

PYTHON_BIN=".venv/bin/python"

"$PYTHON_BIN" repro.py > repro_stdout.log 2> repro_stderr.log

cat repro_stdout.log
if [[ -s repro_stderr.log ]]; then
  cat repro_stderr.log >&2
fi
