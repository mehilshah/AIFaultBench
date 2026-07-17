# Reproduction Trajectory — Bug 496: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38105](https://github.com/jax-ml/jax/issues/38105)
- **Repository:** jax-ml/jax @ `085710a88cfdcc1a8bbfa4b1ba1bc6cceb63e8c9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the pinned JAX runtime and import the local source tree from codebase/.
2. Evaluate heaviside for NaN inputs in eager mode and under jax.jit.
3. Observed a mismatch for both float32 and float64: NumPy returns nan, JAX returns -1.0.

## Observed behavior

- jax version: 0.10.2.dev20260717
- jaxlib version: 0.10.1
- numpy version: 2.5.1
- float32: numpy=np.float32(nan), eager=Array(-1., dtype=float32), jit=Array(-1., dtype=float32)
- float64: numpy=np.float64(nan), eager=Array(-1., dtype=float64), jit=Array(-1., dtype=float64)

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
