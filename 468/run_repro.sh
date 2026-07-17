#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

bash "${ROOT_DIR}/setup_env.sh"

"${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py" \
  > >(tee "${ROOT_DIR}/repro_stdout.log") \
  2> >(tee "${ROOT_DIR}/repro_stderr.log" >&2)
