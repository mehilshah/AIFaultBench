# Reproduction Trajectory — Bug 200: cibuildwheel

- **Bug report:** [https://github.com/pypa/cibuildwheel/issues/2659](https://github.com/pypa/cibuildwheel/issues/2659)
- **Repository:** pypa/cibuildwheel @ `f6c8108`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. ./setup_env.sh
2. ./run_repro.sh

## Observed behavior

- run_repro.sh exits with code 1.
- repro_stderr.log shows KeyError: 'ApiVersion' at cibuildwheel/oci_container.py:123.
- The KeyError is wrapped as OCIEngineTooOldError with the message 'Build failed because docker is too old or is not working properly.'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
