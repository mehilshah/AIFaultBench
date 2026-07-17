# Reproduction Trajectory — Bug 539: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3032](https://github.com/pyro-ppl/pyro/issues/3032)
- **Repository:** pyro-ppl/pyro @ `f4fafc5c7fa0dc5a377ceb06ec59a234bf3ac465`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python 3.9 virtual environment.
2. Installed the pinned repro dependencies from requirements.txt.
3. Ran repro.py via run_repro.sh and observed the expected TypeError.

## Observed behavior

- Under Python 3.9.25 with torch 1.9.0+cpu, `torch.meshgrid(xs, ys, indexing='xy')` failed with `TypeError: meshgrid() got an unexpected keyword argument 'indexing'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
