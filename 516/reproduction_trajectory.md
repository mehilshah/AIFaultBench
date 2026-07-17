# Reproduction Trajectory — Bug 516: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3315](https://github.com/pytorch/rl/issues/3315)
- **Repository:** pytorch/rl @ `5e89e4e7c99a3d3122387548058d4ea20baca926`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated Python 3.12 venv with the dependencies from requirements.txt.
2. Run PYTHONNOUSERSITE=1 PYTHONPATH=codebase bash run_repro.sh.
3. Observe that centralized shared-parameter execution duplicates the agent dimension in the output shape.

## Observed behavior

- In a clean venv with torch==2.5.1+cpu and tensordict==0.10.0, running the minimal MultiAgentNetBase example printed input_shape=(4, 3, 2) and output_shape=(4, 3, 3, 4), then failed the expected-shape assertion with AssertionError: Expected output shape (4, 3, 4), got (4, 3, 3, 4).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
