#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -x "${root_dir}/.venv/bin/python" ]]; then
    python3 -m venv "${root_dir}/.venv"
fi
"${root_dir}/.venv/bin/python" -m pip install -r "${root_dir}/requirements.txt"
"${root_dir}/.venv/bin/python" -m pip install --no-build-isolation --no-deps -e "${root_dir}/codebase/libs/langgraph"
