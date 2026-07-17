# Reproduction Trajectory — Bug 581: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38096](https://github.com/jax-ml/jax/issues/38096)
- **Repository:** jax-ml/jax @ `eb93eda9fbe95cf21c1501db8b064f66b040bf33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install `requirements.txt`.
2. Set `PYTHONPATH=codebase` so the local JAX source tree is imported.
3. Run `python repro.py` through `run_repro.sh`.
4. Observe that `jax.jit(jax.grad(...))` returns `[1.]` while eager `jax.grad(...)` returns `[inf]`.

## Observed behavior

- Running `bash run_repro.sh` exits with status 1.
- `repro_stdout.log` shows `jit_grad: [1.0]` and `eager_grad: [Infinity]` for the smallest normal float32 input.
- `repro_stdout.log` prints `BUG REPRODUCED: jit(grad(f)) != grad(f) for sqrt(abs(square(x))).`
- `repro_stderr.log` only contains the CPU fallback notice and no unrelated error.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
