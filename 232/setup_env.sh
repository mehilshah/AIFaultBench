#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ -x "$VENV_DIR/bin/python" ]]; then
  if "$VENV_DIR/bin/python" - <<'PY'
import importlib
for module in ("torch", "pytorch_lightning", "neuralprophet"):
    importlib.import_module(module)
PY
  then
    exit 0
  fi
fi

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install --index-url https://download.pytorch.org/whl/cpu "torch==2.4.1+cpu"
python -m pip install -r "$ROOT_DIR/requirements.txt"
python -m pip install -e "$ROOT_DIR/codebase" --no-deps
