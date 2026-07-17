# Bug 183 Reproduction Bundle

This folder reproduces the `LigerFusedLinearCrossEntropyLoss(reduction='none')` bug from
[`linkedin/Liger-Kernel#488`](https://github.com/linkedin/Liger-Kernel/issues/488).

## What It Shows

The fused linear cross entropy path accumulates per-token losses into a 1D tensor, but the
implementation always returns `torch.sum(loss_1d)`. As a result, `reduction='none'` still returns
a scalar instead of a vector of unreduced losses.

## Files

- `bug_report.txt`: original bug report
- `codebase/`: local source snapshot used for the repro
- `repro.py`: executable reproduction script
- `requirements.txt`: pinned runtime dependencies for the repro
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro and captures stdout/stderr
- `manifest.json`: metadata for the standardized folder
- `reproduction.json`: structured result from the last repro run
- `repro_stdout.log`, `repro_stderr.log`: command output from the last repro run

## Reproduce

```bash
./run_repro.sh
```

The script uses a CPU-only PyTorch install and stubs the Triton kernel so the Python reduction
logic can be exercised without a GPU.
