#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -x "${ROOT_DIR}/.venv_test/bin/activate" ]; then
    bash "${ROOT_DIR}/setup_env.sh"
fi
# shellcheck disable=SC1090
source "${ROOT_DIR}/.venv_test/bin/activate"

export DS_ACCELERATOR=cpu
export PYTHONNOUSERSITE=1
export RANK=0
export WORLD_SIZE=1
export LOCAL_RANK=0
export MASTER_ADDR=127.0.0.1
export MASTER_PORT="${MASTER_PORT:-29517}"

python "${ROOT_DIR}/repro.py" > "${ROOT_DIR}/repro_stdout.log" 2> "${ROOT_DIR}/repro_stderr.log"
