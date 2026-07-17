#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/setup_env.sh"

# shellcheck disable=SC1091
source "${ROOT_DIR}/.venv/bin/activate"

python "${ROOT_DIR}/repro.py" >"${ROOT_DIR}/repro_stdout.log" 2>"${ROOT_DIR}/repro_stderr.log"
status=$?

cat "${ROOT_DIR}/repro_stdout.log"
if [[ -s "${ROOT_DIR}/repro_stderr.log" ]]; then
  cat "${ROOT_DIR}/repro_stderr.log" >&2
fi

exit "${status}"
