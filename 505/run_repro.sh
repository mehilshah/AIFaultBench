#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/setup_env.sh"

env -u LD_LIBRARY_PATH PYTHONNOUSERSITE=1 \
  "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py"
