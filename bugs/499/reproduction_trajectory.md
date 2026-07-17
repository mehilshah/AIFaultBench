# Reproduction Trajectory — Bug 499: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21561](https://github.com/Lightning-AI/pytorch-lightning/issues/21561)
- **Repository:** Lightning-AI/pytorch-lightning @ `92a54747aa40273b07a1c15a25a486bb4b37f13d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- repro_stdout.log contains caught_runtime_error=1 and the Lightning message: 'Lightning can't create new processes if CUDA is already initialized.'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
