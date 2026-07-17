#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${ROOT_DIR}/.venv/bin/activate"
export PYTHONUNBUFFERED=1
python "${ROOT_DIR}/repro.py"
