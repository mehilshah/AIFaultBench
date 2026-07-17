#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
    bash setup_env.sh
fi

export PYTHONPATH="$(pwd)/codebase/src"
exec .venv/bin/python -u repro.py
