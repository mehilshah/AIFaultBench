#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$ROOT_DIR/.venv/bin/activate"

python "$ROOT_DIR/repro.py" > >(tee "$ROOT_DIR/repro_stdout.log") 2> >(tee "$ROOT_DIR/repro_stderr.log" >&2)
