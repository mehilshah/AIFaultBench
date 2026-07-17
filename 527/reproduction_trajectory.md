# Reproduction Trajectory — Bug 527: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3061](https://github.com/pyro-ppl/pyro/issues/3061)
- **Repository:** pyro-ppl/pyro @ `a98bb57e1704997a3e01c76a7820c0b1db909ee3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install no extra dependencies; the repro uses a stubbed in-memory `torch` module.
2. Run `bash run_repro.sh` from the standardized bug folder.
3. Observe the traceback in `repro_stderr.log` and the missing `_CorrCholesky` marker in `repro_stdout.log`.

## Observed behavior

- Running `bash run_repro.sh` reproduces the import-time crash in `codebase/pyro/distributions/torch_patch.py`: `AttributeError: module 'torch.distributions.constraints' has no attribute '_CorrCholesky'` at the `@patch_dependency("torch.distributions.constraints._CorrCholesky.check")` decorator.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
