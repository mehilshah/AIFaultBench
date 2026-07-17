#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [ ! -d "$VENV_DIR" ] || [ ! -x "$VENV_DIR/bin/python" ] || ! "$VENV_DIR/bin/python" - <<'PY' >/dev/null 2>&1
import torch
PY
then
  rm -rf "$VENV_DIR"
  python3 -m venv --system-site-packages "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r requirements.txt
