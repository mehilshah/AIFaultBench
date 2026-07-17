# Reproduction Trajectory — Bug 448: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38497](https://github.com/jax-ml/jax/issues/38497)
- **Repository:** jax-ml/jax @ `48f94e65d54b20e86ac68872622f239a89aa33fe`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment.
2. Install pinned dependencies from requirements.txt.
3. Run repro.py with JAX forced to CPU.
4. Observe that the middle two blocks are NaN while the first and last blocks are written correctly.

## Observed behavior

- Verified locally with jax==0.10.1 and jaxlib==0.10.1 on CPU.
- Running the minimal pallas_call repro on shape (1, 512) with grid (1, 4) and block size 128 produced nan_count=256.
- Observed block pattern was ok, nan, nan, ok, matching the issue report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
