#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
python -m pip install --quiet --upgrade pip
python -m pip install --quiet --index-url https://download.pytorch.org/whl/cpu -r "$ROOT/requirements.txt"
