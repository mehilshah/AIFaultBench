#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$ROOT/.venv"

if [ ! -d "$VENV" ]; then
  python3 -m venv --system-site-packages "$VENV"
fi

"$VENV/bin/python" -m pip install -q -U pip setuptools wheel
"$VENV/bin/python" -m pip install -q -r "$ROOT/requirements.txt"
"$VENV/bin/python" -m pip install -q -e "$ROOT/codebase"
