# Reproduction Trajectory — Bug 634: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46693](https://github.com/huggingface/transformers/issues/46693)
- **Repository:** huggingface/transformers @ `0a4d1c8bac38208fb5b424a510b8a9cef149d1ee`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a venv and installed the minimal runtime dependencies from requirements.txt.
2. Ran `bash run_repro.sh` to inspect the local source and execute the proxy benchmark.
3. Captured stdout in repro_stdout.log and stderr in repro_stderr.log.

## Observed behavior

- codebase/src/transformers/modeling_flash_attention_utils.py still returns `seqlens_in_batch.max()` without `.item()` in both `_unpad_input()` and `_get_unpad_data()`.
- run_repro.sh reported `flash_attn is unavailable in this environment`, so the upstream CUDA/FlashAttention 2 path could not be exercised here.
- The CPU proxy benchmark showed the tensor-valued path is materially slower than the int-valued path in this snapshot (about 5x in the recorded run).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The full reproducer requires a usable CUDA + FlashAttention 2 environment, which is not available in this folder; the local runtime only supports a CPU-side proxy check.
