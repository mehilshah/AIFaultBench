#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${ROOT_DIR}"

if [[ ! -x ".venv/bin/python" ]]; then
  bash ./setup_env.sh
fi

set +e
".venv/bin/python" repro.py > repro_stdout.log 2> repro_stderr.log
status=$?
set -e
exit "${status}"
