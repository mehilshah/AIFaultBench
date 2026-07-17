# Bug 104 Reproduction Bundle

This folder reproduces [vector-quantize-pytorch issue #160](https://github.com/lucidrains/vector-quantize-pytorch/issues/160).

Bug summary:
- `ResidualVQ` initializes `MLP` modules even when `implicit_neural_codebook=False`.

Files:
- `bug_report.txt`: recovered issue report
- `codebase/`: local source snapshot used for the repro
- `repro.py`: minimal failing script
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: installs the runtime dependencies
- `run_repro.sh`: runs the repro and captures stdout/stderr
- `manifest.json`: metadata for the standardized bundle

Repro command:
```bash
bash run_repro.sh
```

Expected result:
- The script raises an `AssertionError` because `ResidualVQ.mlps` is non-empty even when `implicit_neural_codebook=False`.
