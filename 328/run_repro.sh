#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT="$ROOT/repro_stdout.log"
STDERR="$ROOT/repro_stderr.log"

: >"$STDOUT"
: >"$STDERR"

run_and_log() {
  "$@" >>"$STDOUT" 2>>"$STDERR"
}

run_and_log "$ROOT/setup_env.sh"
run_and_log "$ROOT/.venv/bin/python" "$ROOT/repro.py"
