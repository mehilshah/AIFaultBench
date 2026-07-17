# Reproduction Trajectory — Bug 538: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3291](https://github.com/pytorch/rl/issues/3291)
- **Repository:** pytorch/rl @ `ab35c364cbebea9267bbe50b6e6cafab0768b249`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a 2D BoundedContinuous action spec.
2. Build a minimal SACLoss with that action spec.
3. Read target_entropy and compare it to the expected -dim(A) value.

## Observed behavior

- repro.py prints observed_target_entropy=-1.0 and expected_target_entropy=-2.0 for a 2D BoundedContinuous action spec, then exits with code 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
