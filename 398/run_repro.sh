#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-/tmp/repro_bug_398_venv}"

source "$VENV_DIR/bin/activate"
cd "$ROOT_DIR"
PYTHONPATH="$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}" \
  python repro.py > repro_stdout.log 2> repro_stderr.log
