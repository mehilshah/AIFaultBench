#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${REPRO_VENV_DIR:-/tmp/repro_bug450_venv}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  bash "$ROOT/setup_env.sh"
fi

. "$VENV_DIR/bin/activate"
export PYTHONPATH="$ROOT/codebase/src${PYTHONPATH:+:$PYTHONPATH}"
python "$ROOT/repro.py"
