#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$ROOT/setup_env.sh"

set +e
"$ROOT/.venv/bin/python" "$ROOT/repro.py" >"$ROOT/repro_stdout.log" 2>"$ROOT/repro_stderr.log"
status=$?
set -e

if [ "$status" -eq 0 ]; then
  echo "repro.py completed successfully"
else
  echo "repro.py failed with exit code $status"
fi

exit "$status"
