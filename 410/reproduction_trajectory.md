# Reproduction Trajectory — Bug 410: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47421](https://github.com/vllm-project/vllm/issues/47421)
- **Repository:** vllm-project/vllm @ `25fcb65d51deef0026aa34e6067703da4a91f956`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspected the Qwen3-ASR realtime buffer in the checked-out vLLM source.
2. Ran a source-level simulation of the realtime buffer with 10 seconds of audio.
3. Observed that the buffer emits two 5-second segments, which matches the current implementation rather than a defect.

## Observed behavior

- codebase/vllm/model_executor/models/qwen3_asr_realtime.py hard-codes segment_duration_s = 5.0 and emits each 5-second audio segment separately.
- A 10-second simulated utterance is split into two 5-second segments by the same buffer logic.
- The upstream issue comment says 5-second chunks may need post-processing to merge them.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported behavior is expected from the current realtime implementation: it intentionally chunks audio into 5-second segments, so the 'segmentation' is not reproducible as a bug in this source snapshot. Direct runtime import is also blocked in this environment by an installed CUDA/NCCL torch mismatch.
