#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Keep the local vLLM source importable without mutating the codebase.
export PYTHONPATH="${ROOT}/codebase${PYTHONPATH:+:${PYTHONPATH}}"

echo "PYTHONPATH=${PYTHONPATH}"
echo "If you need to install the inferred runtime dependencies, run:"
echo "  python3 -m pip install -r ${ROOT}/requirements.txt"

