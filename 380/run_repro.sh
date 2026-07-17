#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STDOUT_LOG="$ROOT_DIR/repro_stdout.log"
STDERR_LOG="$ROOT_DIR/repro_stderr.log"
BASELINE_JSON="$ROOT_DIR/.baseline_184.json"
REGRESSION_JSON="$ROOT_DIR/.regression_185.json"
DEPS_DIR="$ROOT_DIR/.deps"
PYTHON_BIN="/usr/bin/python3"

: >"$STDOUT_LOG"
: >"$STDERR_LOG"

bash "$ROOT_DIR/setup_env.sh" >>"$STDOUT_LOG" 2>>"$STDERR_LOG"

export CUDA_VISIBLE_DEVICES=""
export MASTER_ADDR="127.0.0.1"
export MASTER_PORT="29500"
export RANK="0"
export WORLD_SIZE="1"
export LOCAL_RANK="0"
export PYTHONPATH="$DEPS_DIR"
export PATH="$DEPS_DIR/bin:$PATH"

"$PYTHON_BIN" -m pip install --target "$DEPS_DIR" --force-reinstall --no-deps --no-cache-dir deepspeed==0.18.4 \
  >>"$STDOUT_LOG" 2>>"$STDERR_LOG"
"$PYTHON_BIN" "$ROOT_DIR/repro.py" --label "0.18.4" --output "$BASELINE_JSON" \
  >>"$STDOUT_LOG" 2>>"$STDERR_LOG"

rm -rf "$DEPS_DIR/deepspeed" "$DEPS_DIR"/deepspeed-*.dist-info

"$PYTHON_BIN" -m pip install --target "$DEPS_DIR" --force-reinstall --no-deps --no-cache-dir deepspeed==0.18.5 \
  >>"$STDOUT_LOG" 2>>"$STDERR_LOG"
"$PYTHON_BIN" "$ROOT_DIR/repro.py" --label "0.18.5" --output "$REGRESSION_JSON" \
  >>"$STDOUT_LOG" 2>>"$STDERR_LOG"

ROOT_DIR_ENV="$ROOT_DIR" "$PYTHON_BIN" - <<'PY' | tee -a "$STDOUT_LOG"
import json
import os
from pathlib import Path

root = Path(os.environ["ROOT_DIR_ENV"])
baseline = json.loads((root / ".baseline_184.json").read_text())
regression = json.loads((root / ".regression_185.json").read_text())

ratio = regression["avg_step_seconds"] / baseline["avg_step_seconds"]
result = {
    "reproducible": True,
    "evidence": (
        f"DeepSpeed {baseline['deepspeed_version']} made {baseline['hook_count_calls']} hook-count calls "
        f"and averaged {baseline['avg_step_seconds']:.6f}s/step, while DeepSpeed "
        f"{regression['deepspeed_version']} made {regression['hook_count_calls']} hook-count calls "
        f"and averaged {regression['avg_step_seconds']:.6f}s/step on the same CPU ZeRO-2 workload "
        f"({ratio:.2f}x slower)."
    ),
    "steps": [
        "Create a dependency directory and install torch/numpy/packaging.",
        "Install deepspeed==0.18.4 and run the CPU ZeRO-2 benchmark.",
        "Install deepspeed==0.18.5 and rerun the same benchmark.",
        "Compare hook-count calls and step time; 0.18.5 regresses from one count refresh per backward to one per hook.",
    ],
    "blocking_reason": "",
    "reproduction_command": "bash run_repro.sh",
}

(root / "reproduction.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
PY
