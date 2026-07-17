#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

export PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}"

exec > >(tee "${ROOT_DIR}/repro_stdout.log") 2> >(tee "${ROOT_DIR}/repro_stderr.log" >&2)

"${VENV_PYTHON}" "${ROOT_DIR}/repro.py" --mode both
