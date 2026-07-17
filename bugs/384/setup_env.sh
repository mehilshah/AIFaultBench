#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -e "${ROOT_DIR}/codebase" ]]; then
  bash "${ROOT_DIR}/setup_codebase.sh"
fi

source "${ROOT_DIR}/.venv_repro/bin/activate"
cd "${ROOT_DIR}/codebase"
if [[ ! -f detectron2/_C.cpython-312-x86_64-linux-gnu.so ]]; then
  mkdir -p /tmp/d2build
  FORCE_CUDA=0 python setup.py build_ext --inplace --build-temp /tmp/d2build
fi
