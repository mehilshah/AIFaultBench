#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
	bash setup_env.sh
fi

ANONYMIZED_TELEMETRY=false BROWSER_USE_SETUP_LOGGING=false .venv/bin/python repro.py
