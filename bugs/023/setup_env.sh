#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="${ROOT_DIR}/.deps"

mkdir -p "${DEPS_DIR}"
python3 -m pip install --break-system-packages --target "${DEPS_DIR}" -r "${ROOT_DIR}/requirements.txt"
