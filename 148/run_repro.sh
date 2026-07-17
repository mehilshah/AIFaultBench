#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
bash "${ROOT_DIR}/setup_env.sh"

export PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}"
export HF_HOME="${HF_HOME:-${ROOT_DIR}/.hf_cache}"

exec python3 "${ROOT_DIR}/repro.py"
