#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

VENV_PYTHON=".venv/bin/python"
if [ ! -x "$VENV_PYTHON" ]; then
  VENV_PYTHON="python3"
fi

: >repro_stdout.log
: >repro_stderr.log

echo "[stage 0]" >>repro_stdout.log
ZERO_STAGE=0 "$VENV_PYTHON" repro.py >>repro_stdout.log 2>>repro_stderr.log

echo "[stage 1]" >>repro_stdout.log
ZERO_STAGE=1 "$VENV_PYTHON" repro.py >>repro_stdout.log 2>>repro_stderr.log
