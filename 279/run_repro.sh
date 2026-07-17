#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"
bash "$ROOT_DIR/setup_env.sh" > /dev/null
python3 -u "$ROOT_DIR/repro.py" >"$ROOT_DIR/repro_stdout.log" 2>"$ROOT_DIR/repro_stderr.log"
