#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/.venv/bin/activate"
export PYTHONPATH="$ROOT:$ROOT/codebase/src:${PYTHONPATH:-}"
python "$ROOT/repro.py"

