# Reproduction Trajectory — Bug 337: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/1999](https://github.com/huggingface/peft/issues/1999)
- **Repository:** huggingface/peft @ `41c274ecac6247a63e3b10f8536904f3ead82213`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local fake 4-bit `bitsandbytes` package and a tiny model that exposes a flattened 1x1 quantized weight while keeping the base forward valid.
2. Instantiated PEFT's 4-bit LoRA wrapper directly with `init_lora_weights=True`, `olora`, and `pissa`.
3. Ran the wrapper on a 2048-wide input and observed that only the `olora` and `pissa` cases crash.

## Observed behavior

- `init_lora_weights=True` runs successfully and returns a tensor with shape [3, 2048].
- `init_lora_weights="olora"` fails on the first forward with `RuntimeError: mat1 and mat2 shapes cannot be multiplied (3x2048 and 1x1)`.
- `init_lora_weights="pissa"` fails with the same runtime error at the same code path in `peft/tuners/lora/bnb.py:489`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
