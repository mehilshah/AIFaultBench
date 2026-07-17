# Reproduction Trajectory — Bug 423: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1489](https://github.com/huggingface/accelerate/issues/1489)
- **Repository:** huggingface/accelerate @ `7d24bdefb5b3252505151d8c1ac0efbed3574857`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create the local venv and install a working CPU Torch wheel.
2. Run `bash run_repro.sh` to execute `repro.py` against `codebase/src`.
3. Inspect `repro_stdout.log` for the captured launch/config summary.

## Observed behavior

- The local Accelerate CLI parser in this revision does not expose `--rdzv_backend`.
- The simulated multi-node launch path resolves to `rdzv_backend=static` and `rdzv_endpoint=10.13.23.78:7010`.
- Loading the YAML workaround round-trips `rdzv_backend=c10d`, matching the issue report's workaround.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
