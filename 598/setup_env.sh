#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3.11}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

if [ ! -d ".venv311" ]; then
  "${PYTHON_BIN}" -m venv --system-site-packages .venv311
fi

.venv311/bin/pip install --upgrade pip >/dev/null
.venv311/bin/pip install -r requirements.txt --no-deps
.venv311/bin/pip install -e codebase --no-deps
