#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set +e
PYTHONNOUSERSITE=1 PYTHONPATH="$ROOT/.deps:$ROOT/codebase" python3 "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
status=$?
set -e

echo "repro exit status: $status"
exit "$status"
