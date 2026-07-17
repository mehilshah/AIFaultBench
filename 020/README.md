# Reproduction Bundle

## Bug

`tf-models-official==2.12.0` fails on Python 3.8 when `official/core/base_trainer.py`
reaches the evaluation log merge at line 442:

`return passthrough_logs | logs`

That operator is only valid for dictionary merging on Python 3.9 and newer.

## How to run

```bash
bash run_repro.sh
```

## Expected result

Python 3.8 raises:

`TypeError: unsupported operand type(s) for |: 'dict' and 'dict'`

## Notes

The reproduction uses the local `codebase/` copy to point at the exact source
line reported in the issue and executes the same failure mode under a Python 3.8
container.
