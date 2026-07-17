#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

git -C codebase checkout 61e05b3d9a967c0cbbda2e355859287ce7221f52

rm -rf deps
python3 -m pip install \
  --target deps \
  --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple \
  -r requirements.txt
