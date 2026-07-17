#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$ROOT/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  bash "$ROOT/setup_env.sh"
fi

: > "$ROOT/repro_stdout.log"
: > "$ROOT/repro_stderr.log"

run_case() {
  local label="$1"
  shift

  printf '=== %s ===\n' "$label" | tee -a "$ROOT/repro_stdout.log"
  printf '=== %s ===\n' "$label" >> "$ROOT/repro_stderr.log"

  if "$@" >>"$ROOT/repro_stdout.log" 2>>"$ROOT/repro_stderr.log"; then
    printf '%s: unexpectedly succeeded\n' "$label" | tee -a "$ROOT/repro_stdout.log"
    return 1
  fi

  printf '%s: expected failure observed\n' "$label" | tee -a "$ROOT/repro_stdout.log"
}

run_case offline env HF_HUB_OFFLINE=1 "$PYTHON" "$ROOT/repro.py" --case offline
run_case local_files_only "$PYTHON" "$ROOT/repro.py" --case local_files_only

printf 'Both reproduction paths failed with the expected offline-mode ValueError.\n' | tee -a "$ROOT/repro_stdout.log"
