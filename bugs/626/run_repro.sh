#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "${ROOT}/setup_env.sh"

set +e
python3 "${ROOT}/repro.py" >"${ROOT}/repro_stdout.log" 2>"${ROOT}/repro_stderr.log"
status=$?
set -e

cat "${ROOT}/repro_stdout.log"
cat "${ROOT}/repro_stderr.log" >&2

exit "${status}"
