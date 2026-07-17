#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

rm -rf "$VENV"
python3 -m venv "$VENV"
source "$VENV/bin/activate"
python -m pip install -r "$ROOT/requirements.txt"
