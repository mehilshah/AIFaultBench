#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="${ROOT_DIR}/.deps"

export PYTHONPATH="${DEPS_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
python3 "${ROOT_DIR}/repro.py"
