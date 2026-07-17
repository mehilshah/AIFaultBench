#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck disable=SC1090
. "${ROOT_DIR}/.venv/bin/activate"

python "${ROOT_DIR}/repro.py"
