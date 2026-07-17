#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [[ "${INSTALL_VLLM:-0}" == "1" ]]; then
  # Install the checked-out vLLM source tree so `vllm serve` is available.
  python -m pip install -e ./codebase
else
  echo "Skipping editable vLLM install; set INSTALL_VLLM=1 to build the local source tree."
fi
