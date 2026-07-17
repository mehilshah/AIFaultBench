#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

export PYTHONPATH="$ROOT_DIR/codebase/src:${PYTHONPATH:-}"
export ACCELERATE_USE_FSDP=true
export FSDP_VERSION=2
export MASTER_ADDR="${MASTER_ADDR:-localhost}"
export MASTER_PORT="${MASTER_PORT:-29517}"
export RANK="${RANK:-0}"
export LOCAL_RANK="${LOCAL_RANK:-0}"
export WORLD_SIZE="${WORLD_SIZE:-1}"

stdout_log="$ROOT_DIR/repro_stdout.log"
stderr_log="$ROOT_DIR/repro_stderr.log"

set +e
"$PYTHON_BIN" "$ROOT_DIR/repro.py" >"$stdout_log" 2>"$stderr_log"
status=$?
set -e

printf 'exit_status=%s\n' "$status" >>"$stdout_log"
exit "$status"
