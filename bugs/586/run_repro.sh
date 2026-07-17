#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT/.venv}"
STDOUT_LOG="$ROOT/repro_stdout.log"
STDERR_LOG="$ROOT/repro_stderr.log"

"$ROOT/setup_env.sh"
source "$VENV_DIR/bin/activate"

export DS_ACCELERATOR=cpu
export DS_BUILD_OPS=0
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"

: > "$STDOUT_LOG"
: > "$STDERR_LOG"

torchrun --standalone --nproc_per_node="${NPROC_PER_NODE:-2}" "$ROOT/repro.py" \
  > >(tee "$STDOUT_LOG") \
  2> >(tee "$STDERR_LOG" >&2)
