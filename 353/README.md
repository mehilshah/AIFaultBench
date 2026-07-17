# Bug 353 Reproduction Bundle

Issue: ROCm 7.0 compatibility failure in `timm.layers.Attention2d` and `timm.layers.MultiQueryAttention2d`.

## What this bundle does

- Sets up an isolated Python environment with a CPU torch build.
- Exercises the same attention forward paths described in the report.
- Records whether ROCm is available locally.

## Why the issue is not reproducible here

The reported failure requires an AMD ROCm runtime. This machine does not expose ROCm, so the HIP-specific `invalid argument` error cannot be triggered locally.

## Files

- `repro.py`: minimal forward-pass harness.
- `requirements.txt`: isolated runtime dependencies.
- `setup_env.sh`: creates `.venv` and installs requirements.
- `run_repro.sh`: runs the repro inside the venv.
- `reproduction.json`: final schema-constrained result.
- `repro_stdout.log` / `repro_stderr.log`: captured run output.

## Reproduce

```bash
bash setup_env.sh
bash run_repro.sh
```
