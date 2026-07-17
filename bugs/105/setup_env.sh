#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 -m pip install --user --disable-pip-version-check --break-system-packages -r "${ROOT_DIR}/requirements.txt"
