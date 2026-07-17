# Bug 117

ClearML Fire integration crash from issue [#1268](https://github.com/clearml/clearml/issues/1268).

## Reproduction

1. Run `./run_repro.sh`.
2. The script creates `.venv/`, installs `fire==0.6.0` and the local `codebase/` package, then runs:
   `python repro.py multiply --x 2 --y 10 --verbose`
3. The expected failure is:
   `TypeError: PatchFire.__CallAndUpdateTrace() missing 1 required positional argument: 'target'`

## Generated files

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
