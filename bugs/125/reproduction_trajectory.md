# Reproduction Trajectory — Bug 125: stable_baselines3

- **Bug report:** [https://github.com/DLR-RM/stable-baselines3/issues/2175](https://github.com/DLR-RM/stable-baselines3/issues/2175)
- **Repository:** DLR-RM/stable-baselines3 @ `7883ed4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment and installed the bug-specific runtime dependencies.
2. Ran `bash run_repro.sh` against the local `codebase/` snapshot.
3. Observed PPO finish with `final_num_timesteps=2` after being asked to train for `total_timesteps=1`.

## Observed behavior

- In the local run, `repro.py` reported `stable_baselines3_version=2.7.1a2`, `total_timesteps=1`, and `final_num_timesteps=2`, then printed `BUG_REPRODUCED: learn() overshot total_timesteps`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
