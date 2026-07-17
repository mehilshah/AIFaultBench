# Reproduction Trajectory — Bug 135: deepvariant

- **Bug report:** [https://github.com/google/deepvariant/issues/830](https://github.com/google/deepvariant/issues/830)
- **Repository:** google/deepvariant @ `b4e87ce`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash run_repro.sh` from the standardized bug folder.
2. The script fetched the Docker Hub manifest for `google/deepvariant:1.6.1`.
3. The script fetched the image config blob and extracted `config.Env`.
4. The config reported `VERSION=1.6.0` instead of the expected `1.6.1`.
5. The script exited with status 1 to flag the mismatch.

## Observed behavior

- On 2026-07-17, `bash run_repro.sh` inspected the Docker Hub metadata for `google/deepvariant:1.6.1` and reported `Image VERSION env: 1.6.0`, with stderr `Mismatch reproduced: google/deepvariant:1.6.1 advertises VERSION=1.6.0`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
