#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$ROOT_DIR/setup_env.sh" >/dev/null 2>&1
source "$ROOT_DIR/.venv/bin/activate"
exec python "$ROOT_DIR/repro.py"
