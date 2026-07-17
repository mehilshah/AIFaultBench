#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-/tmp/repro_repro_366_venv}"

bash "$(dirname "$0")/setup_env.sh" >/dev/null
"${VENV_DIR}/bin/python" "$(dirname "$0")/repro.py"
