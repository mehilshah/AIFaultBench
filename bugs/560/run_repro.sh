#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="${ROOT_DIR}/.venv_repro/bin/python"

export PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}"
export PATH="${ROOT_DIR}/.venv_repro/bin:${PATH}"

bash "${ROOT_DIR}/setup_env.sh"

rm -f "${ROOT_DIR}/repro_stdout.log" "${ROOT_DIR}/repro_stderr.log" "${ROOT_DIR}/reproduction.json"

"${VENV_PY}" -m torch.distributed.run --standalone --nproc_per_node=2 "${ROOT_DIR}/repro.py" \
  >"${ROOT_DIR}/repro_stdout.log" \
  2>"${ROOT_DIR}/repro_stderr.log"
