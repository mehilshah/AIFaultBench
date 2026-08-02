#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
    bash setup_env.sh
fi

if .venv/bin/python repro.py; then
    exit 0
else
    exit $?
fi
