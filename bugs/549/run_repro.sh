#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "${ROOT}/.venv" ]; then
  bash "${ROOT}/setup_env.sh"
fi

# shellcheck disable=SC1091
source "${ROOT}/.venv/bin/activate"

export PYTHONPATH="${ROOT}/codebase:${PYTHONPATH:-}"
python "${ROOT}/repro.py"
