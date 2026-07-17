# Reproduction Trajectory — Bug 184: ludwig

- **Bug report:** [https://github.com/ludwig-ai/ludwig/issues/3092](https://github.com/ludwig-ai/ludwig/issues/3092)
- **Repository:** ludwig-ai/ludwig @ `05a1a60`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create the local Python environment with `bash setup_env.sh`.
2. Run the packaged reproducer with `bash run_repro.sh`.
3. Confirm that the GBM TorchScript conversion on CUDA completes without a Hummingbird device-mismatch error.

## Observed behavior

- Running `bash run_repro.sh` completes successfully in this checkout.
- `repro_stdout.log` ends with `CUDA available: True` and `TorchScript conversion succeeded: TopLevelTracedModule`.
- `repro_stderr.log` only contains a TorchScript tracer warning, not the reported CPU/CUDA device mismatch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported CUDA device-mismatch did not reproduce here; the direct GBM-to-TorchScript conversion path succeeds.
