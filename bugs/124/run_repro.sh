#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [ ! -d "${VENV_DIR}" ]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

source "${VENV_DIR}/bin/activate"
cd "${ROOT_DIR}"

python repro.py > repro_stdout.log 2> repro_stderr.log
