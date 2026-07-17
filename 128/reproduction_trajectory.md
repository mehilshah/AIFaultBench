# Reproduction Trajectory — Bug 128: codon

- **Bug report:** [https://github.com/exaloop/codon/issues/652](https://github.com/exaloop/codon/issues/652)
- **Repository:** exaloop/codon @ `dcb41dc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ensure Codon is available via `codon` or `~/.codon/bin/codon`.
2. Run `bash run_repro.sh`.
3. Observe the pyext build fail while generating wrappers for `ndarray[float32,1]`.

## Observed behavior

- Running `bash run_repro.sh` reproduces the compiler failure: `internal.codon:174 (36-49): error: 'Ptr[float32]' object has no attribute '__to_py__'`, followed by `during the realization of to_py(slf: ndarray[float32,1])` and `__to_py__(self: ndarray[float32,1])`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
