# Reproduction Trajectory — Bug 099: rotary-embedding-torch

- **Bug report:** [https://github.com/lucidrains/rotary-embedding-torch/issues/24](https://github.com/lucidrains/rotary-embedding-torch/issues/24)
- **Repository:** lucidrains/rotary-embedding-torch @ `cd0971297a26ec557ad0c65a6d9e4e1ffca8ae89`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a CUDA float16 tensor and call `RotaryEmbedding(dim=32).cuda().rotate_queries_or_keys(...)`; this completes successfully.
2. Create the same tensor shape, cast it to `torch.float8_e4m3fn`, and call the same method.
3. Observe the immediate `NotImplementedError` from `torch.arange(..., dtype=torch.float8_e4m3fn)`.

## Observed behavior

- fp16 input succeeds: `dtype=torch.float16, output_dtype=torch.float16, finite=True`.
- fp8 input fails in `RotaryEmbedding.rotate_queries_or_keys()` with `NotImplementedError: "arange_cuda" not implemented for 'Float8_e4m3fn'`.
- The exception is raised from `codebase/rotary_embedding_torch/rotary_embedding_torch.py:152` inside `get_seq_pos()`, which is reached from `rotate_queries_or_keys()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
