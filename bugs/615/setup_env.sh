#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT/.venv"

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
"$VENV_DIR/bin/pip" install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r "$ROOT/requirements.txt"
