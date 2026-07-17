#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec > >(tee "${ROOT_DIR}/repro_stdout.log") 2> >(tee "${ROOT_DIR}/repro_stderr.log" >&2)

if ! python3 - <<'PY' >/dev/null 2>&1
import lightning_utilities  # noqa: F401
import torch  # noqa: F401
import torchmetrics  # noqa: F401
PY
then
  "${ROOT_DIR}/setup_env.sh"
fi

export PYTHONUNBUFFERED=1

python3 "${ROOT_DIR}/repro.py"
