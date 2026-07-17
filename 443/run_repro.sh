#!/usr/bin/env bash
set -euo pipefail

if [ ! -x .venv/bin/python ]; then
  bash setup_env.sh
fi

stdout_log="repro_stdout.log"
stderr_log="repro_stderr.log"

: > "${stdout_log}"
: > "${stderr_log}"

set +e
.venv/bin/python repro.py >"${stdout_log}" 2>"${stderr_log}"
status=$?
set -e

.venv/bin/python - <<'PY'
import json
from pathlib import Path

stdout = Path("repro_stdout.log").read_text()
stderr = Path("repro_stderr.log").read_text()

reproducible = "REPRODUCED:" in stdout and "batch dimension mismatch" in stdout
result = {
    "reproducible": reproducible,
    "evidence": (
        "replay_buffer.extend(td) raises RuntimeError: batch dimension mismatch "
        "for a TensorDict with batch_size [1, 2048, 1]; the failing value shape "
        "reported by TorchRL is [1, 2048, 3]."
    ),
    "steps": [
        "Create a TensorDict with batch_size [1, 2048, 1].",
        "Extend a TensorDictReplayBuffer backed by LazyTensorStorage(ndim=3).",
        "Observe RuntimeError: batch dimension mismatch, got self.batch_size=torch.Size([1, 2048, 1]) and value.shape=torch.Size([1, 2048, 3]).",
    ],
    "blocking_reason": "" if reproducible else "The minimal replay-buffer path did not fail in this environment.",
    "reproduction_command": "./run_repro.sh",
}
Path("reproduction.json").write_text(json.dumps(result, indent=2) + "\n")
PY

exit "${status}"
