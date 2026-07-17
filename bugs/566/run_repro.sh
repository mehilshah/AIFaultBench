#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$ROOT/setup_env.sh"
source "$ROOT/.venv/bin/activate"
export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

python "$ROOT/repro.py"
