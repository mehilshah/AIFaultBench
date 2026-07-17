#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"

python3 -m venv "$VENV"
"$VENV/bin/pip" install -U pip setuptools wheel
"$VENV/bin/pip" install -r "$ROOT/requirements.txt"
"$VENV/bin/pip" install -e "$ROOT/codebase" --no-deps
