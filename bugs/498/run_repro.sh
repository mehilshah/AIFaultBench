#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${ROOT}/.venv/bin/activate"
export HF_HOME="${ROOT}/.hf_cache"
export TRANSFORMERS_CACHE="${ROOT}/.hf_cache"
export HF_HUB_ENABLE_HF_TRANSFER=0
python "${ROOT}/repro.py"

