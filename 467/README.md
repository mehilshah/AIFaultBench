# Accelerate unwrap_model repro

This bundle reproduces the bug from `huggingface/accelerate` at commit `901ab69a1601ba1a7c63523356c5acb1d66b7ea9`.

## Setup

```bash
bash setup_codebase.sh
bash setup_env.sh
```

## Reproduction

```bash
bash run_repro.sh
cat repro_stdout.log
cat repro_stderr.log
```

The script expects `Accelerator.unwrap_model()` to return the original `ToyModel`, but the buggy version returns the `torch.compile` wrapper instead.
