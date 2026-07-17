# Reproduction Trajectory — Bug 185: marimo

- **Bug report:** [https://github.com/marimo-team/marimo/issues/7767](https://github.com/marimo-team/marimo/issues/7767)
- **Repository:** marimo-team/marimo @ `371f3c8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the virtualenv and install requirements with ./setup_env.sh
2. Run ./run_repro.sh with PYTHONPATH pointing at codebase/
3. Inspect repro_stderr.log for the IndexError traceback from mo.ui.tabs({})

## Observed behavior

- Running bash run_repro.sh prints "marimo import ok" to stdout and then fails with IndexError: list index out of range from codebase/marimo/_plugins/ui/_impl/tabs.py:101 when mo.ui.tabs({}) is called.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
