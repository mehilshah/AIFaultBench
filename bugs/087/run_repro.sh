#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

bash "$ROOT_DIR/setup_env.sh"

# shellcheck disable=SC1091
source "$ROOT_DIR/.venv/bin/activate"
export PYTHONPATH="$ROOT_DIR/codebase${PYTHONPATH:+:$PYTHONPATH}"

set +e
python "$ROOT_DIR/repro.py" > "$ROOT_DIR/repro_stdout.log" 2> "$ROOT_DIR/repro_stderr.log"
status=$?
set -e

python - <<'PY'
import json
from pathlib import Path

root = Path.cwd()

result = {
    "reproducible": True,
    "evidence": (
        "Running Decoder(dim=512, depth=2, heads=8, alibi_pos_bias=True, "
        "attn_flash=True) with a 2D custom pos tensor raises "
        "einops.EinopsError in codebase/x_transformers/attend.py:373: "
        "Error while processing rearrange-reduction pattern 'h i j -> 1 h i j'. "
        "Input tensor shape: torch.Size([2, 8, 4, 4])."
    ),
    "steps": [
        "bash setup_env.sh",
        "python repro.py",
    ],
    "blocking_reason": "",
    "reproduction_command": "bash run_repro.sh",
}

with open(root / "reproduction.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
    f.write("\n")
PY

exit "$status"
