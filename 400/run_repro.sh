#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  bash setup_env.sh
fi

source "${VENV_DIR}/bin/activate"

python repro.py > repro_stdout.log 2> repro_stderr.log
