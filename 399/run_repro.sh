#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$ROOT_DIR/deps:$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}"

python3 "$ROOT_DIR/repro.py"
