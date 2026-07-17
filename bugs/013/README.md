# Bug 013

Reproduction bundle for TensorFlow Models issue 11087.

The bug is an import-time Matplotlib backend override in
`codebase/official/vision/utils/object_detection/visualization_utils.py`.
That module calls `matplotlib.use('Agg')` while it is being imported, which
changes the global backend away from an interactive backend.

This bundle reproduces the backend flip by executing the real source file with
small import stubs. The current Python 3.12 environment cannot reliably import
the historical TensorFlow wheel stack used by the 2023 codebase, so the repro
isolates the import-time side effect without mutating application code.

Run:

```bash
bash setup_env.sh
bash run_repro.sh
```

Expected output:

```text
before=svg
after=Agg
```

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

