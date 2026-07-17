#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$ROOT_DIR/.venv/bin/python" ]]; then
  bash "$ROOT_DIR/setup_env.sh"
fi

PYTHONPATH="$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}" \
  "$ROOT_DIR/.venv/bin/python" "$ROOT_DIR/repro.py"
