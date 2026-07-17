# Reproduction Trajectory — Bug 555: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38098](https://github.com/jax-ml/jax/issues/38098)
- **Repository:** jax-ml/jax @ `eb93eda9fbe95cf21c1501db8b064f66b040bf33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv and installed the source tree from codebase/ with jaxlib==0.10.1.
2. Ran the minimal reproducer at x=[126.0] float32.
3. Observed jit_result=[1.] and eager_result=[0.], matching the issue report.

## Observed behavior

- On the local JAX source tree with jaxlib 0.10.1, repro.py prints jit_result [1.] and eager_result [0.] for x=[126.] and then raises AssertionError.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash ./run_repro.sh
```
