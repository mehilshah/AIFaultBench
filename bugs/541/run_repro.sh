#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="${ROOT}/.venv/bin/python"

if [[ -x "${VENV_PY}" ]]; then
  PYTHON="${VENV_PY}"
else
  PYTHON="${PYTHON:-python3.11}"
fi

export PYTHONPATH="${ROOT}/codebase${PYTHONPATH:+:${PYTHONPATH}}"
"${PYTHON}" "${ROOT}/repro.py"
