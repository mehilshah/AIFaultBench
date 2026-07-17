#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="$ROOT_DIR/repro_stdout.log"
STDERR_LOG="$ROOT_DIR/repro_stderr.log"

: >"$STDOUT_LOG"
: >"$STDERR_LOG"

python3 "$ROOT_DIR/repro.py" \
  > >(tee -a "$STDOUT_LOG") \
  2> >(tee -a "$STDERR_LOG" >&2)
