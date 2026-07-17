#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  bash "$ROOT/setup_env.sh"
fi

export PYTHONNOUSERSITE=1
export HF_HUB_DISABLE_TELEMETRY=1

exec "$VENV_DIR/bin/python" "$ROOT/repro.py"
