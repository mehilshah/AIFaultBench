# Reproduction Trajectory — Bug 615: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3242](https://github.com/pytorch/rl/issues/3242)
- **Repository:** pytorch/rl @ `8570c25a745da54ca647b8a70231112f063d1421`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtual environment with `setup_env.sh` and install `torch==2.3.1`, `tensordict==0.10.0`, `gymnasium==1.2.2`, and `numpy>=1.26`.
2. Run `bash run_repro.sh` from the bug folder with `PYTHONPATH` pointing at `codebase/`.
3. Observe that the base GymWrapper spec is incorrectly stacked as a 1D categorical action spec instead of a `MultiCategorical`, then `ActionMask` raises a shape mismatch during `check_env_specs()`.

## Observed behavior

- Running the bundled repro against the local codebase prints an action spec of `Categorical(shape=torch.Size([2]), space=CategoricalBox(n=5))` for `MultiDiscrete([5, 5])`, then `check_env_specs(env_transformed)` fails inside `ActionMask._call()` with `RuntimeError: Cannot expand mask to the desired shape.` The captured logs are in `repro_stdout.log` and `repro_stderr.log`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
