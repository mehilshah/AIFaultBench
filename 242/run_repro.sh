#!/usr/bin/env bash
set -euo pipefail

export JAX_PLATFORM_NAME=cpu

bash setup_env.sh
source .venv/bin/activate
python repro.py
