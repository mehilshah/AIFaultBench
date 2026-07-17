#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [[ -d "$VENV_DIR" ]]; then
  source "$VENV_DIR/bin/activate"
fi

python "$ROOT_DIR/repro.py" --dry-run

if ! python - <<'PY'
try:
    import torch
except Exception:
    raise SystemExit(1)

raise SystemExit(0 if torch.cuda.is_available() and torch.cuda.device_count() > 0 else 1)
PY
then
  echo "Blocked: no CUDA GPU is available, so the SM90 FlashAttention 4 path cannot be exercised here." >&2
  exit 2
fi

echo "Launching vLLM server for the reported reproduction..."
vllm serve google/gemma-4-31B-it \
  --port 8080 \
  --gpu-memory-utilization 0.95 \
  --tensor-parallel-size 2 \
  --max-model-len 262144 \
  --max-num-batched-tokens 16384 \
  --reasoning-parser gemma4 \
  --enable-auto-tool-choice \
  --tool-call-parser gemma4 \
  --attention-backend FLASH_ATTN &
server_pid=$!

cleanup() {
  kill "$server_pid" 2>/dev/null || true
}
trap cleanup EXIT

python3 - <<'PY'
import time
import urllib.request

for _ in range(120):
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/v1/models", timeout=2) as resp:
            if resp.status == 200:
                break
    except Exception:
        time.sleep(5)
else:
    raise SystemExit("vLLM server did not become ready")
PY

python "$ROOT_DIR/repro.py" --backend FLASH_ATTN
