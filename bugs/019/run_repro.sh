#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

: >"${STDOUT_LOG}"
: >"${STDERR_LOG}"

exec > >(tee -a "${STDOUT_LOG}") 2> >(tee -a "${STDERR_LOG}" >&2)

bash "${ROOT_DIR}/setup_env.sh"

# shellcheck disable=SC1091
source "${ROOT_DIR}/.venv/bin/activate"
export PYTHONPATH="${ROOT_DIR}/codebase${PYTHONPATH:+:${PYTHONPATH}}"

python "${ROOT_DIR}/repro.py"

