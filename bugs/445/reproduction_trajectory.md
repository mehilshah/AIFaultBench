# Reproduction Trajectory — Bug 445: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3200](https://github.com/pyro-ppl/pyro/issues/3200)
- **Repository:** pyro-ppl/pyro @ `dd4e0f81b4ddceb82ebd663b20333e175ce27c2a`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a Python 3.10 virtual environment.
2. Install torch==2.0.0 and the local editable pyro snapshot from codebase/.
3. Import pyro.optim and check for the ExponentialLR attribute.

## Observed behavior

- Imported pyro.optim from codebase/pyro/optim/__init__.py; pyro.__version__=1.8.4+dd4e0f81; has ExponentialLR=True; attr_type=function.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The standardized snapshot already exposes pyro.optim.ExponentialLR, so the reported AttributeError does not occur here.
