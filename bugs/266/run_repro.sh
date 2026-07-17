#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="${ROOT_DIR}/repro_stdout.log"
STDERR_LOG="${ROOT_DIR}/repro_stderr.log"

: > "${STDOUT_LOG}"
: > "${STDERR_LOG}"

exec > >(tee -a "${STDOUT_LOG}") 2> >(tee -a "${STDERR_LOG}" >&2)

if "${ROOT_DIR}/setup_env.sh"; then
  :
else
  setup_status=$?
  echo "setup_env.sh failed with exit code ${setup_status}" >&2
  exit "${setup_status}"
fi

# shellcheck disable=SC1091
source "${ROOT_DIR}/.venv/bin/activate"

echo "=== baseline case: no TensorFlow import ==="
python "${ROOT_DIR}/repro.py"
baseline_status=$?
echo "baseline exit code: ${baseline_status}"

echo "=== bug case: TensorFlow imported first ==="
python "${ROOT_DIR}/repro.py" --with-tensorflow
bug_status=$?
echo "bug case exit code: ${bug_status}"

if [[ ${baseline_status} -eq 2 || ${bug_status} -eq 2 ]]; then
  exit 2
fi

if [[ ${bug_status} -ne 0 ]]; then
  exit ${bug_status}
fi

exit ${baseline_status}
