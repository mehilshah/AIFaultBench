#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${ROOT_DIR}/.venv/bin/activate"

: > "${ROOT_DIR}/repro_stdout.log"
: > "${ROOT_DIR}/repro_stderr.log"

python "${ROOT_DIR}/repro.py" 2> >(tee -a "${ROOT_DIR}/repro_stderr.log" >&2) \
  | tee -a "${ROOT_DIR}/repro_stdout.log"
