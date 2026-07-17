#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(dirname "$0")"
"$ROOT_DIR/setup_env.sh"
"$ROOT_DIR/.venv/bin/python" "$ROOT_DIR/repro.py"
