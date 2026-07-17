# Reproduction Trajectory — Bug 463: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38268](https://github.com/jax-ml/jax/issues/38268)
- **Repository:** jax-ml/jax @ `5073cd4d871bd39a04a75aef1db21e065b903f1a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Clone the JAX checkout at commit 5073cd4d871bd39a04a75aef1db21e065b903f1a into `codebase/`.
2. Create a Python 3.12 virtualenv and install the pinned requirements from `requirements.txt`.
3. Run `bash run_repro.sh` to execute the JAX `jit` probe.

## Observed behavior

- Running the probe on Python 3.12.3 with jax 0.10.2.dev20260608+5073cd4d8 and jaxlib 0.10.2 prints `JitTracer(~int32[]) True False`, so `isinstance(x, ArrayLike)` is false for a traced value.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
