#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -x "$SCRIPT_DIR/.venv/bin/python" ]; then
  bash "$SCRIPT_DIR/setup_env.sh"
fi

# shellcheck disable=SC1091
source "$SCRIPT_DIR/.venv/bin/activate"

stdout_log="$SCRIPT_DIR/repro_stdout.log"
stderr_log="$SCRIPT_DIR/repro_stderr.log"

set +e
python "$SCRIPT_DIR/repro.py" >"$stdout_log" 2>"$stderr_log"
status=$?
set -e

cat "$stdout_log"
cat "$stderr_log" >&2

exit "$status"
