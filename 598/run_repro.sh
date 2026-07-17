#!/usr/bin/env bash
set -euo pipefail

if [ ! -x ".venv311/bin/python" ]; then
  bash setup_env.sh
fi

stdout_log="${STDOUT_LOG:-repro_stdout.log}"
stderr_log="${STDERR_LOG:-repro_stderr.log}"

set +e
.venv311/bin/python repro.py >"${stdout_log}" 2>"${stderr_log}"
status=$?
set -e

exit "${status}"
