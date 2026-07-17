# Bug 326 Reproduction

This folder reproduces Pyro issue 3314, where mypy reports missing implementations or stubs for `pyro` imports.

## What it does

`repro.py` installs the local `codebase/` package in editable mode without dependencies, then runs mypy on an external file that imports:

- `pyro`
- `pyro.distributions`
- `pyro.infer`
- `pyro.infer.autoguide`
- `pyro.optim`

The bug is reproduced when mypy emits `import-not-found` errors for those modules.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The run stores stdout in `repro_stdout.log` and stderr in `repro_stderr.log`, then writes the summary to `reproduction.json`.
