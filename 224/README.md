# Bug 224 Reproduction

This folder contains a standalone reproduction of ART issue 2473.

## Bug summary

`art/estimators/object_detection/pytorch_object_detector.py` parses `torchvision.__version__` with:

```python
list(map(int, torchvision.__version__.lower().split("+", maxsplit=1)[0].split(".")))
```

That fails for versions with a pre-release segment such as `0.18.1a0+405940f`.

## Files

- `bug_report.txt`: original report
- `codebase/`: local source snapshot
- `repro.py`: minimal failing reproduction
- `requirements.txt`: minimal environment dependencies
- `setup_env.sh`: environment bootstrap
- `run_repro.sh`: reproduction launcher
- `reproduction.json`: schema-constrained result
- `repro_stdout.log` / `repro_stderr.log`: captured command output

## Reproduction command

```bash
bash run_repro.sh
```

