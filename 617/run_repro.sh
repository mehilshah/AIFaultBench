#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${ROOT_DIR}/.venv/bin/activate"
export PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}"
exec > >(tee "${ROOT_DIR}/repro_stdout.log") 2> >(tee "${ROOT_DIR}/repro_stderr.log" >&2)
python "${ROOT_DIR}/repro.py"
