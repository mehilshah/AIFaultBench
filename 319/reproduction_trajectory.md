# Reproduction Trajectory — Bug 319: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7942](https://github.com/deepspeedai/DeepSpeed/issues/7942)
- **Repository:** microsoft/DeepSpeed @ `2f0924a55de959f88d09451b19b1dac20ac4301a`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a tiny embedding model with weight shape (8, 4).
2. Flattened embed_tokens.weight to (32,) to simulate the bad DeepCompile shape.
3. Forward pass raised: RuntimeError: 'weight' must be 2-D

## Observed behavior

- Flattening the embedding weight to 1-D reproduces the same low-level failure here: 'weight' must be 2-D

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The full DeepCompile/Qwen2Moe stack is not runnable in this machine; the bundled fallback only reproduces the embedding-shape failure mode.
