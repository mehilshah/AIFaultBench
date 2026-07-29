#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

if [[ ! -x .venv/bin/python ]]; then
    bash setup_env.sh
fi

exec .venv/bin/python repro.py
