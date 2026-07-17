# Reproduction Trajectory — Bug 345: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38969](https://github.com/jax-ml/jax/issues/38969)
- **Repository:** jax-ml/jax @ `7b6de017d4ca3f405d630eb59ec6c111cf7ded4c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a venv and installed argparse==1.4.0.
2. Forced the venv site-packages ahead of stdlib with PYTHONPATH.
3. Ran codebase/build/build.py --help and observed the TypeError from parser.add_subparsers(dest='command', required=True).

## Observed behavior

- With argparse imported from .venv/lib/python3.12/site-packages/argparse.py, running codebase/build/build.py --help fails at parser.add_subparsers(dest="command", required=True) with TypeError: _SubParsersAction.__init__() got an unexpected keyword argument 'required'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
