# Reproduction Trajectory — Bug 514: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7770](https://github.com/deepspeedai/DeepSpeed/issues/7770)
- **Repository:** microsoft/DeepSpeed @ `816e4aef49c3f30186d65a007480bb5d4a94d17f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local venv and install dependencies with `./setup_env.sh`.
2. Run the repro with `./run_repro.sh`.

## Observed behavior

- Eager `torch.nn.functional.cross_entropy` succeeded at shape (8192, 4096) with `eager_loss=8.824750`.
- The decomposed FX backward graph contains the dense intermediates reported in the bug, including `full_like`, `scatter`, `mul`, `exp`, and `sub`.
- After lowering the memory cap to 1000 MB, executing the FX graph failed with `RuntimeError: DefaultCPUAllocator: can't allocate memory: you tried to allocate 134217728 bytes`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```
