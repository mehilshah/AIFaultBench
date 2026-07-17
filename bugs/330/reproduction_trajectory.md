# Reproduction Trajectory — Bug 330: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/39089](https://github.com/jax-ml/jax/issues/39089)
- **Repository:** jax-ml/jax @ `4f484c50b83d2f7bc779b23a37cd851409324e78`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh
3. Verified repro_stdout.log shows the third invocation creating a second C++ fastpath cache entry

## Observed behavior

- On this checkout, jitted_identity over a PRNG key on 2 CPU devices produced cache sizes 1, 1, 2 on the first run while trace_count stayed at 1. The same script also reproduced the no_tracing raise and the raw-key workaround staying at cache size 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
