# Reproduction Trajectory — Bug 360: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38813](https://github.com/jax-ml/jax/issues/38813)
- **Repository:** jax-ml/jax @ `6a19c8b5ae8986e3aba44cb78b4bb024cd1997b2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install the runtime dependencies from requirements.txt.
2. Run repro.py with PYTHONPATH pointing at the local codebase/ directory and JAX_PLATFORMS=cpu.
3. Observe the internal MLIR lowering NotImplementedError from jax.nn.scaled_matmul.

## Observed behavior

- Running the minimal CPU reproducer in the local checkout raises NotImplementedError: MLIR translation rule for primitive 'scaled_matmul' not found for platform cpu.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
