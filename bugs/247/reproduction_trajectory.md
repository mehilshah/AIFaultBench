# Reproduction Trajectory — Bug 247: pyro-ppl

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3374](https://github.com/pyro-ppl/pyro/issues/3374)
- **Repository:** pyro-ppl/pyro @ `64e71ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create `.venv` and install the runtime dependencies.
2. Run `bash run_repro.sh` from the bug folder.
3. Inspect `repro_stdout.log` and `repro_stderr.log` for the missing-handler failure.

## Observed behavior

- With an isolated CPU-only Torch venv, the repro prints `has pyro.poutine.equalize: False` and then fails at `pyro.poutine.equalize(model, ["dogs_std", "cats_std"])` with `AttributeError: module 'pyro.poutine' has no attribute 'equalize'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
