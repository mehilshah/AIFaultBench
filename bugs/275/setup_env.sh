#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --quiet --upgrade pip setuptools wheel

if ! "$VENV_DIR/bin/python" - <<'PY'
import importlib

modules = ["torch", "torchvision", "numpy", "fvcore", "iopath", "yaml", "PIL", "omegaconf"]
for name in modules:
    importlib.import_module(name)
PY
then
  "$VENV_DIR/bin/python" -m pip install --quiet \
    torch==2.5.1 torchvision==0.20.1 \
    --index-url https://download.pytorch.org/whl/cpu
  "$VENV_DIR/bin/python" -m pip install --quiet -r "$ROOT/requirements.txt"
fi

printf 'Virtualenv ready at %s\n' "$VENV_DIR"
