# Reproduction Trajectory — Bug 548: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47147](https://github.com/vllm-project/vllm/issues/47147)
- **Repository:** vllm-project/vllm @ `ea9ddf59fc9d262da7467699959d8c84600c073c`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read the bug report and identified the reported mismatch between frontend and backend multimodal cache clearing.
2. Inspected AsyncLLM.pause_generation() and reset_mm_cache() in the local codebase.
3. Ran the source-level reproduction script to verify the renderer cache clear is present before pausing the engine.

## Observed behavior

- codebase/vllm/v1/engine/async_llm.py:750-793 already calls self.renderer.clear_mm_cache_async() before self.engine_core.pause_scheduler_async(...).
- codebase/vllm/v1/engine/async_llm.py:917-919 already clears both frontend and backend multimodal caches in reset_mm_cache().

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The current checkout already contains the fix described in the bug report, so the cache-desync failure cannot be reproduced here.
