# Reproduction Trajectory — Bug 594: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/38087](https://github.com/jax-ml/jax/issues/38087)
- **Repository:** jax-ml/jax @ `58d4bf8194fbe2efe7da845cf5192d7e70f58de2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtualenv and installed the runtime dependencies from requirements.txt.
2. Ran bash run_repro.sh with PYTHONPATH pointing at codebase/.
3. Imported jax from the local source tree and executed the report's dot example.
4. Confirmed the docstring still claims broadcast-compatible leading dimensions while the example succeeds with stacked batch dimensions.

## Observed behavior

- run_repro.sh completed successfully in the local checkout.
- repro_stdout.log shows doc_contains_misleading_line True.
- repro_stdout.log shows dot_shape (3, 4, 26, 1), matching the bug report example.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
