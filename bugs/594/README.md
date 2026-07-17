# Bug 594 Repro

This folder reproduces the `jax.numpy.dot` documentation mismatch reported in
https://github.com/jax-ml/jax/issues/38087.

Observed behavior in this checkout:
- The `dot` docstring says the leading dimensions of `b` must be
  broadcast-compatible with `a`.
- The example from the report succeeds anyway and returns shape `(3, 4, 26, 1)`.

How to run:
```bash
bash run_repro.sh
```

The repro imports JAX from `codebase/` and uses the local source checkout, with
`jaxlib` provided by `requirements.txt`.
