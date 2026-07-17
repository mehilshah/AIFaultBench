# Bug 172

This folder is a self-contained reproduction bundle for the Kornia doc mismatch in
`projections_from_fundamental`.

## What the repro shows

The source docstring for `kornia.geometry.epipolar.projections_from_fundamental`
advertises a return shape of `(*, 4, 4, 2)`, but the implementation returns
`(*, 3, 4, 2)` because it stacks two 3x4 projection matrices.

## Files

- `bug_report.txt`: original issue description
- `codebase/`: local source tree used for the repro
- `repro.py`: minimal checker for the doc/runtime mismatch
- `requirements.txt`: Python dependencies for the repro environment
- `setup_env.sh`: installs the repro dependencies
- `run_repro.sh`: executes the repro and writes logs
- `manifest.json`: machine-readable metadata for the bundle
- `reproduction.json`: schema-constrained result produced after running the repro
- `repro_stdout.log` / `repro_stderr.log`: captured command output

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro succeeds when it prints the documented shape and the actual runtime
shape, then reports that they differ.

