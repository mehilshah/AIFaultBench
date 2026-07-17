#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/setup_env.sh"

export PYTHONPATH="${ROOT_DIR}/codebase/src${PYTHONPATH:+:${PYTHONPATH}}"
export HF_HUB_DISABLE_PROGRESS_BARS=1
export TQDM_DISABLE=1

exec "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py"
