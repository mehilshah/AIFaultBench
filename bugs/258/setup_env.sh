#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

python3 -m venv .venv
"$ROOT/.venv/bin/pip" install -U pip setuptools wheel
"$ROOT/.venv/bin/pip" install -r requirements.txt
