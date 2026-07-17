# Bug 229 Reproduction Bundle

This folder reproduces POT issue [#738](https://github.com/PythonOT/POT/issues/738) against the local `codebase/` checkout.

## Result

- Reproducible: `yes`
- Trigger: `ot.wasserstein_circle(sample1, sample2)` changes after adding the same `delta` to both inputs
- Observed on the `p=1` path
- Not reproduced on the `p=2` path for the same inputs

## Files

- `bug_report.txt`: original report
- `codebase/`: local source checkout used for the repro
- `requirements.txt`: minimal runtime/build dependencies
- `setup_env.sh`: creates a clean virtualenv and installs the bundle
- `run_repro.sh`: executes the repro inside that environment
- `repro.py`: the minimal reproduction script
- `manifest.json`: bundle metadata
- `reproduction.json`: schema-constrained result payload
- `repro_stdout.log`, `repro_stderr.log`: captured output from the successful repro run

## Reproduction

```bash
bash run_repro.sh
```

The script exits non-zero when the invariant check fails, which is the expected buggy behavior here.
