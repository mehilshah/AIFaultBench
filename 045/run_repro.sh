#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  bash setup_env.sh
fi

exec "$VENV_DIR/bin/python" repro.py
