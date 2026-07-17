# Reproduction Trajectory — Bug 123: stable_baselines3

- **Bug report:** [https://github.com/DLR-RM/stable-baselines3/issues/2119](https://github.com/DLR-RM/stable-baselines3/issues/2119)
- **Repository:** DLR-RM/stable-baselines3 @ `d35597f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv and installed the minimal runtime dependencies from `requirements.txt`.
2. Loaded the local Stable-Baselines3 source files directly from `codebase/` while stubbing only torch-dependent modules that are unrelated to the bug path.
3. Executed `make_vec_env(TinyContinuousEnv, n_envs=1, wrapper_class=gym.wrappers.ClipAction)` and observed the unbounded action space `Box(-inf, inf, (2,), float32)`.

## Observed behavior

- Running `bash run_repro.sh` from a clean state installs the lightweight runtime deps and prints `Box(-inf, inf, (2,), float32)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
