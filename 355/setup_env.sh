#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 -m venv "${ROOT}/.venv"

# No third-party packages are required for this reproducer.
"${ROOT}/.venv/bin/python" -m pip install --upgrade pip >/dev/null
