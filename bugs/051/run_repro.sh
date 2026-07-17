#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "${ROOT_DIR}/.venv" ]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

source "${ROOT_DIR}/.venv/bin/activate"
export KERAS_BACKEND=tensorflow
python "${ROOT_DIR}/repro.py"
