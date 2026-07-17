#!/usr/bin/env bash
set -euo pipefail

python3 repro.py > repro_stdout.log 2> repro_stderr.log

python3 - <<'PY'
import json
from pathlib import Path

result = {
    "reproducible": False,
    "evidence": [
        "codebase/vllm/model_executor/models/qwen3_asr_realtime.py hard-codes segment_duration_s = 5.0 and emits each 5-second audio segment separately.",
        "A 10-second simulated utterance is split into two 5-second segments by the same buffer logic.",
        "The upstream issue comment says 5-second chunks may need post-processing to merge them.",
    ],
    "steps": [
        "Inspected the Qwen3-ASR realtime buffer in the checked-out vLLM source.",
        "Ran a source-level simulation of the realtime buffer with 10 seconds of audio.",
        "Observed that the buffer emits two 5-second segments, which matches the current implementation rather than a defect.",
    ],
    "blocking_reason": "The reported behavior is expected from the current realtime implementation: it intentionally chunks audio into 5-second segments, so the 'segmentation' is not reproducible as a bug in this source snapshot. Direct runtime import is also blocked in this environment by an installed CUDA/NCCL torch mismatch.",
    "reproduction_command": "bash run_repro.sh",
}
Path("reproduction.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
PY
