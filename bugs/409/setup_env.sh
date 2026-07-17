#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="$ROOT/.deps"

rm -rf "$DEPS_DIR"
mkdir -p "$DEPS_DIR"

python3 -m pip install --target "$DEPS_DIR" torch==2.10.0 numpy
