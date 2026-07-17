# Reproduction Trajectory — Bug 119: gpytorch

- **Bug report:** [https://github.com/cornellius-gp/gpytorch/issues/2604](https://github.com/cornellius-gp/gpytorch/issues/2604)
- **Repository:** cornellius-gp/gpytorch @ `d501c28`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an ExactGP model and trained it briefly on synthetic sine data.
2. Called model.get_fantasy_model(fantasy_x, fantasy_y) after priming the prediction strategy with a test forward pass.
3. Enabled gpytorch.settings.trace_mode() and invoked torch.jit.trace on the fantasized model wrapper.
4. Observed the trace abort with RuntimeError in exact_prediction_strategies.py at test_train_covar.matmul(precomputed_cache).

## Observed behavior

- torch.jit.trace fails after fantasization with RuntimeError: Cannot insert a Tensor that requires grad as a constant.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
