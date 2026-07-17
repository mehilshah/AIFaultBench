#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --upgrade pip setuptools wheel
"$VENV/bin/python" -m pip install -r "$ROOT/requirements.txt" --extra-index-url https://download.pytorch.org/whl/cpu
"$VENV/bin/python" -m pip install --no-deps "asteroid @ git+https://github.com/asteroid-team/asteroid.git@v0.7.0"
