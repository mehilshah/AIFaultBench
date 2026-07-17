# Bug 564

Reproduction bundle for NumPyro issue 2022.

## Contents

- `bug_report.txt`: recovered issue report
- `codebase/`: local NumPyro source snapshot
- `repro.py`: standalone reproduction script
- `requirements.txt`: minimal runtime dependencies
- `setup_env.sh`: installs dependencies for the repro
- `run_repro.sh`: runs the reproduction
- `manifest.json`: machine-readable metadata for the bundle
- `reproduction.json`: final reproduction verdict
- `repro_stdout.log`, `repro_stderr.log`: captured command output

## Repro Summary

The bug is triggered by `numpyro.contrib.module.random_nnx_module` when an
`flax.nnx.Module` stores submodules in a Python list. The recursive parameter
path builder in `_update_params` tries to join a string prefix with an integer
list index and raises `TypeError`.

## How to Run

```bash
bash setup_env.sh
bash run_repro.sh
```

Or build the container:

```bash
```
