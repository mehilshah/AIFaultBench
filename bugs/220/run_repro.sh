#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

source "${ROOT}/.venv/bin/activate"
export PYTHONPATH="${ROOT}/codebase${PYTHONPATH:+:${PYTHONPATH}}"

python "${ROOT}/repro.py" "$@"
