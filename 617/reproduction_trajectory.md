# Reproduction Trajectory — Bug 617: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/2833](https://github.com/pyro-ppl/pyro/issues/2833)
- **Repository:** pyro-ppl/pyro @ `0c7884dd6c06a8457a0696126f32d7ce7f404945`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.9 virtualenv with torch 1.8.1+cpu and NumPy < 2.
2. Install the local Pyro codebase in editable mode.
3. Run `python repro.py`, which constructs a zero-element covariance tensor and passes it to `pyro.distributions.MultivariateNormal`.
4. Observe the reshape failure in `pyro/distributions/torch_patch.py`.

## Observed behavior

- Running `bash run_repro.sh` in the prepared Python 3.9 virtualenv raises `RuntimeError: cannot reshape tensor of 0 elements into shape [-1, 0, 0] because the unspecified dimension size -1 can be any value and is ambiguous` from `pyro/distributions/torch_patch.py:_PositiveDefinite_check` while constructing `dist.MultivariateNormal(mean, covariance)` with `covariance.shape == (3, 0, 0)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
