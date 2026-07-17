#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv --system-site-packages "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
if ! python - <<'PY'
import torch
PY
then
  python -m pip install torch==2.13.0 --index-url https://download.pytorch.org/whl/cpu
fi
python -m pip install -r "$ROOT/requirements.txt"
