#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

bash "$ROOT_DIR/setup_env.sh" >/dev/null

exec "$VENV_DIR/bin/python" "$ROOT_DIR/repro.py"
