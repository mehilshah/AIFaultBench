#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  bash "$ROOT_DIR/setup_env.sh"
fi

source "$VENV_DIR/bin/activate"
python "$ROOT_DIR/repro.py"
