#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/setup_env.sh"

export JAX_TRACEBACK_FILTERING=off
export PYTHONPATH="${ROOT_DIR}/codebase:${ROOT_DIR}/.deps${PYTHONPATH:+:${PYTHONPATH}}"
python3 "${ROOT_DIR}/repro.py"
