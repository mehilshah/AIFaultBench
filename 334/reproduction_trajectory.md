# Reproduction Trajectory — Bug 334: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/3485](https://github.com/huggingface/accelerate/issues/3485)
- **Repository:** huggingface/accelerate @ `63168b151fa15987064a22c77b8b8ec72946f54e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a CPU-only Python 3.12 virtual environment and install torch from the PyTorch CPU wheel index plus the runtime dependencies needed by accelerate.
2. Run `torchrun --standalone --nproc-per-node=2 repro.py` with `PYTHONPATH=codebase/src` so the local accelerate source tree is exercised.
3. Observe that the gathered completions contain duplicated entries and do not match the expected four-item list.

## Observed behavior

- Running the 2-process launcher on the local source tree produced {"expected": ["cpu: 0", "cpu: 1", "cpu: 2", "cpu: 3"], "gathered": ["cpu:0: 0", "cpu:0: 1", "cpu:0: 0", "cpu:0: 1", "cpu:0: 2", "cpu:0: 3", "cpu:0: 2", "cpu:0: 3"], "matches_expected": false}, showing duplicated padded output.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
