#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-/tmp/bug338-venv}"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  bash "${REPO_ROOT}/setup_env.sh"
fi

source "${VENV_DIR}/bin/activate"
export PYTHONPATH="${REPO_ROOT}/codebase${PYTHONPATH:+:${PYTHONPATH}}"
exec python "${REPO_ROOT}/repro.py" "$@"
