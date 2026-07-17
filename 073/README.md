# Reproduction Bundle

Bug report: DeepSpeedExamples issue 940, `Failed to run Domino example`.

The reported failure is an `AttributeError: 'NoneType' object has no attribute 'all_reduce'` caused by DeepSpeed's communication backend `cdb` not being initialized before `all_reduce()` is called.

This bundle keeps the original `codebase/` intact and provides a distilled repro in `repro.py` that matches the failing code path.

## Run

```bash
bash run_repro.sh
```

## Files

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
