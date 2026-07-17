#!/usr/bin/env bash
set -euo pipefail

./setup_env.sh

VENV_DIR="/tmp/repro_bug_492_venv"
"$VENV_DIR/bin/python" repro.py
