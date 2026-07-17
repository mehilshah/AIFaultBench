#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export JAX_PLATFORM_NAME=cpu

bash "$ROOT/setup_env.sh"
exec "$ROOT/.venv/bin/python" "$ROOT/repro.py"
