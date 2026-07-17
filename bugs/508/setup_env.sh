#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r "${ROOT_DIR}/requirements.txt"
python -m pip install --no-deps -e "${ROOT_DIR}/codebase"

if python - <<'PY'
import importlib.util
print("present" if importlib.util.find_spec("typing_extensions") else "missing")
PY
then
  python -m pip uninstall -y typing_extensions >/dev/null 2>&1 || true
fi

python - <<'PY'
import importlib.util
print("typing_extensions", "present" if importlib.util.find_spec("typing_extensions") else "missing")
PY
