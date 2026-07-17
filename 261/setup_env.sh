#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
SITE_PACKAGES="$VENV_DIR/lib/python3.12/site-packages"

cd "$ROOT_DIR"

rm -rf "$VENV_DIR"
mkdir -p "$VENV_DIR/bin" "$SITE_PACKAGES"
python3 -m pip install --target "$SITE_PACKAGES" -r "$ROOT_DIR/requirements.txt"
