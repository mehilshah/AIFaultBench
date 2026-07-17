#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT}/setup_env.sh"
# shellcheck disable=SC1091
source "${ROOT}/.venv/bin/activate"

exec > >(tee "${ROOT}/repro_stdout.log") 2> >(tee "${ROOT}/repro_stderr.log" >&2)
python "${ROOT}/repro.py"
