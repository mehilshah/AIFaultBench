# Reproduction Trajectory — Bug 101: rotary-embedding-torch

- **Bug report:** [https://github.com/lucidrains/rotary-embedding-torch/issues/8](https://github.com/lucidrains/rotary-embedding-torch/issues/8)
- **Repository:** lucidrains/rotary-embedding-torch @ `22cac59a55ae25cd06b4522d891278aedd929184`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv and installed torch==2.13.0 and einops==0.8.2.
2. Ran repro.py against the local codebase with RotaryEmbedding(dim=32, use_xpos=True).
3. Confirmed that seq_len=64 stays finite, but seq_len=96 makes k non-finite.

## Observed behavior

- With torch=2.13.0+cu130, RotaryEmbedding(dim=32, use_xpos=True) on all-ones tensors produces finite q and non-finite k at seq_len=96; the repro prints {'seq_len': 96, 'k_finite': False, 'k_nan': True, 'k_inf': True, 'k_non_finite_count': 91}.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
