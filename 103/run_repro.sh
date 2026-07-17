#!/usr/bin/env bash
set -euo pipefail

if [[ -x .venv/bin/python ]]; then
  PYTHON_BIN=".venv/bin/python"
else
  PYTHON_BIN="python3"
fi

export PYTHONPATH="$(pwd)/codebase${PYTHONPATH:+:$PYTHONPATH}"
"$PYTHON_BIN" -W always repro.py
