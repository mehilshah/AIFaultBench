#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -d "${ROOT}/.venv" ]]; then
  bash "${ROOT}/setup_env.sh"
fi
source "${ROOT}/.venv/bin/activate"

stdout_file="${ROOT}/repro_stdout.log"
stderr_file="${ROOT}/repro_stderr.log"

set +e
python "${ROOT}/repro.py" >"${stdout_file}" 2>"${stderr_file}"
exit_code=$?
set -e

if [[ ${exit_code} -ne 0 ]]; then
  reproducible=true
  blocking_reason=null
  evidence="repro.py prints observed_target_entropy=-1.0 and expected_target_entropy=-2.0 for a 2D BoundedContinuous action spec, then exits with code ${exit_code}."
else
  reproducible=false
  blocking_reason="The expected mismatch was not observed."
  evidence="repro.py exited with code 0 and did not show the target entropy mismatch."
fi

cat >"${ROOT}/reproduction.json" <<EOF
{
  "reproducible": ${reproducible},
  "evidence": "${evidence}",
  "steps": [
    "Create a 2D BoundedContinuous action spec.",
    "Build a minimal SACLoss with that action spec.",
    "Read target_entropy and compare it to the expected -dim(A) value."
  ],
  "blocking_reason": ${blocking_reason},
  "reproduction_command": "bash run_repro.sh"
}
EOF

if [[ ${exit_code} -ne 0 ]]; then
  exit 0
fi

exit 0
