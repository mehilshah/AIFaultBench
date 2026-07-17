#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install -U pip setuptools wheel

# Install a CPU-only torch stack so the local timm checkout imports cleanly.
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision

python -m pip install -r requirements.txt
python -m pip install -e codebase
