# Reproduction Trajectory — Bug 493: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3156](https://github.com/pyro-ppl/pyro/issues/3156)
- **Repository:** pyro-ppl/pyro @ `8b7e5641228b664b3c9b674a079e95a478f3e2a0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated virtualenv and install the pinned CPU PyTorch wheel plus Pyro's runtime dependencies.
2. Patch `torch.__version__` to a 1.x string before importing the bundled Pyro snapshot so the old `torch_patch.py` import guard is satisfied.
3. Instantiate `HMC` with a potential function that evaluates to NaN, run `setup(1)`, and call `_find_reasonable_step_size()` on a one-site latent dict.
4. Observe that the call hangs until the wrapper timeout kills it.

## Observed behavior

- The repro reaches `setup done nan` and `call start`, then `_find_reasonable_step_size()` does not return before the 5s wrapper timeout. The captured stdout ends with `result=timeout` and `exit_status=124`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
