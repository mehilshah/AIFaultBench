#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv --system-site-packages "${VENV_DIR}"
fi

# Reuse the system torch if present; otherwise pip can resolve it into the venv.
"${VENV_DIR}/bin/pip" install --upgrade pip >/dev/null
"${VENV_DIR}/bin/pip" install --extra-index-url https://download.pytorch.org/whl/cpu -r "${ROOT}/requirements.txt"
"${VENV_DIR}/bin/python" - <<'PY'
import importlib.util
mods = ["torch", "kornia_rs"]
missing = [m for m in mods if importlib.util.find_spec(m) is None]
if missing:
    raise SystemExit(f"missing runtime dependencies: {missing}")
print("environment_ready=True")
PY
