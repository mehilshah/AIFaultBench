#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

if [[ ! -d "${SCRIPT_DIR}/.venv" ]]; then
  ./setup_env.sh
fi

source "${SCRIPT_DIR}/.venv/bin/activate"
python repro.py
