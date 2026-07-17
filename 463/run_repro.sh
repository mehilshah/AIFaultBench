#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

"$ROOT_DIR/setup_env.sh"

exec "$VENV_DIR/bin/python" "$ROOT_DIR/repro.py"
