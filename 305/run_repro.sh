#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${ROOT}/.repro-venv/bin/python"
if [[ ! -x "${VENV_PYTHON}" ]] || ! "${VENV_PYTHON}" - <<'PY' >/dev/null 2>&1
import peft  # noqa: F401
PY
then
  bash "${ROOT}/setup_env.sh"
fi
source "${ROOT}/.repro-venv/bin/activate"
PYTHONPATH="${ROOT}/codebase/src:${PYTHONPATH:-}" python "${ROOT}/repro.py"
