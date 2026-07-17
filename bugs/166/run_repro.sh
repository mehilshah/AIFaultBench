#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$ROOT/codebase:${PYTHONPATH:-}"

python3 "$ROOT/repro.py"
