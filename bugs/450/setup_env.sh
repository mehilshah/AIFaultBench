#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"
VENV_DIR="${REPRO_VENV_DIR:-/tmp/repro_bug450_venv}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN=python3
fi

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

. "$VENV_DIR/bin/activate"
python -m pip install -U pip setuptools wheel
python -m pip install -r "$ROOT/requirements.txt"
