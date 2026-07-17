# Reproduction Trajectory — Bug 282: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/39145](https://github.com/jax-ml/jax/issues/39145)
- **Repository:** jax-ml/jax @ `3147de52286b807368fd9429844e50e16d8d7cc7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtual environment and installed the pinned GPU release from requirements.txt: jax[cuda12]==0.10.2.
2. Ran bash run_repro.sh, which sets XLA_PYTHON_CLIENT_ALLOCATOR=platform and executes repro.py.
3. Observed the process GPU usage remain elevated after del + gc and end at 6652 MiB instead of returning near the 580 MiB baseline.

## Observed behavior

- On jax 0.10.2 with XLA_PYTHON_CLIENT_ALLOCATOR=platform, the repro process used about 580 MiB at baseline, stayed at 1610 MiB after deleting a 1 GiB array and running gc.collect(), and climbed to 6652 MiB after the vmap scratch loop. That is consistent with the reported allocator retention/regression.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
