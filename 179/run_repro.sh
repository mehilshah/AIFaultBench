#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$ROOT/.venv" ]; then
  "$ROOT/setup_env.sh"
fi

# shellcheck disable=SC1091
source "$ROOT/.venv/bin/activate"
python "$ROOT/repro.py"
