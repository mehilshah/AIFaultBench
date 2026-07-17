#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

"$ROOT_DIR/setup_env.sh"

source "$ROOT_DIR/.repro-venv/bin/activate"
export PYTHONPATH="$ROOT_DIR/codebase/src"
export HF_HUB_DISABLE_PROGRESS_BARS=1

: > repro_stdout.log
: > repro_stderr.log

python repro.py > >(tee repro_stdout.log) 2> >(tee repro_stderr.log >&2)
