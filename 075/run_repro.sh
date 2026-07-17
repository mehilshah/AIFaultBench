#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

"${ROOT_DIR}/setup_env.sh"

# shellcheck source=/dev/null
source "${ROOT_DIR}/.venv/bin/activate"

: > "${ROOT_DIR}/repro_stdout.log"
: > "${ROOT_DIR}/repro_stderr.log"

python "${ROOT_DIR}/repro.py" \
  > >(tee "${ROOT_DIR}/repro_stdout.log") \
  2> >(tee "${ROOT_DIR}/repro_stderr.log" >&2)

