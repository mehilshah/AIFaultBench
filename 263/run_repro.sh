#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

if [[ ! -x "${ROOT_DIR}/.venv/bin/python" ]]; then
  bash "${ROOT_DIR}/setup_env.sh"
fi

# shellcheck disable=SC1091
source "${ROOT_DIR}/.venv/bin/activate"

: > repro_stdout.log
: > repro_stderr.log

python repro.py \
  > >(tee -a repro_stdout.log) \
  2> >(tee -a repro_stderr.log >&2)
