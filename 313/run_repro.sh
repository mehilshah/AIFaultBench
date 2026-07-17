#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -d .venv ]]; then
  bash setup_env.sh
fi

source .venv/bin/activate
timeout 60s python repro.py
