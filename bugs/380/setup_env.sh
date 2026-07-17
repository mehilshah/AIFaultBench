#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="${DEPS_DIR:-$ROOT_DIR/.deps}"

rm -rf "$DEPS_DIR"
mkdir -p "$DEPS_DIR"

/usr/bin/python3 -m pip install --target "$DEPS_DIR" -r "$ROOT_DIR/requirements.txt"

echo "Dependency directory ready at $DEPS_DIR"
