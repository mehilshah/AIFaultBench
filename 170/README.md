# Bug 170

Reproduction bundle for Kornia issue `#3464`.

What to run:

```bash
bash run_repro.sh
```

What it checks:

- `RandomThinPlateSpline(p=1.0, same_on_batch=True)` should sample identical TPS control points for every item in a batch.
- The current code samples `dst` per element, so `dst[0] != dst[1]` even though `same_on_batch=True`.

Generated artifacts:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source inputs:

- `bug_report.txt`
- `codebase/`
