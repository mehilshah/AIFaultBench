#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

rm -rf .deps
mkdir -p .deps
python3 -m pip install --break-system-packages --target .deps -r requirements.txt || true
