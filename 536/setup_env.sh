#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT/codebase${PYTHONPATH:+:$PYTHONPATH}"

echo "[setup] root=$ROOT"
echo "[setup] python3=$(command -v python3)"
echo "[setup] PYTHONPATH=$PYTHONPATH"

