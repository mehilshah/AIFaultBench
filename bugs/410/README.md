# Bug 410

This folder contains the preserved issue report, the checked-out vLLM source snapshot, and the reproduction bundle.

What the repro shows:
- The Qwen3-ASR realtime path hard-codes `segment_duration_s = 5.0`.
- The realtime buffer emits each 5-second audio segment independently.
- A single utterance longer than 5 seconds is therefore expected to surface as multiple streamed chunks unless the client merges them after the fact.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Issue reference:
- https://github.com/vllm-project/vllm/issues/47421

Source references inside the checked-out snapshot:
- `codebase/vllm/model_executor/models/qwen3_asr_realtime.py`
- `codebase/vllm/model_executor/models/qwen3_asr.py`
