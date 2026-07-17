# Reproduction Trajectory — Bug 162: unknown

- **Bug report:** [https://github.com/jupyter/docker-stacks/issues/2138](https://github.com/jupyter/docker-stacks/issues/2138)
- **Repository:** jupyter/docker-stacks @ `0098788`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` in the bug folder.
2. The script invokes `docker pull quay.io/jupyter/scipy-notebook:hub-4.1.6`.
3. Docker returns `not found` for the requested tag.

## Observed behavior

- docker pull quay.io/jupyter/scipy-notebook:hub-4.1.6 failed with exit code 1 and stderr reported `quay.io/jupyter/scipy-notebook:hub-4.1.6: not found`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
