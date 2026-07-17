#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT}/setup_env.sh"
# shellcheck source=/dev/null
source "${ROOT}/.venv/bin/activate"
python "${ROOT}/repro.py"
