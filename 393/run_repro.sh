#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT_DIR/.venv/bin/activate"

export PYTHONPATH="$ROOT_DIR/codebase/src${PYTHONPATH:+:$PYTHONPATH}"

python "$ROOT_DIR/repro.py" >"$ROOT_DIR/repro_stdout.log" 2>"$ROOT_DIR/repro_stderr.log"
