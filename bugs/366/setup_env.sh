#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-/tmp/repro_repro_366_venv}"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/pip" install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/pip" install -r requirements.txt

printf '%s\n' "${VENV_DIR}"
