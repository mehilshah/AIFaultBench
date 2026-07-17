#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="$ROOT/.repro_deps"

if [[ -f "$DEPS_DIR/.ready" ]]; then
  exit 0
fi

mkdir -p "$DEPS_DIR"

python3 -m pip install --break-system-packages --upgrade pip setuptools wheel
python3 -m pip install --break-system-packages --target "$DEPS_DIR" --upgrade --index-url https://download.pytorch.org/whl/cpu torch==2.5.1
python3 -m pip install --break-system-packages --target "$DEPS_DIR" --upgrade --no-deps accelerate==1.7.0
python3 -m pip install --break-system-packages --target "$DEPS_DIR" --upgrade -r "$ROOT/requirements.txt"
touch "$DEPS_DIR/.ready"
