# Bug 128 Reproduction

This folder reproduces Codon issue [#652](https://github.com/exaloop/codon/issues/652): `pyext`
compilation fails when a Codon function returns or accepts `np.ndarray`.

## What fails

Running the repro command on the local Codon 0.19.6 installation fails with:

`internal.codon:174 (36-49): error: 'Ptr[float32]' object has no attribute '__to_py__'`

The failure occurs while realizing `to_py(slf: ndarray[float32,1])` during Python-extension
wrapper generation.

## Repro steps

1. Run `bash setup_env.sh`.
1. Run `bash run_repro.sh`.
1. Inspect `repro_stdout.log` and `repro_stderr.log` for the compiler diagnostic.

## Files

- `repro.codon`: minimal Codon source that triggers the bug.
- `repro.py`: driver that invokes `codon build -pyext`.
- `run_repro.sh`: captures stdout/stderr into the checked-in log files.
- `reproduction.json`: machine-readable reproduction result.

