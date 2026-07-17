#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prepare a fresh environment and then install the local package exactly as a
# user would with pip.
source "${ROOT_DIR}/setup_env.sh"
python -m pip install "${ROOT_DIR}/codebase"

python "${ROOT_DIR}/repro.py"
