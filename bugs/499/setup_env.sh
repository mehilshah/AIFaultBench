#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip setuptools wheel

# Install a CPU-only torch build so the local source tree imports cleanly in this container.
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.5.1
python -m pip install -r "$ROOT/requirements.txt"
