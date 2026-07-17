#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${SCRIPT_DIR}/repro_stdout.log"
STDERR_LOG="${SCRIPT_DIR}/repro_stderr.log"

: > "${STDOUT_LOG}"
: > "${STDERR_LOG}"

exec > >(tee -a "${STDOUT_LOG}") 2> >(tee -a "${STDERR_LOG}" >&2)

bash "${SCRIPT_DIR}/setup_env.sh"

# shellcheck disable=SC1091
source "${SCRIPT_DIR}/.venv/bin/activate"

cd "${SCRIPT_DIR}"
python repro.py

