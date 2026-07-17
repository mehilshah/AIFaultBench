# Reproduction Trajectory — Bug 249: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/2328](https://github.com/pytorch/rl/issues/2328)
- **Repository:** pytorch/rl @ `0063741`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtual environment with `setup_env.sh`.
2. Installed the pinned dependencies from `requirements.txt`.
3. Ran `bash run_repro.sh` against the local `codebase/` checkout.
4. Observed the default `MLP` architecture expand to 3 hidden layers instead of a single linear layer.

## Observed behavior

- With torch==2.4.0 and tensordict==0.5.0, `MLP(in_features=1024, out_features=512)` printed `['Linear', 'Tanh', 'Linear', 'Tanh', 'Linear', 'Tanh', 'Linear']` and the repr showed three hidden 32-unit layers before the final 1024->512 linear layer. The repro then failed the assertion against the one-layer expected repr.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
