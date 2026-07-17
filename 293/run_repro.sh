#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$ROOT/setup_env.sh"
PYTHONUNBUFFERED=1 "$ROOT/.venv/bin/python" "$ROOT/repro.py"
