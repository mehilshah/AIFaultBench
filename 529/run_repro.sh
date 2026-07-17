#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/setup_env.sh"

source "${ROOT_DIR}/.venv/bin/activate"
export PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}"

python "${ROOT_DIR}/repro.py" \
  --world-size "${WORLD_SIZE:-2}" \
  ${FORCE_CPU:+--force-cpu} \
  >"${ROOT_DIR}/repro_stdout.log" \
  2>"${ROOT_DIR}/repro_stderr.log"
