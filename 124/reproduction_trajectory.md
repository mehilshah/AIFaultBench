# Reproduction Trajectory — Bug 124: stable-baselines3

- **Bug report:** [https://github.com/DLR-RM/stable-baselines3/issues/2172](https://github.com/DLR-RM/stable-baselines3/issues/2172)
- **Repository:** DLR-RM/stable-baselines3 @ `f7a89e1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a venv and install the bug-specific runtime dependencies from requirements.txt.
2. Run bash run_repro.sh, which loads stable_baselines3/common/env_checker.py from the local codebase without executing the package __init__ side effects.
3. Observe the nested Sequence cases fail in check_env while the top-level Sequence cases pass.

## Observed behavior

- Running bash run_repro.sh against the local codebase reproduces the checker failures for nested Sequence spaces: Dict+Sequence(stack=False) raises AssertionError about a tuple observation, Dict+Sequence(stack=True) raises AssertionError about shape None vs (3, 1), Tuple+Sequence raises TypeError: 'NoneType' object is not iterable from DummyVecEnv, and OneOf+Sequence(stack=False/True) raises AssertionError that the reset observation is a tuple. The successful top-level Sequence cases pass.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
