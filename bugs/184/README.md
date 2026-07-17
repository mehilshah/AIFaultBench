# Bug 184 Reproduction Bundle

This folder packages the Ludwig GBM / Hummingbird CUDA report from
`bug_report.txt` together with a direct reproducer.

## What the repro does

`repro.py`:

1. Loads the Auto MPG dataset from the bug report.
2. Builds the same GBM regression schema.
3. Fits a tiny LightGBM regressor.
4. Converts the Ludwig GBM wrapper to TorchScript on CUDA.

## Outcome in this checkout

The reported CPU/CUDA tensor mismatch did not reproduce here. The TorchScript
conversion completed successfully.

## How to run

1. Create the environment:
   `bash setup_env.sh`
2. Run the repro:
   `bash run_repro.sh`

The script writes:

- `repro_stdout.log`
- `repro_stderr.log`

## Notes

- `repro.py` stubs `torchtext` because the wheel is not usable in this
  environment, but the GBM conversion path does not depend on it.
- The checked-in `codebase/` is left unchanged.
