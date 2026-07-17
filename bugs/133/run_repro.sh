#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -n "${REPRO_PYTHON:-}" ]]; then
  PYTHON_BIN="$REPRO_PYTHON"
else
  PYTHON_BIN="$("$ROOT_DIR/setup_env.sh")"
fi

exec "$PYTHON_BIN" "$ROOT_DIR/repro.py"
