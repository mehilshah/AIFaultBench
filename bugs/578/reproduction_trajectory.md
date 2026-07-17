# Reproduction Trajectory — Bug 578: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/2935](https://github.com/pyro-ppl/pyro/issues/2935)
- **Repository:** pyro-ppl/pyro @ `43dbb2e67331bd3aa6c73bb5483825432a8b7145`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Imported the standardized Pyro 1.7.0 codebase under Torch 1.13.1+cpu.
2. Checked whether CUDA is available before running the reported snippet.

## Observed behavior

- pyro=1.7.0; torch=1.13.1+cpu; cuda_available=False

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This machine has no CUDA device, so the reported torch.rand(3).cuda() input cannot be created here.
