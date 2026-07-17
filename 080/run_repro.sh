#!/usr/bin/env bash
set -euo pipefail

bash "$(dirname "$0")/setup_env.sh"
. "$(dirname "$0")/.venv/bin/activate"
python "$(dirname "$0")/repro.py"
