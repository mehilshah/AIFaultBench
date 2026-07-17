#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-.venv}"

# shellcheck disable=SC1091
source "$ROOT_DIR/$VENV_DIR/bin/activate"

export PYTHONUNBUFFERED=1
python "$ROOT_DIR/repro.py"
