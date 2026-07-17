#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-/tmp/bug338-venv}"

python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "${REPO_ROOT}/requirements.txt"

cat <<EOF
Environment ready.
Activate with: source "${VENV_DIR}/bin/activate"
Run with: PYTHONPATH="${REPO_ROOT}/codebase" python "${REPO_ROOT}/repro.py"
EOF
