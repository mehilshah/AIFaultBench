#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -x "${root_dir}/.venv/bin/python" ]]; then
    bash "${root_dir}/setup_env.sh"
fi
PYTHONWARNINGS=ignore "${root_dir}/.venv/bin/python" "${root_dir}/repro.py"
