# Reproduction Trajectory — Bug 589: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3246](https://github.com/pytorch/rl/issues/3246)
- **Repository:** pytorch/rl @ `7e0968aa621c0b67313b3f5db09d931baf8a1b3b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment with `setup_env.sh` and install `hydra-core`.
2. Load `torchrl.trainers.algorithms.configs.transforms` through a stub package namespace so `torchrl.__init__` is not imported.
3. Call `InitTrackerConfig(init_key='is_test_init')`.
4. Observe the constructor raise `TypeError` because the dataclass still exposes `in_keys` and `out_keys` instead of `init_key`.

## Observed behavior

- Running the harness in a clean local venv prints `InitTrackerConfig signature: (in_keys: 'list[str] | None' = None, out_keys: 'list[str] | None' = None, _target_: 'str' = 'torchrl.envs.transforms.transforms.InitTracker') -> None` and then fails with `TypeError: InitTrackerConfig.__init__() got an unexpected keyword argument 'init_key'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
