#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

bash setup_env.sh

PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}" .venv/bin/python repro.py
