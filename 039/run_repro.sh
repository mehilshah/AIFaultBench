#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -d "$ROOT_DIR/.venv" ]]; then
  bash "$ROOT_DIR/setup_env.sh"
fi

# shellcheck disable=SC1091
source "$ROOT_DIR/.venv/bin/activate"

python repro.py > repro_stdout.log 2> repro_stderr.log
status=$?

printf '{"exit_code": %d}\n' "$status" > repro_exit_status.json
exit 0
