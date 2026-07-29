#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
	bash setup_env.sh
fi

export ANONYMIZED_TELEMETRY=false
export BROWSER_USE_SETUP_LOGGING=false
export BROWSER_USE_DISABLE_EXTENSIONS=1
.venv/bin/python repro.py
