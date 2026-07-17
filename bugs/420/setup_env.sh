#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.5.1
python -m pip install -r "$ROOT_DIR/requirements.txt"
# tokenizers is required by this snapshot at import time, but its wheel metadata
# conflicts with the newer huggingface-hub release used by this source tree.
python -m pip install --no-deps --force-reinstall tokenizers==0.22.2
python -m pip install -e "$ROOT_DIR/codebase" --no-deps
