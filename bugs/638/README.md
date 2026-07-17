# Bug 638

This folder reproduces DeepSpeed issue 7686.

The bug report describes a ZeRO stage 3 ZenFlow crash where `param.ds_shape`
remains 2D but `param.ds_tensor.data` is accidentally a 0-d scalar. The
reproduction in [`repro.py`](./repro.py) injects that exact corrupted state and
calls `ZenFlowSelectiveAdamW_stage3.group_step()`, which fails at:

```text
RuntimeError: narrow() cannot be applied to a 0-dim tensor
```

## Files

- [`bug_report.txt`](./bug_report.txt): original report
- [`codebase/`](./codebase): local DeepSpeed source snapshot
- [`repro.py`](./repro.py): minimal failing harness
- [`requirements.txt`](./requirements.txt): runtime dependencies
- [`setup_env.sh`](./setup_env.sh): creates a local venv and installs deps
- [`run_repro.sh`](./run_repro.sh): runs the repro and captures logs
- [`reproduction.json`](./reproduction.json): schema-constrained result

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The run is expected to exit non-zero and write the traceback to
`repro_stderr.log`.
