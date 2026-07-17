# Bug 570

This folder contains a minimal reproduction for the QwenImage Ulysses context-parallel mask bug.

## What the repro checks

The local `QwenImageTransformer2DModel` builds a joint text+image attention mask, then runs the model with
context parallelism enabled via `ContextParallelConfig(ulysses_degree=2)`.

The reported issue is that a non-contiguous `encoder_hidden_states_mask` is not sharded correctly for Ulysses SP,
so the SP output diverges from the non-SP output.

## Files

- `bug_report.txt`: original issue report
- `codebase/`: local diffusers source snapshot
- `repro.py`: minimal distributed repro
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local venv and installs dependencies
- `run_repro.sh`: runs the repro script
- `manifest.json`: metadata for the standardized bundle
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured command output

## Run

```bash
bash run_repro.sh
```

The script exits non-zero because `torch.testing.assert_close` fails on the SP and non-SP outputs.
