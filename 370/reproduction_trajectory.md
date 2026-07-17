# Reproduction Trajectory — Bug 370: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3711](https://github.com/pytorch/rl/issues/3711)
- **Repository:** pytorch/rl @ `898298dfcd112c337d44523dd1f28bb6b663c1e4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a fresh .venv and installed torch==2.6.0+cpu, tensordict==0.12.0, numpy, and packaging.
2. Ran bash run_repro.sh with PYTHONPATH pointing at codebase/.
3. Observed that the end of the first trajectory is populated while the final step of the shorter second trajectory remains all zeros.

## Observed behavior

- In a clean CPU-only virtualenv with torch==2.6.0+cpu and tensordict==0.12.0, the repro prints split_step_sum=0.331211 and last_step_sum=0.000000. The final step of the shorter second trajectory has zeroed recurrent_state_h/recurrent_state_c values.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
