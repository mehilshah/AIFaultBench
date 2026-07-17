#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export XLA_FLAGS="--xla_force_host_platform_device_count=4"
export XLA_PYTHON_CLIENT_PREALLOCATE="false"

"${ROOT_DIR}/setup_env.sh"
"${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/repro.py"
