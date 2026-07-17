#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -f "${ROOT_DIR}/.venv/bin/activate" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

# shellcheck disable=SC1091
source "${ROOT_DIR}/.venv/bin/activate"

python "${ROOT_DIR}/repro.py"
