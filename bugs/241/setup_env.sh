#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="${ROOT_DIR}/.deps"

cd "${ROOT_DIR}"
rm -rf "${DEPS_DIR}"
mkdir -p "${DEPS_DIR}"
python3 -m pip install --break-system-packages --upgrade pip
python3 -m pip install --break-system-packages --target "${DEPS_DIR}" -r requirements.txt
