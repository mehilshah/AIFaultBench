#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="$(pwd)/codebase:${PYTHONPATH:-}"

if [ -x .venv/bin/python ]; then
  PYTHON_BIN=.venv/bin/python
else
  PYTHON_BIN=python3
fi

"$PYTHON_BIN" repro.py
