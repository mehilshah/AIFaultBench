# Reproduction Bundle

This folder reproduces the `numpyro` import failure caused by a missing runtime dependency.

## What fails

`numpyro/_typing.py` imports `typing_extensions` at import time, but `setup.py` does not declare
`typing_extensions` in `install_requires`.

## How to run

```bash
bash run_repro.sh
```

The run creates a fresh virtual environment, installs the package dependencies listed in
`requirements.txt`, installs the local `codebase/` package, and then imports `numpyro`.

## Expected result

The import fails with:

```text
ModuleNotFoundError: No module named 'typing_extensions'
```

## Notes

The repro intentionally does not install `typing_extensions`, because that is the missing package
the bug report is about.
