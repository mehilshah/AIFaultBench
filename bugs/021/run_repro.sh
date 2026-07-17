#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$ROOT_DIR/setup_env.sh"
source "$ROOT_DIR/.venv/bin/activate"

cd "$ROOT_DIR"
python repro.py > repro_stdout.log 2> repro_stderr.log
