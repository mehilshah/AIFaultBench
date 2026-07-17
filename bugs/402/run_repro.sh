#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

if [ -d "$ROOT/.venv" ]; then
    . "$ROOT/.venv/bin/activate"
fi

python "$ROOT/repro.py"
