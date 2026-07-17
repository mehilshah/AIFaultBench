#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then
    PYTHON_BIN=.venv/bin/python3
else
    PYTHON_BIN=python3
fi
"$PYTHON_BIN" -u repro.py >repro_stdout.log 2>repro_stderr.log
