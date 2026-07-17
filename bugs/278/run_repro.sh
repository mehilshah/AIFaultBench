#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/setup_env.sh"
PYTHONPATH="${SCRIPT_DIR}/codebase" "${SCRIPT_DIR}/.venv/bin/python" "${SCRIPT_DIR}/repro.py"
