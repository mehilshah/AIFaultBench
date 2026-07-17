#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_STDOUT="$ROOT_DIR/repro_stdout.log"
LOG_STDERR="$ROOT_DIR/repro_stderr.log"

source "$ROOT_DIR/.venv/bin/activate"
python "$ROOT_DIR/repro.py" >"$LOG_STDOUT" 2>"$LOG_STDERR"
