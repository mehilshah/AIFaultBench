#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PIP_DISABLE_PIP_VERSION_CHECK=1

REQ_FILE="$(mktemp)"
trap 'rm -f "${REQ_FILE}"' EXIT

if python3 - <<'PY' >/dev/null 2>&1
import torch  # noqa: F401
PY
then
  awk '!/^torch([<>=[:space:]]|$)/' "${ROOT_DIR}/requirements.txt" > "${REQ_FILE}"
else
  cp "${ROOT_DIR}/requirements.txt" "${REQ_FILE}"
fi

python3 -m pip install --break-system-packages -U pip setuptools wheel
python3 -m pip install --break-system-packages -r "${REQ_FILE}"
