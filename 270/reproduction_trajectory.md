# Reproduction Trajectory — Bug 270: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/3877](https://github.com/huggingface/accelerate/issues/3877)
- **Repository:** huggingface/accelerate @ `b9ca0de682f25f15357a3f9f1a4d94374a1d451d`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local venv and installed the CUDA 12.8 PyTorch stack plus accelerate, deepspeed, transformers, datasets, and trl.
2. Ran the reported TRL SFT training path twice under DeepSpeed ZeRO-2: once with batch_size=2 and gradient_accumulation_steps=4, and once with batch_size=8 and gradient_accumulation_steps=1.
3. Compared the resulting loss histories and found no meaningful divergence in this environment.

## Observed behavior

- The exact TRL SFT path from the issue report ran successfully under DeepSpeed ZeRO-2, but the two comparable settings stayed aligned: batch_size=2 with gradient_accumulation_steps=4 produced train_loss=11.920878887176514, and batch_size=8 with gradient_accumulation_steps=1 produced train_loss=11.920918822288513. The absolute train loss delta was 3.993511199951172e-05 and the maximum per-step loss delta was 0.00014019012451171875, which is within floating-point noise for this short run.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported zero-2-only loss divergence is not reproducible on this machine with the tested stack; both comparable SFT runs matched to within 1e-4 over 8 optimizer steps.
