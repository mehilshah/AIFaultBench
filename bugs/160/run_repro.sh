#!/usr/bin/env bash
set -euo pipefail

exec > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)

bash setup_env.sh
VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_BIN="${PYTHON_BIN:-${VENV_DIR}/bin/python}"
"${PYTHON_BIN}" repro.py
