#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 -m pip install --user --break-system-packages --upgrade pip setuptools wheel
python3 -m pip install --user --break-system-packages -r "${ROOT_DIR}/requirements.txt"
