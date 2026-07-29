#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
    bash setup_env.sh
fi

exec .venv/bin/python repro.py
