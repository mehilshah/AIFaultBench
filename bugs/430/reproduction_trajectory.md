# Reproduction Trajectory — Bug 430: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3203](https://github.com/pyro-ppl/pyro/issues/3203)
- **Repository:** pyro-ppl/pyro @ `dd4e0f81b4ddceb82ebd663b20333e175ce27c2a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install `torch==2.13.0+cpu` from the PyTorch CPU wheel index.
2. Run `repro.py`, which deletes `torch.distributions.constraints._CorrCholesky` to mimic the upstream PyTorch API removal.
3. Import `codebase/pyro/distributions/torch_patch.py` directly from the target commit worktree.

## Observed behavior

- Running `bash run_repro.sh` in the prepared venv loads `codebase/pyro/distributions/torch_patch.py` from commit `dd4e0f81b4ddceb82ebd663b20333e175ce27c2a` and crashes with `AttributeError: module 'torch.distributions.constraints' has no attribute '_CorrCholesky'`. The traceback points to the `@patch_dependency("torch.distributions.constraints._CorrCholesky.check")` decorator in `torch_patch.py:74`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
