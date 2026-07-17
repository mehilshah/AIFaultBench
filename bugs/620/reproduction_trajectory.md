# Reproduction Trajectory — Bug 620: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/37991](https://github.com/jax-ml/jax/issues/37991)
- **Repository:** jax-ml/jax @ `262e222e5f038161866f02ec21527d66453f487d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the editable codebase plus jaxlib==0.10.0, numpy>=2.0, scipy>=1.14, ml_dtypes>=0.5.0, and opt_einsum.
2. Ran repro.py through run_repro.sh against the local JAX checkout.
3. Compared NumPy cumsum with JAX cumsum on integer input using dtype=bool and observed a mismatch.

## Observed behavior

- After installing the local editable JAX checkout (jax 0.10.1.dev20260717) with jaxlib==0.10.0, the repro prints expected_numpy=[True, True] and actual_jax=[True, False] for input [-1, 1] with dtype=bool, so the results differ exactly as described in the issue.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
