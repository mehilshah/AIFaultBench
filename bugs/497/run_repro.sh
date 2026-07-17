#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$ROOT_DIR/setup_env.sh"
fi

source "$VENV_DIR/bin/activate"
export HF_HUB_DISABLE_XET=1
export TOKENIZERS_PARALLELISM=false
python "$ROOT_DIR/repro.py"
