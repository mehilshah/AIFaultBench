#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${ROOT_DIR}/setup_env.sh"

VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"
exec "${VENV_PYTHON}" "${ROOT_DIR}/repro.py"
