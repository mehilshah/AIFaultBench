# Bug 309

Reproduction bundle for NumPyro issue 2161.

Environment assumptions:
- Python 3.12
- CPU-only JAX
- local editable install from `codebase/`

Reproduction:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

Expected result:
- The control case completes.
- The mutable-state NNX case fails with `Leaked trace DynamicJaxprTrace`.
