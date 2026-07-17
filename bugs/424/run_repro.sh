#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${ROOT_DIR}/.venv/bin/activate"
export PYTHONPATH="${ROOT_DIR}/codebase:${PYTHONPATH:-}"
python "${ROOT_DIR}/repro.py"
