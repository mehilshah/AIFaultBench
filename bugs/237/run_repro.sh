#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

bash "$ROOT_DIR/setup_env.sh"

cd "$ROOT_DIR"
: > repro_stdout.log
: > repro_stderr.log
"$VENV_DIR/bin/python" repro.py >repro_stdout.log 2>repro_stderr.log
