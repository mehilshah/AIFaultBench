#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"
"$VENV_DIR/bin/python" repro.py > repro_stdout.log 2> repro_stderr.log
