#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

source "$ROOT/setup_env.sh"
python3 "$ROOT/repro.py"

