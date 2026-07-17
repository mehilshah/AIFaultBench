#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  "$ROOT/setup_env.sh"
fi

PYTHON="$ROOT/.venv/bin/python"

export PYTHONPATH="$ROOT/codebase/src"

STDOUT_LOG="$ROOT/repro_stdout.log"
STDERR_LOG="$ROOT/repro_stderr.log"

set +e
"$PYTHON" "$ROOT/repro.py" >"$STDOUT_LOG" 2>"$STDERR_LOG"
status=$?
set -e

if [[ $status -eq 0 ]]; then
  cat >"$ROOT/reproduction.json" <<'EOF'
{
  "reproducible": true,
  "evidence": "A local sharded AutoencoderTiny checkpoint was rewritten so diffusion_pytorch_model.safetensors.index.json mapped one shard to ../outside/secret.safetensors. _get_checkpoint_shard_files resolved that shard to an out-of-directory path, and AutoencoderTiny.from_pretrained loaded successfully from the outside copy after the in-tree shard was removed.",
  "steps": [
    "Created a local AutoencoderTiny checkpoint with sharded safetensors.",
    "Moved one shard outside the model directory and rewrote the index weight_map entry to ../outside/secret.safetensors.",
    "Confirmed _get_checkpoint_shard_files returned the escaped path and from_pretrained loaded the model successfully."
  ],
  "blocking_reason": "",
  "reproduction_command": "./run_repro.sh"
}
EOF
else
  cat >"$ROOT/reproduction.json" <<'EOF'
{
  "reproducible": false,
  "evidence": "The repro script failed before confirming path traversal.",
  "steps": [
    "Created a local AutoencoderTiny checkpoint with sharded safetensors.",
    "Rewrote the checkpoint index to point one shard outside the model directory.",
    "Attempted to load the model through from_pretrained."
  ],
  "blocking_reason": "See repro_stderr.log for the failing command output.",
  "reproduction_command": "./run_repro.sh"
}
EOF
fi

exit $status
