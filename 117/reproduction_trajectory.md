# Reproduction Trajectory — Bug 117: clearml

- **Bug report:** [https://github.com/clearml/clearml/issues/1268](https://github.com/clearml/clearml/issues/1268)
- **Repository:** clearml/clearml @ `3094d57`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the local ClearML source from codebase/ into a virtualenv.
2. Run `python repro.py multiply --x 2 --y 10 --verbose`.
3. Observe the TypeError raised from clearml/binding/frameworks/__init__.py while Fire is resolving the command.

## Observed behavior

- stderr contains the ClearML Fire patch failure: PatchFire.__CallAndUpdateTrace() missing 1 required positional argument: 'target'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
