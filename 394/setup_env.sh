#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

export DS_BUILD_OPS=0
VENV_DIR=".venv"
CODEBASE_DIR="$(pwd)/codebase"
export PIP_CERT="/etc/ssl/certs/ca-certificates.crt"
export SSL_CERT_FILE="$PIP_CERT"

if [ -d "$VENV_DIR" ]; then
  rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"

"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel
"$VENV_DIR/bin/python" -m pip install -r requirements.txt
"$VENV_DIR/bin/python" -m pip install -e "file://$CODEBASE_DIR"
